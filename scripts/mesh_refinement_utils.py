import numpy as np
import h5py
import pathlib
from typing import Dict, Tuple, List, Union
import logging
import matplotlib.pyplot as plt

from scripts.mesh_generation_utils import loc_to_id, id_to_loc, calc_n_cells_array
from scripts.realistic_window.param_sampling import slice_box

logging.basicConfig(level=logging.WARNING)

def refine_cell(old_cell_center, curr_resolution, bounds:List):
    new_cell_centers = []
    offset_list = [[-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0]]
    for offset in offset_list:
        new_pos = old_cell_center + np.array(offset) * curr_resolution / 2
        if new_pos[0] < bounds[0][0] or new_pos[0] > bounds[0][1] or new_pos[1] < bounds[1][0] or new_pos[1] > bounds[1][1]:
            continue
        new_cell_centers.append([*new_pos, curr_resolution])
    new_cell_centers = np.array(new_cell_centers)
    return new_cell_centers

def refine_grid_acc_to_hps(grid_and_resolutions, hps, settings, min_resolution:float=0.1):
    bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]
    for curr_hp_loc in hps:
    # refine cell around hp
        curr_resolution = id_to_loc(grid_and_resolutions, loc_to_id(grid_and_resolutions[:,:-1], curr_hp_loc))[-1]
        while curr_resolution > min_resolution:
        # TODO achtung z ist falsch!!
            cell_id_hp = loc_to_id(grid_and_resolutions[:,:-1], curr_hp_loc)
        # TODO next loc variiert, wenn diese schleife mehrmals durchlaufen wird (also für nächste HP)
            logging.info(f"{cell_id_hp=}")
            old_cell_center = id_to_loc(grid_and_resolutions, cell_id_hp)
            if old_cell_center[-1] <= curr_resolution:
                logging.warning("cell is already refined")
                curr_resolution /= 2
                continue
            new_cell_centers = refine_cell(old_cell_center[:-1], curr_resolution, bounds=bounds)
            logging.info(f"{new_cell_centers=}")
        # add new cell centers to grid and remove old cell center
            logging.info(f"to delete: {cell_id_hp-1=}")
            grid_and_resolutions = np.delete(grid_and_resolutions, cell_id_hp-1, 0)
            grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_centers])

            curr_resolution /= 2
    return grid_and_resolutions

def refine_cell_centers_and_volumes_acc_to_hps(cell_centers:np.ndarray, hps:np.ndarray, settings:Dict):
    '''for 1 dp: 1 mesh and 1 set of heat pumps'''
    # refine mesh + store information:
    n_cells = calc_n_cells_array(settings)
    resolutions = np.array([settings["grid"]["resolution"],]*np.prod(n_cells))
    ## cell centers
    grid_and_resolutions = np.concatenate([cell_centers, resolutions.reshape(-1, 1)], axis=1)
    refined_grid_and_resolutions = refine_grid_acc_to_hps(grid_and_resolutions, hps, settings)
    refined_cell_centers = refined_grid_and_resolutions[:,:-1]
    ## cell volumes
    refined_cell_volumes = refined_grid_and_resolutions[:,-1]**3
    # TODO store information
    return refined_cell_centers, refined_cell_volumes

## face areas
## face cell ids
## face centers
## correct face ids


# TODO boundaries: specific boundary handling necessary?

def plot_grid(centers_new, vols_new, settings:Dict, hps=np.array([]), factor:int=1000):
    plt.figure(figsize=(int(settings["grid"]["size [m]"][0]/10), int(settings["grid"]["size [m]"][1]/10)))
    for hp in hps:
        plt.plot(hp[0], hp[1], "rx")

    plt.scatter(centers_new[:, 0], centers_new[:, 1], c="b", s=vols_new*factor)
    plt.grid()
    plt.xlim(0,settings["grid"]["size [m]"][0])
    plt.ylim(0,settings["grid"]["size [m]"][1])
    plt.show()

def sichardt_distance(cell_hp: np.array, hydr_cond: Union[float, np.array], thickness: Union[float, np.array], debug:Union[float, None]=None) -> List[np.array]:
    '''Sichardt  (1928)
    
    Returns distance in m, float.

    Keyword arguments:
        cell_hp -- location of heat pump in cell,  np.array
        hydr_cond -- hydraulic conductivity, float or np.array
        thickness -- thickness of aquifer, float or np.array
    '''
    if not debug:
        if isinstance(hydr_cond, np.ndarray):
            hydr_cond = slice_box(hydr_cond, cell_hp, [3,3])
        if isinstance(thickness, np.ndarray):
            thickness = slice_box(thickness, cell_hp, [3,3])
        max_downdraw = 2/3 * thickness
        return 3000 * max_downdraw * np.sqrt(hydr_cond)
    else:
        return debug

