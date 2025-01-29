import numpy as np
from pathlib import Path
from typing import Dict
import logging
from tqdm import tqdm

from scripts.mesh_refinement_utils import *
from scripts.mesh_generation_utils import store_mesh, calc_face_cell_ids

# @profile
def refine_region_acc_to_hp(grid_and_resolutions: np.ndarray, faces_and_res_and_orient:np.ndarray, face_cell_ids:np.ndarray, orig_resolution: int, hp_loc: np.ndarray, hp_temperature:float, hp_rate: float, subsurface_properties:dict[str,np.ndarray], bounds, max_resolution: int, min_resolution:float=0.1):
    refinement_steps = calc_refinement_steps(hp_loc, max_resolution, min_resolution, orig_resolution, subsurface_properties, hp_temperature, hp_rate, decrease_factor=1)
    
    for goal_resolution, curr_radius in refinement_steps["radius"].items():
        if curr_radius == 0:
            print("curr_radius is 0, skipping")
            continue

        cells_to_refine_and_res = calc_cells_to_refine(grid_and_resolutions, hp_loc, goal_resolution, refinement_steps, curr_radius)
        print(f"For resolution {goal_resolution}: {len(cells_to_refine_and_res)=}")
        # refine cells in region
        for id in tqdm(range(len(cells_to_refine_and_res)), desc="Cells"):
            # refine cell
            curr_resolution = cells_to_refine_and_res[id][-1]
            if curr_resolution / 2 >= goal_resolution:
                curr_cell_id = loc_to_id(grid_and_resolutions, cells_to_refine_and_res[id][:-1])
                new_cell_and_res_tmp = calc_refined_cell_centers(cells_to_refine_and_res[id][:-1], curr_resolution / 2, bounds)
                # get old face centers, calc new face centers
                new_outer_face_centers_and_res_and_orient, old_face_ids, already_refined_faces = calc_refined_face_centers(cells_to_refine_and_res[id], face_cell_ids, faces_and_res_and_orient, grid_and_resolutions, new_cell_and_res_tmp)
                new_inner_face_centers_and_res_and_orient = calc_inner_face_centers(new_cell_and_res_tmp)
                try:
                    new_face_centers_and_res_and_orient_tmp = np.concatenate([new_inner_face_centers_and_res_and_orient, new_outer_face_centers_and_res_and_orient])
                except:
                    new_face_centers_and_res_and_orient_tmp = new_inner_face_centers_and_res_and_orient

                ## overwrite and append: cells: centers, volumes; faces: centers, areas, cell ids
                # old cell ids: curr_cell_id; # new cells: new_cell_centers_tmp
                grid_and_resolutions[curr_cell_id-1] = new_cell_and_res_tmp[0]
                grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_and_res_tmp[1:]])

                # new faces: new_face_centers_tmp, new_face_cell_ids_tmp
                new_face_cell_ids_tmp = calc_face_cell_ids(new_face_centers_and_res_and_orient_tmp, grid_and_resolutions)

                collect_already_faces_cell_ids = []
                if len(already_refined_faces) > 0:
                    neighbors = calc_face_cell_ids(already_refined_faces[:,1:], grid_and_resolutions)
                    for neigh, face in zip(neighbors, already_refined_faces):
                        face_cell_ids[int(face[0])] = neigh
                        collect_already_faces_cell_ids.append(neigh)
                collect_already_faces_cell_ids = np.array(collect_already_faces_cell_ids)

                # pos of refined_face in faces_and_resolutions
                for id, old_f in enumerate(old_face_ids):
                    faces_and_res_and_orient[old_f] = new_face_centers_and_res_and_orient_tmp[id]
                    # update cell ids in faces, face cell ids genauso wie face centers machen
                    face_cell_ids[old_f] = new_face_cell_ids_tmp[id]
                faces_and_res_and_orient = np.concatenate([faces_and_res_and_orient, new_face_centers_and_res_and_orient_tmp[len(old_face_ids):]])
                face_cell_ids = np.concatenate([face_cell_ids, new_face_cell_ids_tmp[len(old_face_ids):]])
        
    return grid_and_resolutions, faces_and_res_and_orient, face_cell_ids


def mesh_refinements_all_dps(num_dp:int, settings:Dict, meshs_regular: list, dps_hps_locs:np.ndarray, dps_hps_temps:np.ndarray, dps_hps_rates:np.ndarray, windows_properties_collected: list[dict[str, np.ndarray]], orig_resolution: int, output_dir: Path, min_resolution:float=0.1) -> list[Dict[str, np.ndarray]]:
    """
    Refine regular-grid around hp according to hps and settings
    Outputs:
    meshs_refined: list (len=num_dp) of dicts with keys:
    - cell_centers: list of np.arrays (#cells, 3) with cell centers
    - cell_volumes: list of np.arrays (#cells, ) with cell volumes
    - face_areas: list of np.arrays (#faces, ) with face areas
    - face_cell_ids: list of np.arrays (#faces, 2) with cell ids of faces
    - face_centers: list of np.arrays (#faces, 3) with face centers
    """
    meshs_refined = []

    # for each dp:
    for id in tqdm(range(num_dp), desc="Runs"):
        output_run_dir = output_dir / f"RUN_{id}"
        # get cell centers in region
        resolutions_cells = np.array([settings["grid"]["resolution"],]*len(meshs_regular[id]["cell_centers"]))
        grid_and_resolutions = np.concatenate([meshs_regular[id]["cell_centers"], resolutions_cells.reshape(-1, 1)], axis=1)
        bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]], [0, settings["grid"]["size [m]"][2]]]
        resolutions_faces = np.array([settings["grid"]["resolution"],]*len(meshs_regular[id]["face_centers"]))
        faces_and_res_and_orient = np.concatenate([meshs_regular[id]["face_centers"], resolutions_faces.reshape(-1,1), np.ones_like(resolutions_faces.reshape(-1,1))*(-1)], axis=1)
        face_cell_ids_tmp = meshs_regular[id]["face_cell_ids"]

        # for each hp:
        print(f"num hps: {len(dps_hps_locs[id])}")
        for hp_loc, hp_temp, hp_rate in zip(dps_hps_locs[id], dps_hps_temps[id], dps_hps_rates[id]):
            # refine region around hp
            grid_and_resolutions, faces_and_res_and_orient, face_cell_ids_tmp = refine_region_acc_to_hp(grid_and_resolutions, faces_and_res_and_orient, face_cell_ids_tmp, orig_resolution, hp_loc, hp_temp, hp_rate, windows_properties_collected[id]["properties"], bounds, max_resolution=settings["grid"]["resolution"], min_resolution=min_resolution)

        mesh_refined = {"cell_centers": grid_and_resolutions[:,:-1], "cell_volumes": grid_and_resolutions[:,-1]**3, "face_areas": faces_and_res_and_orient[:,-2]**2, "face_cell_ids": face_cell_ids_tmp, "face_centers": faces_and_res_and_orient[:,:-2]}

        # store refined mesh: overwrite normal mesh
        store_mesh(output_run_dir, mesh_refined)

        meshs_refined.append(mesh_refined)
        
    return meshs_refined