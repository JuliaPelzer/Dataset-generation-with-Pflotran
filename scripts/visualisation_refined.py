import matplotlib.pyplot as plt
import numpy as np
import h5py
from typing import TypedDict, Tuple
from pathlib import Path
import logging

from scripts.utils import aligned_colorbar
import scripts.cmap_jp
from scripts.utils import timing

@timing
def plot_results(path_run: Path, plot_name: str = "plot_simulation_results",plot_area=(0,-1,0,-1),     plot_res:float = 0.15625):
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
    
    plt.figure()
    n_subplots = len(data)
    _, axes = plt.subplots(n_subplots, 1, sharex=True, figsize=(8, 4 * (n_subplots)))
    
    for index, data_point in enumerate(data):
        values = generate_regular_cell_values(plot_res, mesh, data_point)
        plt.sca(axes[index])
        plt.title(f"{data_point['property']} at time {data_point['time_years']}")
        plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp", interpolation="nearest") #, vmin=10, vmax=20)
        # offset of 0.5*plot_res to center the cells, i.e. to x-,y-scale
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.gca().invert_yaxis()
        aligned_colorbar(label=data_point["property"])
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
            if not time in ["   0 Time  0.00000E+00 y"]:
                for property in file[time].keys():
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

        mesh[:, 3] = np.sqrt(mesh[:, 3]/5) # TODO wenn 3D dann np.cbrt

    return list_to_plot, mesh

def calc_shape_regular_plot_grid(plot_res: float, mesh: np.ndarray) -> Tuple[int, int]:
    res_min = np.min(mesh[:, 3]) # TODO wenn 3D dann np.cbrt
    res_max = np.max(mesh[:, 3]) # TODO wenn 3D dann np.cbrt

    # reihe mit verdopplungen von res_min bis res_max
    res_len = np.log2(res_max/res_min)
    res_options = [res_min * np.power(2, i) for i in range(int(res_len)+1)]
    assert plot_res in res_options, f"{plot_res=}, {res_options=}"

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
    
    for (curr_x,curr_y,curr_z,curr_res), value in zip(mesh, data["data"]):
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
