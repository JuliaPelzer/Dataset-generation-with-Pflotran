import numpy as np
import h5py
import pathlib
from typing import Dict, Tuple, List, Union
import logging
import matplotlib.pyplot as plt

from scripts.mesh_generation_utils import loc_to_id, id_to_loc, calc_n_cells_array
from scripts.realistic_window.param_sampling import slice_box
from scripts.realistic_window.lahm.analytical_model_lahm import estimate_plume_shapeparams_lahm

def get_circular_region(hp:np.array, grid_and_resolutions:np.array, radius:float):
    # if cell within radius, add to region
    region = []
    # TODO how to handle z-dim?
    for cell in grid_and_resolutions:
        if np.linalg.norm(cell[:-1] - hp) < radius + 0.75 * cell[-1]:
            region.append(cell)
    return region


def get_rectangular_region(hp:np.array, grid_and_resolutions:np.array, width:float, length:float):
# 3. define region as 1m refinement
    region = []
    # TODO how to handle z-dim?
    for cell in grid_and_resolutions:
        # !! Expects flow to be in x-direction, from left to right
        if np.abs(cell[1] - hp[1]) < length/2 + 0.5*cell[-1] and 0 < cell[0] + 0.5*cell[-1] - hp[0] < width:
            region.append(cell)
    return region

def get_face_orientation(cell_position, face_position):
    id_differ = np.where(cell_position - face_position)[0]
# expects the numbers to only differ in 1 index
    assert len(id_differ) == 1, f"cell and face should share 2 positions, but cell={cell_position} and face={face_position} differ in {id_differ}"
    return id_differ[0]

def calc_inner_face_centers(new_4cell_centers:np.ndarray):
    # 4 new faces between new cells
    new_face_centers = []
    for inter1, inter2 in [(0, 1), (1, 3), (3, 2), (2, 0)]:
        new_face_center = (new_4cell_centers[inter1,:-1] + new_4cell_centers[inter2,:-1])/2
        new_face_orient = get_face_orientation(new_4cell_centers[inter1,:-1], new_face_center) # TODO changed to use new cell center
        new_face_centers.append([*new_face_center, new_4cell_centers[0,-1], new_face_orient])
    return np.array(new_face_centers)

def calc_cells_to_refine(grid_and_resolutions, hp, goal_resolution, refinement_steps, curr_radius):
    cells_to_refine = get_circular_region(hp, grid_and_resolutions, curr_radius)
    if goal_resolution in refinement_steps["plume_length"]:
        cells_to_refine += get_rectangular_region(hp, grid_and_resolutions, refinement_steps["plume_length"][goal_resolution], refinement_steps["plume_width"][goal_resolution])
        # make unique
    cells_to_refine = list(set([tuple(row) for row in cells_to_refine]))
    cells_to_refine = np.array([np.array(row) for row in cells_to_refine])
    return cells_to_refine

def determine_refinement_intervals(max_resolution: float, min_resolution: float, inner_distance: float, decrease_factor: float = 1.0) -> dict:
    n_refinement_steps = int(np.log2(max_resolution / min_resolution)) - 1
    refinements = {}
    for i in range(n_refinement_steps + 1):
        max_distance = inner_distance * (1 + decrease_factor * (1 - i / n_refinement_steps))
        refinements[max_resolution / 2 ** (i + 1)] = max_distance
    return refinements

def calc_refinement_steps(center: np.array, max_resolution:float, min_resolution:float, settings:Dict, decrease_factor:float=1.0):
    # Get parameters
    hydr_cond, thickness = settings["subsurface"]["hydraulic conductivity"], settings["subsurface"]["aquifer thickness"]
    T_inj_diff, v_a = settings["max pump"]["temperature"], settings["subsurface"]["darcy velocity"]

    # Estimate the radius of the "Absenktrichter" with Sichardt around each well
    inner_radius = sichardt_distance(center, hydr_cond, thickness, debug=2.5)
    logging.info(f"sichardt distance (=inner_radius) {inner_radius}")
    # max_influence_distance = inner_radius * (1+decrease_factor)
    refinements_radius = determine_refinement_intervals(max_resolution, min_resolution, inner_radius, decrease_factor)

    # Estimate the plume shape parameters (1K isoline) with LAHM
    safety_factor = 1
    length_1K, width_1K = estimate_plume_shapeparams_lahm(T_inj_diff, 1/3 * thickness, v_a, thickness)
    length_1K *= (1+safety_factor)
    length_1K = 15
    width_1K *= (1+safety_factor)
    width_1K = 5
    logging.info(f"downstream: {length_1K=}\nat half length: {width_1K=}")
    min_resolution_plume = 1
    refinement_plume_length = determine_refinement_intervals(max_resolution, min_resolution_plume, length_1K, decrease_factor)
    refinement_plume_width = determine_refinement_intervals(max_resolution, min_resolution_plume, width_1K, decrease_factor)
    
    return {"radius": refinements_radius, "plume_length": refinement_plume_length, "plume_width": refinement_plume_width}


def plot_grid(centers_new, vols_new, settings:Dict, hps=np.array([]), factor:int=1000):
    # plt.figure(figsize=(int(settings["grid"]["size [m]"][0]/10), int(settings["grid"]["size [m]"][1]/10)))
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
        max_downdraw = 1/3 * thickness
        return 3000 * max_downdraw * np.sqrt(hydr_cond)
    else:
        return debug


def calc_refined_cell_centers(old_cell_center, curr_resolution, bounds:List):
    new_cell_centers = []
    offset_list = [[-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0]]
    for offset in offset_list:
        new_pos = old_cell_center + np.array(offset) * curr_resolution / 2
        if new_pos[0] < bounds[0][0] or new_pos[0] > bounds[0][1] or new_pos[1] < bounds[1][0] or new_pos[1] > bounds[1][1]:
            continue
        new_cell_centers.append([*new_pos, curr_resolution])
    return np.array(new_cell_centers)