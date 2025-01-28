import numpy as np
import pathlib
from typing import Dict, Union
from scripts.utils import timing
from h5py import File
import logging

from scripts.utils import save_yaml
from scripts.realistic_window.load_and_align_tiffs import load_properties_after_R_prep
from scripts.realistic_window.interpolate import interpolate_windows
from scripts.realistic_window.estimate_box_dims import make_window_shape_and_pump_params, estimate_box_rotation, calc_box_height_from_TOK_n_GWGL
from scripts.realistic_window.cut_and_rotate_box import cut_out_values, calc_rotated_box, check_validity_window
from scripts.realistic_window.boundary_conditions import get_bcs_values, save_bcs
from scripts.realistic_window.param_sampling import get_start_positions

logging.basicConfig(level=logging.WARNING)

@timing
def realistic_hydrogeological_params_boxes_and_hp_params(settings:Dict, num_dp:int, temp_default:float, rate_default:float):
    # 1. load full maps # properties_full: 1px (=1cell) = 20m (=orig_resolution)
    orig_data_path = pathlib.Path("/home/pelzerja/pelzerja/test_nn/dataset_generation_laptop/Phd_simulation_groundtruth/input_files/real_Munich_input_fields/prepared_with_R")
    properties_full, orig_resolution = load_properties_after_R_prep(data_path=orig_data_path) 

    # 2. get all start points, randomized (NOT checked for validity yet) or manual start point, e.g.  # start_positions = [[2100, 2300]]
    start_positions_in_orig_cells = get_start_positions(properties_full["dtw"], settings["general"])
    logging.info(f"Number of start positions:{len(start_positions_in_orig_cells)}")

    windows_collected = []
    pumps_collected = []
    n_valid_windows = 0
    # while not enough windows:
    for i, start_pos in enumerate(start_positions_in_orig_cells): #[[1883, 1241]][[2630, 2644],[2644,2630]]): #
        try:
            # 3. estimate window_shape [in cells] or load / manually, e.g. np.array([int(12800/20), int(12800/20/2)])
            window_shape, pump_params = make_window_shape_and_pump_params(settings, orig_resolution, properties_full, start_pos, temp_default, rate_default)
            settings["grid"]["size [m]"] = (window_shape*orig_resolution).tolist()

            # 4. define rotation angle
            #TODO check, dass 100% aligned
            rotation_angle_degree = estimate_box_rotation(properties_full["darcy_dir"], start_pos, window_shape)
            logging.info(f"Estimated rotation: {rotation_angle_degree} [°]")

            # 5. coords of rotated window
            window_rotated_cells = calc_rotated_box(start_pos, window_shape, rotation_angle_degree)
        except Exception as e:
            logging.info(f"{e} WARNING in run {i}, e.g. NaN error encountered")
            continue
        # 6. check window for nans
        valid = check_validity_window(properties_full["dtw"], window_rotated_cells)

        # if valid window..., else restart with next start_pos
        if valid:
            logging.info(f"Valid window for start {start_pos} in round {i}, called RUN_{n_valid_windows}")

            # 7. cut out window from full maps
            window_properties = {}
            for name, value in properties_full.items():
                window_properties[name] = cut_out_values(value, window_rotated_cells)
            window_properties["permeability"] = window_properties["hydraulic_conductivity"]/7.5E06

            # 8. calc box height (max thickness)
            window_height_in_meters = calc_box_height_from_TOK_n_GWGL(window_properties["tok"], window_properties["gwgl"])
            logging.info(f"simulation box height: {window_height_in_meters} meters")

            # removed mesh specific code + mesh generation
            windows_collected.append({"properties": window_properties, "shape": window_shape, "box_height": window_height_in_meters, "start_pos": start_pos, "rotation_angle": rotation_angle_degree})
            pumps_collected.append(pump_params)

            n_valid_windows += 1
        else:
            logging.info(f"invalid window for start {start_pos} in run {i}")
            continue

        if n_valid_windows >= num_dp:
            return windows_collected, pumps_collected, orig_resolution, settings

    logging.info(n_valid_windows, " valid windows found within", i+1, "tries")
    if n_valid_windows < num_dp:
        logging.error(f"Not enough windows found. Only {n_valid_windows} found.")

    return windows_collected, pumps_collected, orig_resolution, settings

def interpolate_and_store_windows_and_bcs(destination_path:pathlib.Path, window_collected: dict[str, Union[dict, np.ndarray, float]], mesh_refined: dict[str, np.ndarray], bcs_cell_ids: Dict[str, np.ndarray], orig_resolution:float):

    # 10. interpolate cut out data to mesh (i.e. new resolution), based on coords (in cells of orig resolution)
    # TODO add 3rd dim
    window_desti_values = interpolate_windows(orig_resolution, window_collected["properties"], mesh_refined["cell_centers"][:,:2]) # [m] TODO 0:2 if 2D , sonst 0:3?

    # 11. calc and store BCs (hydraulic head) (convention: north=inflow, south=outflow, west=right, east=left)
    bcs_hh = get_bcs_values(window_desti_values["tok"], window_desti_values["gwgl"], bcs_cell_ids, window_collected["shape"] * orig_resolution)
    save_bcs(destination_path, bcs_hh)
    
    # 12. store interpolated data and unique params to RUN-dir
    save_yaml({"start position [m]": [window_collected["start_pos"][0]*orig_resolution, window_collected["start_pos"][1]*orig_resolution], "rotation angle [°]": float(window_collected["rotation_angle"]), "orig resolution [m]": orig_resolution}, destination_path, "realistic_params", {"allow_unicode":True})
    for key, field in window_desti_values.items():
        if key in ["permeability", "drawdown", "hydraulic_gradient", "dtw"]:
            store_hdf5_field(destination_path/f"{key}.h5", len(mesh_refined["cell_centers"]), field, vary_property=key) # TODO check dass richtig herum (removed order=F)/ eh anders auslesen


def store_hdf5_field(filename, n_cells, values, vary_property:str = "permeability"):

    with File(filename, mode="w") as h5file:
        h5file.create_dataset("Cell Ids", data=np.arange(1,n_cells+1).astype(int))
        h5file.create_dataset(vary_property, data=values, dtype="f8")

    h5file.close()