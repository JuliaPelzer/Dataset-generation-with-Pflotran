import matplotlib.pyplot as plt
import numpy as np
import h5py
from typing import TypedDict, Tuple
from pathlib import Path
import logging

import scripts.cmap_jp
from scripts.utils import aligned_colorbar
from scripts.utils import timing

logging.basicConfig(level=logging.WARNING)

@timing
def plot_results(path_run: Path, plot_name: str = "plot_simulation_results", plot_area=(0,-1,0,-1), plot_res:float = None, slice_height_cells=None, **kwargs):
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
    data, mesh_and_res = load_data_for_visu(path_run)
    
    if plot_res is None:
        plot_res = np.min(mesh_and_res[:,3])
    print(f"plot_res set to {plot_res}")
    n_cells = calc_shape_regular_plot_grid(plot_res, mesh_and_res)
    if slice_height_cells is None:
        slice_height_cells = int(n_cells[2]//2)

    plt.figure()
    n_subplots = len(data)
    _, axes = plt.subplots(1, n_subplots, sharex=True, figsize=(4 * n_subplots, 9))
    
    for index, data_point in enumerate(data):
        values = generate_regular_cell_values(plot_res, mesh_and_res, data_point, n_cells)
        values = values[...,slice_height_cells]
        plt.sca(axes[index])
        plt.title(f"{data_point['property']}")
        if data_point["property"] == "Material ID":
            plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp_linear", interpolation="nearest", origin="lower", vmin=1, vmax=3)
        else:
            plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp_linear", interpolation="nearest", origin="lower") #, vmin=10, vmax=20)
        if plot_area == (0, -1, 0, -1):
            if index == 0:
                plt.yticks(np.arange(0, values.shape[0], 100//plot_res), (np.arange(0, values.shape[0], 100//plot_res)*plot_res+0.5*plot_res).astype(int))
            else:
                plt.yticks([])
            plt.xticks(np.arange(0, values.shape[1], 100//plot_res), (np.arange(0, values.shape[1], 100//plot_res)*plot_res+0.5*plot_res).astype(int))
        else:
            logging.info("for cutouts no xticks, yticks implemented yet")
        if index == 0:
            plt.ylabel("y [m]")
        plt.xlabel("x [m]")
        aligned_colorbar(label=data_point["property"])

    plt.tight_layout()
    # overall pic title
    plt.suptitle(f"Results of simulation after {data_point['time_years']} years, plot resolution {plot_res} m")
    pic_file_name = path_run/f"{plot_name}_res{plot_res}_z{slice_height_cells}.png"
    print(f"Resulting picture is at {pic_file_name}") #logging.info
    plt.savefig(pic_file_name, **kwargs)

@timing
def plot_results_at_height(path_run: Path, plot_name: str = "plot_simulation_results", plot_area=(0,-1,0,-1), plot_res:float = None, slice_height=None, **kwargs):
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
    data, mesh_and_res = load_data_for_visu(path_run)
    
    if plot_res is None:
        plot_res = np.min(mesh_and_res[:,3])
    print(f"plot_res set to {plot_res}")
    n_cells = calc_shape_regular_plot_grid(plot_res, mesh_and_res)
    if slice_height is None:
        slice_height = (np.max(mesh_and_res[:, 2])+np.min(mesh_and_res[:, 2]))/2

    plt.figure()
    n_subplots = len(data)
    _, axes = plt.subplots(1, n_subplots, sharex=True, figsize=(4 * n_subplots, 9))
    for index, data_point in enumerate(data):
        values = generate_regular_cell_values_at_height(plot_res, mesh_and_res, data_point, n_cells, slice_height)
        plt.sca(axes[index])
        plt.title(f"{data_point['property']}")
        if data_point["property"] == "Material ID":
            plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp_linear", interpolation="nearest", origin="lower", vmin=1, vmax=3)
        else:
            plt.imshow(values[plot_area[0]:plot_area[1], plot_area[2]:plot_area[3]], cmap="jp_linear", interpolation="nearest", origin="lower")
        # offset of 0.5*plot_res to center the cells, i.e. to x-,y-scale
        if plot_area == (0, -1, 0, -1):
            if index == 0:
                plt.yticks(np.arange(0, values.shape[0], 100//plot_res), (np.arange(0, values.shape[0], 100//plot_res)*plot_res+0.5*plot_res).astype(int))
            else:
                plt.yticks([])
            plt.xticks(np.arange(0, values.shape[1], 100//plot_res), (np.arange(0, values.shape[1], 100//plot_res)*plot_res+0.5*plot_res).astype(int))
        else:
            logging.info("for cutouts no xticks, yticks implemented yet")
        if index == 0:
            plt.ylabel("y [m]")
        plt.xlabel("x [m]")
        aligned_colorbar(label=data_point["property"])

    plt.tight_layout()

    # overall pic title
    plt.suptitle(f"Results of simulation after {data_point['time_years']} years, plot resolution {plot_res} m")
    pic_file_name = path_run/f"{plot_name}_res{plot_res}_z{slice_height}_at_halfheight.png"
    print(f"Resulting picture is at {pic_file_name}") #logging.info
    plt.savefig(pic_file_name, **kwargs)

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
            if "2.75" in time:
                for property in file[time].keys():
                    if property not in ["Material ID", "Liquid Saturation","Liquid Z-Velocity [m_per_y]",]: # "Liquid Pressure [Pa]", "Liquid X-Velocity [m_per_y]","Liquid Y-Velocity [m_per_y]", "Permeability X [m^2]"
                        data: Property = {
                        "data": np.array(file[time][property]),
                        "property": str(property),
                        "time_years": time_from_pflotran_time(time)
                        }
                        list_to_plot.append(data)
    mesh = load_mesh(path_run)
    
    return list_to_plot, mesh

def load_mesh(path_run):
    with h5py.File(path_run/"mesh.h5", "r") as mesh_file:
        cell_centers = np.array(mesh_file["Domain/Cells/Centers"])
        cell_volumes = np.array(mesh_file["Domain/Cells/Volumes"])
        mesh = np.concatenate([cell_centers, cell_volumes[:,None]], axis=1)

        mesh[:, 3] = np.round(np.cbrt(mesh[:, 3]),8)
    return mesh

def calc_shape_regular_plot_grid(plot_res: float, mesh: np.ndarray) -> Tuple[int, int, int]:
    res_min = np.round(np.min(mesh[:, 3]),8)
    res_max = np.round(np.max(mesh[:, 3]),8)

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
    min_height = np.min(mesh[:, 2]-mesh[:, 3]/2)
    max_height = np.max(mesh[:, 2]+mesh[:, 3]/2)

    n_cells_x = int(np.maximum((max_len - min_len)/plot_res, 1))
    n_cells_y = int(np.maximum((max_width - min_width)/plot_res, 1))
    n_cells_z = int(np.maximum((max_height - min_height)/plot_res, 1))
    
    return n_cells_x, n_cells_y, n_cells_z

def generate_regular_cell_values(plot_res: float, mesh: np.ndarray, data: Property, n_cells: Tuple[int]) -> np.ndarray:
    # interpolate and average data to mesh
    # z-dimension: sliced at slice_height

    n_cells_x, n_cells_y, n_cells_z = n_cells
    weights = np.zeros((n_cells_x, n_cells_y, n_cells_z))
    values = np.zeros((n_cells_x, n_cells_y, n_cells_z))
    for (curr_x,curr_y,curr_z,curr_res), value in zip(mesh, data["data"]):
        start_pos = np.array([curr_x, curr_y, curr_z])-curr_res/2
        cell = (start_pos//plot_res).astype(int)
        if curr_res <= plot_res:
            values[cell[0], cell[1], cell[2]] += value * (curr_res/plot_res)**2
            weights[cell[0], cell[1], cell[2]] += (curr_res/plot_res)**3
        elif curr_res > plot_res:
            # update all cells that are covered by the larger cell
            for i in range(int(curr_res/plot_res)):
                for j in range(int(curr_res/plot_res)):
                    for k in range(int(curr_res/plot_res)):
                        # if int(curr_res/plot_res) > 2:
                        #     print(f"ijk", i,j,k)
                        values[cell[0]+i, cell[1]+j, cell[2]+k] += value
                        weights[cell[0]+i, cell[1]+j, cell[2]+k] += 1
        else:
            raise ValueError(f"{curr_res=}, {plot_res=}")
    values /= weights
    assert np.all(weights == 1), f"weights are not 1 at {np.where(weights != 1)}"
    
    return values

def generate_regular_cell_values_at_height(plot_res: float, mesh: np.ndarray, data: Property, n_cells: Tuple[int], slice_height: int = 0) -> np.ndarray:
    # interpolate and average data to mesh
    # z-dimension: sliced at slice_height

    n_cells_x, n_cells_y, _ = n_cells
    epsilon=10E-4
    height_e = slice_height+epsilon
    weights = np.zeros((n_cells_x, n_cells_y))
    values = np.zeros((n_cells_x, n_cells_y))
    for (curr_x,curr_y,curr_z,curr_res), value in zip(mesh, data["data"]):
        start_pos = np.array([curr_x, curr_y, curr_z])-curr_res/2
        cell = (start_pos//plot_res).astype(int)
        if np.abs(curr_z - height_e) < curr_res/2:
            if curr_res <= plot_res:
                values[cell[0], cell[1]] += value * (curr_res/plot_res)**2
                weights[cell[0], cell[1]] += (curr_res/plot_res)**2
            elif curr_res > plot_res:
                # update all cells that are covered by the larger cell
                for i in range(int(curr_res/plot_res)):
                    for j in range(int(curr_res/plot_res)):
                        values[cell[0]+i, cell[1]+j] += value
                        weights[cell[0]+i, cell[1]+j] += 1
            else:
                raise ValueError(f"{curr_res=}, {plot_res=}")
    values /= weights
    print(np.min(weights), np.max(weights), np.min(data["data"]), np.max(data["data"]), np.min(values), np.max(values))
    
    return values

if __name__ == "__main__":
    path_run = Path('outputs/test_refineD6/RUN_0')
    plot_results(path_run, plot_res =2.5)