import numpy as np
import h5py
import pathlib
from typing import Dict, Tuple
import logging
from tqdm import tqdm

from scripts.mesh_refinement_utils import *
from scripts.mesh_generation_utils import *

# def calc_refined_cell_centers(old_cell_center, curr_resolution, bounds:List):
#     new_cell_centers = []
#     offset_list = [[-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0]]
#     for offset in offset_list:
#         new_pos = old_cell_center + np.array(offset) * curr_resolution / 2
#         if new_pos[0] < bounds[0][0] or new_pos[0] > bounds[0][1] or new_pos[1] < bounds[1][0] or new_pos[1] > bounds[1][1]:
#             continue
#         new_cell_centers.append([*new_pos, curr_resolution])
#     new_cell_centers = np.array(new_cell_centers)
#     return new_cell_centers

# def refine_region_step(grid_and_resolutions, cells_to_handle:List[np.array], bounds:List, goal_resolution:float=0.1):
#     for curr_cell_and_resolution in cells_to_handle:
#         # refine cell
#         curr_resolution = curr_cell_and_resolution[-1] / 2
#         if curr_resolution >= goal_resolution:
#             curr_cell_id = loc_to_id(grid_and_resolutions[:,:-1], curr_cell_and_resolution[:-1])
#             new_cell_centers = calc_refined_cell_centers(curr_cell_and_resolution[:-1], curr_resolution, bounds)
#             # add new cell centers to grid and remove old cell center
#             grid_and_resolutions = np.delete(grid_and_resolutions, curr_cell_id-1, 0)
#             grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_centers])

#     return grid_and_resolutions

# def refine_region(grid_and_resolutions: np.array, hp: np.array, settings, bounds, goal_resolution:float=0.1):
#     refinements = calc_refinement_steps(hp, settings["grid"]["resolution"], goal_resolution, settings, decrease_factor=1)
#     # print(refinements)
    
#     for goal_resolution, curr_radius in tqdm(refinements["radius"].items(), desc="Refinement steps"):
#         cells_to_refine = get_circular_region(hp, grid_and_resolutions, curr_radius)
#         if goal_resolution in refinements["plume_length"]:
#             cells_to_refine += get_rectangular_region(hp, grid_and_resolutions, refinements["plume_length"][goal_resolution], refinements["plume_width"][goal_resolution])
#         # make unique
#         cells_to_refine = list(set([tuple(row) for row in cells_to_refine]))
#         cells_to_refine = [np.array(row) for row in cells_to_refine]
        
#         # refine cells in region
#         grid_and_resolutions = refine_region_step(grid_and_resolutions, cells_to_refine, bounds, goal_resolution)
#         # cells_to_refine_array = np.array(cells_to_refine)
#         # plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, np.concatenate([cells_to_refine_array[:,:-1], hp.reshape(1,-1)]))
#     # plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, hp.reshape(1,-1), factor=0.1)
#     return grid_and_resolutions

# # def refine_cell_acc_to_hps(grid_and_resolutions, hps, settings, min_resolution:float=0.1):
# #     bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]
# #     for curr_hp_loc in hps:
# #     # refine cell around hp
# #         curr_resolution = id_to_loc(grid_and_resolutions, loc_to_id(grid_and_resolutions[:,:-1], curr_hp_loc))[-1]
# #         while curr_resolution > min_resolution:
# #             # TODO achtung z ist falsch!!
# #             cell_id_hp = loc_to_id(grid_and_resolutions[:,:-1], curr_hp_loc)
# #             # TODO next loc variiert, wenn diese schleife mehrmals durchlaufen wird (also für nächste HP)
# #             logging.info(f"{cell_id_hp=}")
# #             old_cell_center = id_to_loc(grid_and_resolutions, cell_id_hp)
# #             if old_cell_center[-1] <= curr_resolution:
# #                 logging.warning("cell is already refined")
# #                 curr_resolution /= 2
# #                 continue
# #             new_cell_centers = refine_cell(old_cell_center[:-1], curr_resolution, bounds=bounds)
# #             logging.info(f"{new_cell_centers=}")
# #             # add new cell centers to grid and remove old cell center
# #             logging.info(f"to delete: {cell_id_hp-1=}")
# #             grid_and_resolutions = np.delete(grid_and_resolutions, cell_id_hp-1, 0)
# #             grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_centers])

# #             curr_resolution /= 2
# #     return grid_and_resolutions

# # def refine_cell_centers_and_volumes_acc_to_hps(cell_centers:np.ndarray, hps:np.ndarray, settings:Dict):
# #     '''for 1 dp: 1 mesh and 1 set of heat pumps'''
# #     # refine mesh + store information:
# #     n_cells = calc_n_cells_array(settings)
# #     resolutions = np.array([settings["grid"]["resolution"],]*np.prod(n_cells))
# #     ## cell centers
# #     grid_and_resolutions = np.concatenate([cell_centers, resolutions.reshape(-1, 1)], axis=1)
# #     refined_grid_and_resolutions = refine_cell_acc_to_hps(grid_and_resolutions, hps, settings)
# #     refined_cell_centers = refined_grid_and_resolutions[:,:-1]
# #     ## cell volumes
# #     refined_cell_volumes = refined_grid_and_resolutions[:,-1]**3
# #     # TODO store information
# #     return refined_cell_centers, refined_cell_volumes


# def refine_regions_acc_to_hps(num_dp:int, settings:Dict, grids:np.array, dps_hps_locs:np.array):
#     # logging.getLogger().setLevel(logging.ERROR)
#     refined_cell_centers = []
#     refined_cell_volumes = []

#     # for each dp:
#     for id in range(num_dp):
#         # get cell centers in region
#         resolutions = np.array([settings["grid"]["resolution"],]*np.prod(calc_n_cells_array(settings)))
#         grid_and_resolutions = np.concatenate([grids[id], resolutions.reshape(-1, 1)], axis=1)
#         if logging.getLogger().getEffectiveLevel() <= logging.WARNING:
#             plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, dps_hps_locs[id], factor=0.1)
#         bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]

#         # for each hp:
#         for hp in dps_hps_locs[id]:
#             # refine region around hp
#             grid_and_resolutions = refine_region(grid_and_resolutions, hp, settings, bounds)

#         if logging.getLogger().getEffectiveLevel() <= logging.WARNING:
#             plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, dps_hps_locs[id], factor=0.1)

#         refined_cell_centers.append(grid_and_resolutions[:,:-1])
#         ## cell volumes
#         refined_cell_volumes.append(grid_and_resolutions[:,-1]**3)
#         # TODO store information
        
#     return refined_cell_centers, refined_cell_volumes


# def refine_mesh(path_to_output: pathlib.Path, settings: Dict, positions_hps: np.ndarray):
#     ...
#     # get mesh

#     # refine mesh + store information:
#     ## cell centers + cell volumes
#     refined_cell_centers, refined_cell_volumes = refine_regions_acc_to_hps(num_dp, settings, grids, dps_hps_locs)

#     ## face areas
#     ## face cell ids
#     ## face centers
#     ## correct face ids


#     # TODO refine boundaries?

def calc_refined_face_centers(old_cell_and_res:np.ndarray, face_cell_ids:np.ndarray, faces_and_res_and_orient:np.ndarray, grid_and_res:np.ndarray, new_cell_centers_and_ress:np.ndarray):
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

def do_refinements(grid_and_resolutions: np.ndarray, faces_and_res_and_orient:np.ndarray, face_cell_ids:np.ndarray, hp: np.ndarray, settings, bounds, goal_resolution:float=0.1):
    refinement_steps = calc_refinement_steps(hp, settings["grid"]["resolution"], goal_resolution, settings, decrease_factor=1)
    for goal_resolution, curr_radius in tqdm(refinement_steps["radius"].items(), desc="Refinement steps"):
        cells_to_refine_and_res = calc_cells_to_refine(grid_and_resolutions, hp, goal_resolution, refinement_steps, curr_radius)

        # refine cells in region
        for id_and_face_and_res_and_orient in range(len(cells_to_refine_and_res)):
            # refine cell
            curr_resolution = cells_to_refine_and_res[id_and_face_and_res_and_orient][-1]
            if curr_resolution / 2 >= goal_resolution:
                curr_cell_id = loc_to_id(grid_and_resolutions[:,:-1], cells_to_refine_and_res[id_and_face_and_res_and_orient][:-1])
                new_cell_and_res_tmp = calc_refined_cell_centers(cells_to_refine_and_res[id_and_face_and_res_and_orient][:-1], curr_resolution / 2, bounds)
                # get old face centers, calc new face centers
                new_outer_face_centers_and_res_and_orient, old_face_ids, already_refined_faces = calc_refined_face_centers(cells_to_refine_and_res[id_and_face_and_res_and_orient], face_cell_ids, faces_and_res_and_orient, grid_and_resolutions, new_cell_and_res_tmp)
                new_inner_face_centers_and_res_and_orient = calc_inner_face_centers(cells_to_refine_and_res[id_and_face_and_res_and_orient,:-1], new_cell_and_res_tmp)
                try:
                    new_face_centers_and_res_and_orient_tmp = np.concatenate([new_inner_face_centers_and_res_and_orient, new_outer_face_centers_and_res_and_orient])
                except:
                    new_face_centers_and_res_and_orient_tmp = new_inner_face_centers_and_res_and_orient
                    print("no outer faces")

                ## overwrite and append: cells: centers, volumes; faces: centers, areas, cell ids
                # old cell ids: curr_cell_id; # new cells: new_cell_centers_tmp
                grid_and_resolutions[curr_cell_id-1] = new_cell_and_res_tmp[0]
                grid_and_resolutions = np.concatenate([grid_and_resolutions, new_cell_and_res_tmp[1:]])

                # old face ids: old_face_ids; # new faces: new_face_centers_tmp, new_face_cell_ids_tmp
                # print("here", new_face_centers_and_res_and_orient_tmp)
                new_face_cell_ids_tmp = calc_face_cell_ids(new_face_centers_and_res_and_orient_tmp, grid_and_resolutions)

                collect_already_faces_cell_ids = []
                if len(already_refined_faces) > 0:
                    print("update already refined face")
                    print("prior", already_refined_faces)
                    neighbors = calc_face_cell_ids(already_refined_faces[:,1:], grid_and_resolutions)
                    for neigh, face in zip(neighbors, already_refined_faces):
                        face_cell_ids[int(face[0])] = neigh
                        collect_already_faces_cell_ids.append(neigh)
                    print("post", face_cell_ids[int(face[0])])
                collect_already_faces_cell_ids = np.array(collect_already_faces_cell_ids)

                # pos of refined_face in faces_and_resolutions
                for id, old_f in enumerate(old_face_ids):
                    faces_and_res_and_orient[old_f] = new_face_centers_and_res_and_orient_tmp[id]
                    # update cell ids in faces, face cell ids genauso wie face centers machen
                    face_cell_ids[old_f] = new_face_cell_ids_tmp[id]
                faces_and_res_and_orient = np.concatenate([faces_and_res_and_orient, new_face_centers_and_res_and_orient_tmp[len(old_face_ids):]])
                face_cell_ids = np.concatenate([face_cell_ids, new_face_cell_ids_tmp[len(old_face_ids):]])
            # break
        plt.figure(figsize=(20,10))
        plt.subplot(121)
        # plt.plot(cells_to_refine_and_res[:,0], cells_to_refine_and_res[:,1], "x")
        plt.scatter(grid_and_resolutions[:,0], grid_and_resolutions[:,1], c=range(len(grid_and_resolutions[:,:-1])))
        # plt.plot(hp[0], hp[1], "rx")
        for cell_id, pos in enumerate(grid_and_resolutions): #cell_positions, cell_ids):
            plt.text(pos[0], pos[1], str(cell_id+1), fontsize=12, ha='center', va='center', color='blue')

        plt.grid()
        # plt.colorbar()
        plt.subplot(122)
        plt.plot(grid_and_resolutions[:,0], grid_and_resolutions[:,1], "gx")
        plt.scatter(faces_and_res_and_orient[:,0], faces_and_res_and_orient[:,1], c=range(len(faces_and_res_and_orient[:,:-1])))
        if len(collect_already_faces_cell_ids) > 0:
            tmpi_cells = np.concatenate((new_face_cell_ids_tmp, collect_already_faces_cell_ids))
            tmpi_centers = np.concatenate((new_face_centers_and_res_and_orient_tmp, already_refined_faces[:,1:]))
        else:
            tmpi_cells = new_face_cell_ids_tmp
            tmpi_centers = new_face_centers_and_res_and_orient_tmp
        for line, face_cell_id in enumerate(tmpi_cells):
            tmp = np.array([id_to_loc(grid_and_resolutions[:,:-1], face_cell_id[0])[:2], tmpi_centers[line][:2], id_to_loc(grid_and_resolutions[:,:-1], face_cell_id[1])[:2]])
            plt.plot(tmp[:,0], tmp[:,1], "r-o")
        # try:
        #     plt.plot(grid_and_resolutions[66,0], grid_and_resolutions[66,1], "ro")
        #     plt.plot(grid_and_resolutions[67,0], grid_and_resolutions[67,1], "ro")
        #     plt.plot(grid_and_resolutions[68,0], grid_and_resolutions[68,1], "ro")
        # except:
        #     print(grid_and_resolutions.shape)
        plt.colorbar()
        plt.grid()
        plt.show()

        # for line, face_cell_id in enumerate(face_cell_ids):
        #     print(face_cell_id, faces_and_res_and_orient[line], "cell1", id_to_loc(grid_and_resolutions[:,:-1], face_cell_id[0]), "cell2", id_to_loc(grid_and_resolutions[:,:-1], face_cell_id[1]))
        # break


    return grid_and_resolutions, faces_and_res_and_orient, face_cell_ids


def refine_regions_acc_to_hps(num_dp:int, settings:Dict, grids:np.ndarray, face_centers:np.ndarray, face_cell_ids:np.ndarray, dps_hps_locs:np.ndarray):
    refined_cell_centers = []
    refined_cell_volumes = []

    # for each dp:
    for id in range(num_dp):
        # get cell centers in region
        resolutions_cells = np.array([settings["grid"]["resolution"],]*len(grids[id]))
        grid_and_resolutions = np.concatenate([grids[id], resolutions_cells.reshape(-1, 1)], axis=1)
        bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]
        resolutions_faces = np.array([settings["grid"]["resolution"],]*len(face_centers[id]))
        faces_and_res_and_orient = np.concatenate([face_centers[id], resolutions_faces.reshape(-1,1), np.ones_like(resolutions_faces.reshape(-1,1))*(-1)], axis=1)
        face_cell_ids_tmp = face_cell_ids[id]
        # print(faces_and_resolutions[:10], faces_and_resolutions.shape)
        # for each hp:
        id = 0
        for hp in dps_hps_locs[id]:
            # refine region around hp
            grid_and_resolutions, faces_and_res_and_orient, face_cell_ids_tmp = do_refinements(grid_and_resolutions, faces_and_res_and_orient, face_cell_ids_tmp, hp, settings, bounds)
            id += 1
            if id > 0:
                break

        # TODO 
        refined_cell_centers.append(grid_and_resolutions[:,:-1])
        ## cell volumes
        refined_cell_volumes.append(grid_and_resolutions[:,-1]**3)
        break
        
    return refined_cell_centers, refined_cell_volumes


# out, _  = create_regular_grid(settings, pathlib.Path.cwd())
# grids_global = np.array([out["Domain/Cells/Centers"],]*num_dp)
# face_areas = np.array([out["Domain/Connections/Areas"],]*num_dp)
# face_cell_ids_global = np.array([out["Domain/Connections/Cell Ids"],]*num_dp)
# face_centers_global = np.array([out["Domain/Connections/Centers"],]*num_dp)
# out.close()
# dps_hps_locs_global = np.array([[[31.27825912, 10.23414779,  1.        ]]])

# refined_cell_centers, refined_cell_volumes = refine_regions_acc_to_hps(num_dp, settings, grids_global, face_centers_global, face_cell_ids_global, dps_hps_locs_global)
