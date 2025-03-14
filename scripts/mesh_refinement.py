import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
from tqdm import tqdm

from scripts.utils import timing
from scripts.mesh_generation_utils import store_mesh
from scripts.realistic_window.param_sampling import sample_median
from scripts.realistic_window.lahm.analytical_model_lahm import estimate_plume_shape_lahm
from scripts.main_helpers import groundwater_temp
from scripts.realistic_window.dupuit_thiem import drawdown_by_dupuit_thiem
from scripts.refinement2D_3Dv2 import Grid, refine_grid, target_resolution

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

def get_sichardt_lahm_distances(hp_cells:np.ndarray, hp_temps: np.ndarray, hp_rates:np.ndarray, subsurface_properties:np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    sichardt_dists = []
    lahm_w = []
    lahm_l = []

    for hp_id, hp_cell in enumerate(hp_cells):
        assert hp_cell[0] < subsurface_properties["hydraulic_conductivity"].shape[0], f"hp out of bounds x, {hp_cell},{subsurface_properties['hydraulic_conductivity'].shape}"
        assert hp_cell[1] < subsurface_properties["hydraulic_conductivity"].shape[1], f"hp out of bounds y, {hp_cell},{subsurface_properties['hydraulic_conductivity'].shape}"
        try: #if isinstance(subsurface_properties["hydraulic_conductivity"], np.ndarray):
            hydr_cond = sample_median(subsurface_properties["hydraulic_conductivity"],  [hp_cell[0],hp_cell[1]], [3,3]) 
            thickness = sample_median(subsurface_properties["thickness"],               [hp_cell[0],hp_cell[1]], [3,3])
            v_a = sample_median(subsurface_properties["darcy_velocity"],                [hp_cell[0],hp_cell[1]], [3,3])
        except:
            hydr_cond = subsurface_properties["hydraulic_conductivity"][hp_cell[0],hp_cell[1]]
            thickness = subsurface_properties["thickness"][hp_cell[0],hp_cell[1]]
            v_a = subsurface_properties["darcy_velocity"][hp_cell[0],hp_cell[1]]
    
        # Estimate the radius of the "Absenktrichter" with Sichardt around each well
        inner_radius = sichardt_distance(hydr_cond, thickness, hp_rates[hp_id])
        inner_radius = np.min([inner_radius, 50]) # limited to 20m

        # Estimate the plume shape parameters (1K isoline) with LAHM
        safety_factor = 1
        length_1K, width_1K = estimate_plume_shape_lahm(hp_temps[hp_id] - groundwater_temp(), hp_rates[hp_id], v_a, thickness)
        length_1K = np.max([length_1K * (1+safety_factor), 60]) # for debug/testing TODO
        width_1K = np.max([width_1K * (1+safety_factor), 10]) # for debug/testing TODO
        # print(f"downstream: {length_1K=}\nat half length: {width_1K=}")

        sichardt_dists.append(inner_radius)
        lahm_w.append(width_1K)
        lahm_l.append(length_1K)
    return sichardt_dists, lahm_w, lahm_l

# @timing
def refinement_all_dps(num_dp:int, grid_settings:Dict, dps_hps_locs:np.ndarray, dps_hps_temps:np.ndarray, dps_hps_rates:np.ndarray, windows_properties_collected: list[dict[str, np.ndarray]], orig_resolution: int, output_dir: Path) -> list[Dict[str, np.ndarray]]:

    max_cell_size = grid_settings["resolution"]
    # length, width, height = grid_settings["size [m]"][0] // max_resolution, grid_settings["size [m]"][1] // max_resolution, 1
    # if len(grid_settings["size [m]"]) > 2:
    #     height = grid_settings["size [m]"][2] // max_resolution
    length, width, height = grid_settings["size [m]"][0], grid_settings["size [m]"][1], max_cell_size
    if len(grid_settings["size [m]"]) > 2:
        height = grid_settings["size [m]"][2]

    meshs_refined = []
    dps_hps_ids = []
    for dp_id in tqdm(range(num_dp), desc="Runs"):
        output_run_dir = output_dir / f"RUN_{dp_id}"

        hp_locs = dps_hps_locs[dp_id]
        hp_locs = np.array([hp_locs[...,0], hp_locs[...,1], hp_locs[...,2]]).T

        sichardt_dists, lahm_w, lahm_l = get_sichardt_lahm_distances((hp_locs//orig_resolution).astype(int), dps_hps_temps[dp_id], dps_hps_rates[dp_id], windows_properties_collected[dp_id]["properties"])

        hps_dict = {
            "hp_centers": hp_locs,
            "sichardt_dists": sichardt_dists,
            "lahm_l": lahm_l,
            "lahm_w": lahm_w,
            "min_cell_size_hp": 0.2,
            "min_cell_size_plume": 1,
            }

        grid = Grid(res_x=length//max_cell_size, res_y=width//max_cell_size, res_z=height//max_cell_size, 
                    minx=0, maxx=length, miny=0, maxy=width, minz=0, maxz=height,
                    chunk_w=length//max_cell_size, chunk_h=width//max_cell_size, chunk_d=1, max_cell_size=max_cell_size)
        results, hps_ids = refine_grid(grid, max_depth=10, target_resolution=target_resolution, hps=hps_dict, visualize_grid=False)
        cell_centers, face_centers, face_cell_ids, face_areas, cell_volumes = results
        
        cell_centers = cell_centers[:, [0, 1, 2]]
        assert (np.array([face_centers[:,0], face_centers[:,1], face_centers[:,2]]).T == face_centers[:,[0,1,2]]).all(), "face centers transpose not correct"
        face_centers = face_centers[:, [0, 1, 2]]

        # TOODo ACTUAL : l, w, h ?? SOLL DAS SO? Wenn nciht, die dim in mesh_gen_boundaries tauschen
        assert np.max(cell_centers[:,0])+max_cell_size > length, f"cell centers not correct {np.max(cell_centers[:,0])} < {length}"
        assert np.max(cell_centers[:,1])+max_cell_size > width, f"cell centers not correct {np.max(cell_centers[:,1])} < {width}"
        assert np.max(cell_centers[:,2])+max_cell_size > height, f"cell centers not correct {np.max(cell_centers[:,2])} < {height}"
        assert np.max(face_centers[:,0])+max_cell_size > length, f"face centers not correct {np.max(face_centers[:,0])} < {length}"
        assert np.max(face_centers[:,1])+max_cell_size > width, f"face centers not correct {np.max(face_centers[:,1])} < {width}"
        assert np.max(face_centers[:,2])+max_cell_size > height, f"face centers not correct {np.max(face_centers[:,2])} < {height}"
        assert np.max(face_cell_ids) == len(cell_centers), f"face ids not correct; not+1? {np.max(face_cell_ids)} != {len(cell_centers)}"

        # store refined mesh
        print(f"number of refined cells: {len(cell_centers)}")
        mesh_refined = {"cell_centers": cell_centers, "cell_volumes": cell_volumes, "face_areas": face_areas, "face_cell_ids": face_cell_ids, "face_centers": face_centers}
        store_mesh(output_run_dir, mesh_refined)

        meshs_refined.append(mesh_refined)
        dps_hps_ids.append(hps_ids)
        
    return meshs_refined, dps_hps_ids

# @timing
# def calc_refined_grid_3D(leave_outs_and_res: List[Tuple[np.ndarray, float]], hp_cells: np.ndarray):
#     ids = None
#     cell_centerss = []
#     face_centerss = []
#     face_idss = []
#     face_areass = []
#     cell_volumess = []
#     # get last entry in leave_outs_and_res
#     _, last_res = leave_outs_and_res[-1]
#     for leave_out, res in leave_outs_and_res + [[None, last_res/2]]:
#         h,w,l = leave_out.shape if leave_out is not None else np.array(ids.shape) * 2
#         aspect_wl = w / l
#         aspect_hl = h / l
#         cell_centers, face_centers, face_ids, face_areas, cell_volumes, ids = get_grid_3D(
#             w=w,
#             l=l,
#             h=h,
#             minx=0,
#             maxx=aspect_wl, # w
#             miny=0,
#             maxy=1, #l, #
#             minz=0,
#             maxz=aspect_hl, #h
#             larger_indices=ids,
#             leave_out=leave_out,
#             res=res,
#         )
#         cell_centerss.append(cell_centers)
#         face_centerss.append(face_centers)
#         face_idss.append(face_ids)
#         face_areass.append(face_areas)
#         cell_volumess.append(cell_volumes)

    
#     # hp_cells to cell_ids from ids in finest level
#     hp_ids = np.zeros(hp_cells.shape[0])
#     for i in range(len(hp_ids)):
#         cell = hp_cells[i].astype(int)
#         assert cell[2] < ids.shape[0], f"hp out of bounds x, {cell}, {ids.shape}"
#         assert cell[1] < ids.shape[1], f"hp out of bounds y, {cell}, {ids.shape}"
#         assert cell[0] < ids.shape[2], f"hp out of bounds z, {cell}, {ids.shape}"
#         hp_ids[i] = ids[cell[2], cell[1], cell[0]]

#     cell_centers = np.concatenate(cell_centerss)
#     face_centers = np.concatenate(face_centerss)
#     face_ids = np.concatenate(face_idss)
#     face_areas = np.concatenate(face_areass)
#     cell_volumes = np.concatenate(cell_volumess)
#     cell_centers[:,0] /= aspect_wl
#     cell_centers[:,2] /= aspect_hl
#     face_centers[:,0] /= aspect_wl
#     face_centers[:,2] /= aspect_hl

#     # add 1 to all face ids, hp ids, because numbering starts at 1 in pflotran
#     face_ids += 1
#     hp_ids += 1

#     return cell_centers, face_centers, face_ids, face_areas, cell_volumes, hp_ids

# # @timing
# def get_grid_3D(w, l, h, minx, maxx, miny, maxy, minz, maxz, larger_indices=None, leave_out=None, res:float=1):

#     # to_draw is a mask that tells us which cells to define
#     to_draw = np.ones((h,w,l), dtype=bool)

#     # don't draw cells that will be filled with finer resolution
#     if leave_out is not None:
#         to_draw[leave_out] = False

#     # don't draw cells that are already in the coarser grid
#     if larger_indices is not None:
#         dont_redraw = larger_indices != -1
#         to_draw[::2, ::2, ::2][dont_redraw] = False
#         to_draw[1::2, ::2, ::2][dont_redraw] = False
#         to_draw[::2, 1::2, ::2][dont_redraw] = False
#         to_draw[1::2, 1::2, ::2][dont_redraw] = False
#         to_draw[::2, ::2, 1::2][dont_redraw] = False
#         to_draw[1::2, ::2, 1::2][dont_redraw] = False
#         to_draw[::2, 1::2, 1::2][dont_redraw] = False
#         to_draw[1::2, 1::2, 1::2][dont_redraw] = False


#     highest_index = np.max(larger_indices) if larger_indices is not None else -1
#     ids = -np.ones((h,w,l))
#     # fill the ids of all cells
#     ids[to_draw] = np.arange(to_draw.sum()) + highest_index + 1 

#     # fill in ids from cells of larger grid
#     if larger_indices is not None:
#         ids[::2, ::2, ::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[1::2, ::2, ::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[::2, 1::2, ::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[1::2, 1::2, ::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[::2, ::2, 1::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[1::2, ::2, 1::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[::2, 1::2, 1::2][dont_redraw] = larger_indices[dont_redraw]
#         ids[1::2, 1::2, 1::2][dont_redraw] = larger_indices[dont_redraw]

#     # remove all faces that are inside the same cell
#     horizontal_mask = ids[:, :, :-1] - ids[:, :, 1:] != 0
#     vertical_mask = ids[:, :-1] - ids[:, 1:] != 0
#     depth_mask = ids[:-1] - ids[1:] != 0
    
#     assert (maxx - minx) / w == (maxy - miny) / l == (maxz - minz) / h, "expects cubes not quader"
#     s = (maxx - minx) / w
#     cell_centers = np.stack(
#         np.meshgrid(
#             np.linspace(minx + s / 2, maxx - s / 2, w),
#             np.linspace(miny + s / 2, maxy - s / 2, l),
#             np.linspace(minz + s / 2, maxz - s / 2, h),
#         )
#     ).T
#     horizontal_faces_centers = np.stack(
#         np.meshgrid(
#             np.linspace(minx + s / 2, maxx - s / 2, w),
#             np.linspace(miny + s,     maxy - s,     l-1),
#             np.linspace(minz + s / 2, maxz - s / 2, h),
#         )
#     ).T

#     vertical_faces_centers = np.stack(
#         np.meshgrid(
#             np.linspace(minx + s,     maxx - s,     w-1),
#             np.linspace(miny + s / 2, maxy - s / 2, l),
#             np.linspace(minz + s / 2, maxz - s / 2, h),
#         )
#     ).T

#     depth_faces_centers = np.stack(
#         np.meshgrid(
#             np.linspace(minx + s / 2, maxx - s / 2, w),
#             np.linspace(miny + s / 2, maxy - s / 2, l),
#             np.linspace(minz + s,     maxz - s,     h - 1),
#         )
#     ).T
    
#     horizontal_face_ids = np.zeros(horizontal_faces_centers.shape, dtype=int)
#     horizontal_face_ids[..., 0] = ids[:, :, :-1]
#     horizontal_face_ids[..., 1] = ids[:, :, 1:]
#     horizontal_mask &= (
#         (horizontal_face_ids[..., 0] != -1)
#         & (horizontal_face_ids[..., 1] != -1)
#         & ~(
#             (horizontal_face_ids[..., 0] <= highest_index)
#             & (horizontal_face_ids[..., 1] <= highest_index)
#         )
#     )
#     horizontal_face_ids = horizontal_face_ids[horizontal_mask]
#     horizontal_faces_centers = horizontal_faces_centers[horizontal_mask]

#     vertical_face_ids = np.zeros(vertical_faces_centers.shape, dtype=int)
#     vertical_face_ids[..., 0] = ids[:, :-1, :]
#     vertical_face_ids[..., 1] = ids[:, 1:, :]
#     vertical_mask &= vertical_face_ids[..., 0] != -1
#     vertical_mask &= vertical_face_ids[..., 1] != -1
#     vertical_mask &= ~(
#         (vertical_face_ids[..., 0] <= highest_index)
#         & (vertical_face_ids[..., 1] <= highest_index)
#     )
#     vertical_face_ids = vertical_face_ids[vertical_mask]
#     vertical_faces_centers = vertical_faces_centers[vertical_mask]

#     depth_face_ids = np.zeros(depth_faces_centers.shape, dtype=int)
#     depth_face_ids[..., 0] = ids[:-1]
#     depth_face_ids[..., 1] = ids[1:]
#     depth_mask &= (
#         (depth_face_ids[..., 0] != -1)
#         & (depth_face_ids[..., 1] != -1)
#         & ~(
#             (depth_face_ids[..., 0] <= highest_index)
#             & (depth_face_ids[..., 1] <= highest_index)
#         )
#     )
#     depth_face_ids = depth_face_ids[depth_mask]
#     depth_faces_centers = depth_faces_centers[depth_mask]

#     cell_centers = cell_centers[to_draw]
#     cell_centers = cell_centers.reshape(-1, 3)
#     cell_volumes = np.full((h,w,l), res**3)
#     cell_volumes = cell_volumes[to_draw]
#     cell_volumes = cell_volumes.flatten()
#     face_centers = np.concatenate(
#         [horizontal_faces_centers.reshape(-1, 3), vertical_faces_centers.reshape(-1, 3), depth_faces_centers.reshape(-1, 3)]
#     )
#     face_ids = np.concatenate(
#         [horizontal_face_ids.reshape(-1, 3), vertical_face_ids.reshape(-1, 3), depth_face_ids.reshape(-1, 3)]
#     )
#     face_areas = np.full(face_centers.shape[0], res**2)
#     return cell_centers, face_centers, face_ids, face_areas, cell_volumes, ids

# # @timing
# def generate_refinement_masks(num_hp, width, length, height, res, hp_cells, sichardt_dists, lahm_w, lahm_l):
#     # transform sichardt etc to number of cells in highest resolution
#     sichardt_dists = np.array(sichardt_dists)/res
#     lahm_w = np.array(lahm_w)/res
#     lahm_l = np.array(lahm_l)/res

#     cells_to_refine_later_and_res = []
#     radii_hps = []
#     plume_w_hps = []
#     plume_l_hps = []
#     for id, hp in enumerate(range(num_hp)):
#         # for now: radii = list of hp with dict of level:radius
#         radii_hps.append(get_refinement_intervals(res, 0.1, sichardt_dists[hp]))
#         plume_w_hps.append(get_refinement_intervals(res, 1, lahm_w[hp]))
#         plume_l_hps.append(get_refinement_intervals(res, 1, lahm_l[hp]))
#     levels = len(radii_hps[0])
#     for i in range(levels):
#         coords = (
#             np.stack(np.meshgrid(
#                     np.linspace(0, width, width * 2**i, endpoint=False),
#                     np.linspace(0, length, length * 2**i, endpoint=False),
#                     np.linspace(0, height, height * 2**i, endpoint=False),
#                     )).T)

#         mask = np.zeros(coords.shape[:3], dtype=bool) # mask of n_cells_h,_w,_l in current resolution
#         for hp_id, hp_coords in enumerate(hp_cells):
#             hp_coords = [hp_coords[1], hp_coords[0], hp_coords[2]]
#             radius = radii_hps[hp_id][i]
#             mask += (coords[..., 0]-hp_coords[0]) ** 2 + (coords[..., 1]-hp_coords[1]) ** 2 + (coords[..., 2]-hp_coords[2]) ** 2 < (radius + 0.75/(2**i)) ** 2 # +0.75 so that no cells with more than 1 difference in resolution steps are adjacent
#             if i in plume_l_hps[hp_id].keys():
#                 diff_l = coords[...,1] - hp_coords[1] #+ 0.5/(2**i)
#                 constraint_l = plume_l_hps[hp_id][i]
#                 diff_w = np.abs(coords[..., 0] - hp_coords[0])
#                 constraint_w =  plume_w_hps[hp_id][i] / 2 #+ 0.5 / (2 ** i)
#                 diff_h = np.abs(coords[..., 2] - hp_coords[2]) 
#                 constraint_h = constraint_w
#                 mask += np.logical_and(np.logical_and(diff_w < constraint_w, diff_h < constraint_h), np.logical_and(0 < diff_l, diff_l < constraint_l))
#         cells_to_refine_later_and_res.append([mask, res / 2**i])

#     # hp_locs_finest = np.array([hp_locs[:,1], hp_locs[:,0], hp_locs[:,2]]).T * 2**levels
#     hp_locs_finest = hp_cells * 2**levels
#     return cells_to_refine_later_and_res, hp_locs_finest

def get_refinement_intervals(max_resolution: float, min_resolution: float, inner_distance: float, decrease_factor: float = 1.0) -> dict:
    n_refinement_steps = int(np.log2(max_resolution / min_resolution)) - 1
    refinements = {}
    for i in range(n_refinement_steps + 1):
        tmp = i / n_refinement_steps if n_refinement_steps > 0 else 1
        max_distance = inner_distance * (1 + decrease_factor * (1 - tmp))
        refinements[i] = np.round(max_distance, 1)
    return refinements
