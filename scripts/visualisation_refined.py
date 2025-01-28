import matplotlib.pyplot as plt
import numpy as np
import h5py
from typing import TypedDict, Tuple
from pathlib import Path
from tqdm import tqdm
from scripts.utils import aligned_colorbar
import scripts.cmap_jp
from scripts.utils import timing
import yaml

@timing
def plot_results(path_run: Path, plot_name: str = "plot_simulation_results", plot_area=(0,-1,0,-1), plot_res:float = None):
    """
    Plots results on a refined mesh of the simulation in the folder path_run. The results are saved in a picture with the name plot_name.

    Args:
        path_run: Path to the run folder
        plot_name: Name of the picture
        plot_area: Area to plot, default is the whole area
        plot_res: Resolution of the plot, default is 0.15625 [m]

    Returns:
        None
    """
    data, mesh = load_data_for_visu(path_run)
    if plot_res is None:
        plot_res = np.min(mesh[:,3])
    print(f"plot_res set to {plot_res}")
    
    plt.figure()
    n_subplots = len(data)
    _, axes = plt.subplots(1, n_subplots, sharex=True, figsize=(4 * n_subplots, 9))
    
    for index, data_point in enumerate(data):
        values = generate_regular_cell_values(plot_res, mesh, data_point)
        plt.sca(axes[index])
        plt.title(f"{data_point['property']} at time {data_point['time_years']}")
        if data_point["property"] == "Material ID":
            plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp", interpolation="nearest", origin="upper", vmin=1, vmax=3)
        else:
            plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp", interpolation="nearest", origin="upper") #, vmin=10, vmax=20)
        # offset of 0.5*plot_res to center the cells, i.e. to x-,y-scale
        if plot_area == (0, -1, 0, -1):
            if index == 0:
                plt.yticks(np.arange(0, values.shape[0], 100//plot_res), (np.arange(0, values.shape[0], 100//plot_res)*plot_res+0.5*plot_res).astype(int))
            plt.xticks(np.arange(0, values.shape[1], 100//plot_res), (np.arange(0, values.shape[1], 100//plot_res)*plot_res+0.5*plot_res).astype(int))
        else:
            print("for cutouts no xticks, yticks implemented yet")
        if index == 0:
            plt.ylabel("y [m]")
        plt.xlabel("x [m]")
        aligned_colorbar(label=data_point["property"])
        # print(f"property {data_point['property']} , min: {np.min(values)}, max: {np.max(values)}")
    plt.tight_layout()

    pic_file_name = path_run/f"{plot_name}.png"
    print(f"Resulting picture is at {pic_file_name}") #logging.info
    plt.savefig(pic_file_name, dpi=400)


# HELPFER FUNCTIONS AND CLASSES
class Property(TypedDict):
    data: np.ndarray
    property: str
    time_years: str

def time_from_pflotran_time(time:str):
    try:
        return float(time.split(" ")[6])
    except:
        return str(time)
    

def load_data_for_visu(path_run: Path) -> Tuple[list[Property], np.ndarray]:
    """
    Load the data from the pflotran.h5 file and the mesh from the mesh.h5 file
    
    Args:
        path_run: Path to the run folder
    Returns:
        list_to_plot: List of dictionaries with the data, property name and time in years
        mesh: Mesh of the domain with the cell centers and volumes
    """

    list_to_plot = []
    with h5py.File(path_run/"pflotran.h5", "r") as file:
        for time in file.keys():
            if not time in []: #"   0 Time  0.00000E+00 y"]:
                for property in file[time].keys():
                    if property not in []: #"Material ID", "Liquid Saturation", "Liquid Z-Velocity [m_per_y]", "Permeability X [m^2]"]:
                        data: Property = {
                        "data": np.array(file[time][property]),
                        "property": str(property),
                        "time_years": time_from_pflotran_time(time)
                        }
                        list_to_plot.append(data)
  
    with h5py.File(path_run/"mesh.h5", "r") as mesh_file:
        cell_centers = np.array(mesh_file["Domain/Cells/Centers"])
        cell_volumes = np.array(mesh_file["Domain/Cells/Volumes"])
        mesh = np.concatenate([cell_centers, cell_volumes[:,None]], axis=1)

        orig_res = yaml.safe_load(open(path_run/"settings.yaml"))["grid"]["resolution"]
        mesh[:, 3] = np.sqrt(mesh[:, 3]/orig_res) # TODO wenn 3D dann np.cbrt statt /orig_res

    return list_to_plot, mesh

def calc_shape_regular_plot_grid(plot_res: float, mesh: np.ndarray) -> Tuple[int, int]:
    res_min = np.min(mesh[:, 3]) # TODO wenn 3D dann np.cbrt
    res_max = np.max(mesh[:, 3]) # TODO wenn 3D dann np.cbrt

    # reihe mit verdopplungen von res_min bis res_max
    res_len = np.log2(res_max/res_min)
    res_options = [res_min * np.power(2, i) for i in range(int(res_len)+1)]
    if not plot_res in res_options:
        plot_res = res_options[np.argmin(np.abs(np.array(res_options)-plot_res))]
        print(f"plot_res changed to {plot_res}")

    min_len = np.min(mesh[:, 0]-mesh[:, 3]/2)
    max_len = np.max(mesh[:, 0]+mesh[:, 3]/2)
    min_width = np.min(mesh[:, 1]-mesh[:, 3]/2)
    max_width = np.max(mesh[:, 1]+mesh[:, 3]/2)

    n_cells_x = ((max_len - min_len)/plot_res).astype(int)
    n_cells_y = ((max_width - min_width)/plot_res).astype(int)
    
    return n_cells_x, n_cells_y

def generate_regular_cell_values(plot_res: float, mesh: np.ndarray, data: Property) -> np.ndarray:
    # interpolate and average data to mesh
    # TODO 3D

    n_cells_x,n_cells_y = calc_shape_regular_plot_grid(plot_res, mesh)

    values = np.zeros((n_cells_x, n_cells_y))
    for (curr_x,curr_y,curr_z,curr_res), value in zip(mesh, data["data"]): # tqdm
        start_pos = np.array([curr_x, curr_y])-curr_res/2
        cell = (start_pos/plot_res).astype(int) # TODO correct this way? also for twice refined cells?
        if curr_res == plot_res:
            assert np.abs(cell-(start_pos/plot_res)).all() == 0, f"{cell=}, {(start_pos/plot_res)=}"
            values[cell[0], cell[1]] = value
        elif curr_res < plot_res:
            values[cell[0], cell[1]] += value * (curr_res/plot_res)**2
        elif curr_res > plot_res:
            # update all cells that are covered by the larger cell
            for i in range(int(curr_res/plot_res)):
                for j in range(int(curr_res/plot_res)):
                    values[cell[0]+i, cell[1]+j] = value
        else:
            raise ValueError(f"{curr_res=}, {plot_res=}")
        
    return values
