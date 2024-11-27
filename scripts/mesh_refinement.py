import numpy as np
import h5py
import pathlib
from typing import Dict, Tuple
import logging
from tqdm import tqdm

from scripts.mesh_refinement_utils import *

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

def refine_region_step(grid_and_resolutions, cells_to_handle:List[np.array], bounds:List, goal_resolution:float=0.1):
    for curr_cell_and_resolution in cells_to_handle:
        # refine cell
        curr_resolution = curr_cell_and_resolution[-1] / 2
        if curr_resolution >= goal_resolution:
            curr_cell_id = loc_to_id(grid_and_resolutions[:,:-1], curr_cell_and_resolution[:-1])
            new_cell_centers = refine_cell(curr_cell_and_resolution[:-1], curr_resolution, bounds)
            # add new cell centers to grid and remove old cell center
            grid_and_resolutions = np.delete(grid_and_resolutions, curr_cell_id-1, 0)
            grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_centers])

    return grid_and_resolutions

def refine_region(grid_and_resolutions: np.array, hp: np.array, settings, bounds, goal_resolution:float=0.1):
    refinements = generate_refinement_steps(hp, settings["grid"]["resolution"], goal_resolution, settings, decrease_factor=1)
    # print(refinements)
    
    for goal_resolution, curr_radius in tqdm(refinements["radius"].items(), desc="Refinement steps"):
        cells_to_refine = get_circular_region(hp, grid_and_resolutions, curr_radius)
        if goal_resolution in refinements["plume_length"]:
            cells_to_refine += get_rectangular_region(hp, grid_and_resolutions, refinements["plume_length"][goal_resolution], refinements["plume_width"][goal_resolution])
        # make unique
        cells_to_refine = list(set([tuple(row) for row in cells_to_refine]))
        cells_to_refine = [np.array(row) for row in cells_to_refine]
        
        # refine cells in region
        grid_and_resolutions = refine_region_step(grid_and_resolutions, cells_to_refine, bounds, goal_resolution)
        # cells_to_refine_array = np.array(cells_to_refine)
        # plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, np.concatenate([cells_to_refine_array[:,:-1], hp.reshape(1,-1)]))
    # plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, hp.reshape(1,-1), factor=0.1)
    return grid_and_resolutions

# def refine_cell_acc_to_hps(grid_and_resolutions, hps, settings, min_resolution:float=0.1):
#     bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]
#     for curr_hp_loc in hps:
#     # refine cell around hp
#         curr_resolution = id_to_loc(grid_and_resolutions, loc_to_id(grid_and_resolutions[:,:-1], curr_hp_loc))[-1]
#         while curr_resolution > min_resolution:
#             # TODO achtung z ist falsch!!
#             cell_id_hp = loc_to_id(grid_and_resolutions[:,:-1], curr_hp_loc)
#             # TODO next loc variiert, wenn diese schleife mehrmals durchlaufen wird (also für nächste HP)
#             logging.info(f"{cell_id_hp=}")
#             old_cell_center = id_to_loc(grid_and_resolutions, cell_id_hp)
#             if old_cell_center[-1] <= curr_resolution:
#                 logging.warning("cell is already refined")
#                 curr_resolution /= 2
#                 continue
#             new_cell_centers = refine_cell(old_cell_center[:-1], curr_resolution, bounds=bounds)
#             logging.info(f"{new_cell_centers=}")
#             # add new cell centers to grid and remove old cell center
#             logging.info(f"to delete: {cell_id_hp-1=}")
#             grid_and_resolutions = np.delete(grid_and_resolutions, cell_id_hp-1, 0)
#             grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_centers])

#             curr_resolution /= 2
#     return grid_and_resolutions

# def refine_cell_centers_and_volumes_acc_to_hps(cell_centers:np.ndarray, hps:np.ndarray, settings:Dict):
#     '''for 1 dp: 1 mesh and 1 set of heat pumps'''
#     # refine mesh + store information:
#     n_cells = calc_n_cells_array(settings)
#     resolutions = np.array([settings["grid"]["resolution"],]*np.prod(n_cells))
#     ## cell centers
#     grid_and_resolutions = np.concatenate([cell_centers, resolutions.reshape(-1, 1)], axis=1)
#     refined_grid_and_resolutions = refine_cell_acc_to_hps(grid_and_resolutions, hps, settings)
#     refined_cell_centers = refined_grid_and_resolutions[:,:-1]
#     ## cell volumes
#     refined_cell_volumes = refined_grid_and_resolutions[:,-1]**3
#     # TODO store information
#     return refined_cell_centers, refined_cell_volumes


def refine_regions_acc_to_hps(num_dp:int, settings:Dict, grids:np.array, dps_hps_locs:np.array):
    logging.getLogger().setLevel(logging.WARNING)
    refined_cell_centers = []
    refined_cell_volumes = []
    # for each dp:
    for id in range(num_dp):

        # get cell centers in region
        resolutions = np.array([settings["grid"]["resolution"],]*np.prod(calc_n_cells_array(settings)))
        grid_and_resolutions = np.concatenate([grids[id], resolutions.reshape(-1, 1)], axis=1)
        if logging.getLogger().getEffectiveLevel() <= logging.WARNING:
            plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, dps_hps_locs[id], factor=0.1)
        bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]

        # for each hp:
        for hp in dps_hps_locs[id]:
            # refine region around hp
            grid_and_resolutions = refine_region(grid_and_resolutions, hp, settings, bounds)

        if logging.getLogger().getEffectiveLevel() <= logging.WARNING:
            plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, dps_hps_locs[id], factor=0.1)

        refined_cell_centers.append(grid_and_resolutions[:,:-1])
        ## cell volumes
        refined_cell_volumes.append(grid_and_resolutions[:,-1]**3)
        # TODO store information
        
    return refined_cell_centers, refined_cell_volumes


def refine_mesh(path_to_output: pathlib.Path, settings: Dict, positions_hps: np.ndarray):
    ...
    # get mesh

    # refine mesh + store information:
    ## cell centers + cell volumes
    refined_cell_centers, refined_cell_volumes = refine_regions_acc_to_hps(num_dp, settings, grids, dps_hps_locs)

    ## face areas
    ## face cell ids
    ## face centers
    ## correct face ids


    # TODO refine boundaries?