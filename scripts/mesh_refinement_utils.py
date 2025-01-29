import numpy as np
from typing import Dict, List, Union
import logging
import matplotlib.pyplot as plt

from scripts.realistic_window.param_sampling import sample_median
from scripts.realistic_window.lahm.analytical_model_lahm import estimate_plume_shape_lahm
from scripts.main_helpers import groundwater_temp
from scripts.realistic_window.dupuit_thiem import drawdown_by_dupuit_thiem
from scripts.mesh_generation_utils import loc_to_id

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

def calc_refined_face_centers(old_cell_and_res:np.ndarray, face_cell_ids:np.ndarray, faces_and_res_and_orient:np.ndarray, grid_and_res:np.ndarray, new_cell_centers_and_ress:np.ndarray):
    logging.getLogger().setLevel(logging.WARNING)
    cell_id = loc_to_id(grid_and_res[:,:-1], old_cell_and_res[:-1])
    curr_face_ids = np.concatenate([np.where(face_cell_ids[:,0] == cell_id)[0], np.where(face_cell_ids[:,1] == cell_id)[0]])

    new_face_and_res_and_orient = []
    already_refined_lines = []
    already_refined_faces = []
    for line, face_id in enumerate(curr_face_ids):
        face_pos_and_res_and_orient = faces_and_res_and_orient[face_id]

        if face_pos_and_res_and_orient[3] <= new_cell_centers_and_ress[0][-1]:
            logging.info("face already refined")
            # face is already refined -> add id to "not to remove" list
            already_refined_lines.append(line)
            already_refined_faces.append([face_id, *face_pos_and_res_and_orient])
            continue
        face_dir = get_face_orientation(old_cell_and_res[:3], face_pos_and_res_and_orient[:3])
        
        # get neighboring new cells -> new face => 2 new faces for one face
        for new_cell_and_res in new_cell_centers_and_ress:
            if np.abs(new_cell_and_res[face_dir] - face_pos_and_res_and_orient[face_dir]) == new_cell_and_res[3]*0.5:
                new_face_pos = new_cell_and_res.copy()
                new_face_pos[face_dir] = face_pos_and_res_and_orient[face_dir]
                new_face_and_res_and_orient.append([*new_face_pos, face_dir])
                
    # rm already refined faces from curr_face_ids
    curr_face_ids = np.delete(curr_face_ids, already_refined_lines)

    return np.array(new_face_and_res_and_orient), curr_face_ids, np.array(already_refined_faces)

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

def get_refinement_intervals(max_resolution: float, min_resolution: float, inner_distance: float, decrease_factor: float = 1.0) -> dict:
    n_refinement_steps = int(np.log2(max_resolution / min_resolution)) - 1
    refinements = {}
    for i in range(n_refinement_steps + 1):
        tmp = i / n_refinement_steps if n_refinement_steps > 0 else 1
        max_distance = inner_distance * (1 + decrease_factor * (1 - tmp))
        refinements[max_resolution / 2 ** (i + 1)] = np.round(max_distance, 1)
    return refinements

def calc_refinement_steps(center: np.array, max_resolution:float, min_resolution:float, orig_resolution: int, subsurface_properties:dict[str, np.ndarray], hp_temp: float, hp_rate: float, decrease_factor:float=1.0):
    # Get parameters
    hp_id = (center / orig_resolution).astype(int)
    try:
        hydr_cond = sample_median(subsurface_properties["hydraulic_conductivity"], [hp_id[1],hp_id[0]], [3,3]) # TODO orientation hp_id correct??
        thickness = sample_median(subsurface_properties["thickness"], [hp_id[1],hp_id[0]], [3,3])
        v_a = sample_median(subsurface_properties["darcy_velocity"], [hp_id[1],hp_id[0]], [3,3])
    except:
        hydr_cond = subsurface_properties["hydraulic_conductivity"][hp_id[1],hp_id[0]]
        thickness = subsurface_properties["thickness"][hp_id[1],hp_id[0]]
        v_a = subsurface_properties["darcy_velocity"][hp_id[1],hp_id[0]]
    T_inj_diff = hp_temp - groundwater_temp()

    # Estimate the radius of the "Absenktrichter" with Sichardt around each well
    inner_radius = sichardt_distance(hydr_cond, thickness, hp_rate) 
    # inner_radius = 2.5 # for debug/testing todo
    inner_radius = np.min([inner_radius, 20]) # limit to 20m
    print(f"sichardt distance (=inner_radius) {inner_radius}") # logging.info
    refinements_radius = get_refinement_intervals(max_resolution, min_resolution, inner_radius, decrease_factor)

    # Estimate the plume shape parameters (1K isoline) with LAHM
    safety_factor = 1
    # TODO check dass hp_rate in m^3/s
    # print(f"{T_inj_diff=}, {hp_rate=}, {v_a=}, {thickness=}")
    length_1K, width_1K = estimate_plume_shape_lahm(T_inj_diff, hp_rate, v_a, thickness)

    length_1K *= (1+safety_factor)
    length_1K = np.max([length_1K, 20]) # for debug/testing TODO 
    width_1K *= (1+safety_factor)
    width_1K = np.max([width_1K, 10]) # for debug/testing TODO
    print(f"downstream: {length_1K=}\nat half length: {width_1K=}")
    min_resolution_plume = 1
    refinement_plume_length = get_refinement_intervals(max_resolution, min_resolution_plume, length_1K, decrease_factor)
    refinement_plume_width = get_refinement_intervals(max_resolution, min_resolution_plume, width_1K, decrease_factor)
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

def sichardt_distance(hydr_cond: float, thickness: float, q_inj: float) -> List[np.array]:
    '''Sichardt  (1928)
    
    Returns distance in m, float.

    Keyword arguments:
        cell_hp -- location of heat pump in cell,  np.array
        hydr_cond -- hydraulic conductivity, float or np.array
        thickness -- thickness of aquifer, float or np.array
    '''
    drawdown = drawdown_by_dupuit_thiem(hydr_cond, thickness, q_inj) # Absenkung mit Dupuit Thiem Brunnenformel, acc. to real pump rate - no need to estimate
    # max_drawdown = 1/3 * thickness
    # print("drawdown", drawdown, max_drawdown)
    return 3000 * drawdown * np.sqrt(hydr_cond)

def calc_refined_cell_centers(old_cell_center, curr_resolution, bounds:List):
    new_cell_centers = []
    offset_list = [[-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0]]
    for offset in offset_list:
        new_pos = old_cell_center + np.array(offset) * curr_resolution / 2
        if new_pos[0] < bounds[0][0] or new_pos[0] > bounds[0][1] or new_pos[1] < bounds[1][0] or new_pos[1] > bounds[1][1]:
            continue
        new_cell_centers.append([*new_pos, curr_resolution])
    return np.array(new_cell_centers)