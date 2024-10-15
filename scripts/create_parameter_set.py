import matplotlib.pyplot as plt
import argparse
import numpy as np
import pathlib
import shutil
from typing import Dict
from scripts.utils import timing
from h5py import File

from scripts.make_general_settings import load_yaml, save_yaml
from scripts.realistic_window.load_and_align_tiffs import load_properties_after_R_prep
from scripts.realistic_window.interpolate import interpolate_windows
from scripts.realistic_window.estimate_box_dims import make_window_shape, estimate_box_rotation, calc_box_height_from_TOK_n_GWGL
from scripts.realistic_window.cut_and_rotate_box import cut_out_values, calc_rotated_box, check_validity_window
from scripts.realistic_window.boundary_conditions import cut_bcs_hh, save_bcs
from scripts.realistic_window.param_sampling import get_start_positions
from scripts.create_grid_unstructured import create_mesh_files


@timing
def make_realistic_hydrogeological_parameter_windows(destination_path:pathlib.Path, settings:Dict, number_of_simulations:int, temp_default:float, rate_default:float):
    # 1. load full maps # properties_full: 1px (=1cell) = 20m (=orig_resolution)
    orig_data_path = pathlib.Path("/home/pelzerja/pelzerja/test_nn/dataset_generation_laptop/Phd_simulation_groundtruth/input_files/real_Munich_input_fields/prepared_with_R")
    properties_full, orig_resolution = load_properties_after_R_prep(data_path=orig_data_path) 

    # 2. get all start points, randomized (NOT checked for validity yet) or manual start point, e.g.  # start_positions = [[2100, 2300]]
    start_positions_in_orig_cells = get_start_positions(properties_full["dtw"], settings["general"])
    print("Number of start positions:", len(start_positions_in_orig_cells))

    valid_start_ids = []
    current_number_valid_windows = 0
    # while not enough windows:
    for i, start_pos in enumerate(start_positions_in_orig_cells): #[[1883, 1241]]
        try:
            # 3. estimate window_shape [in cells] or load / manually, e.g. np.array([int(12800/20), int(12800/20/2)])
            window_shape = make_window_shape(settings, orig_resolution, properties_full, start_pos, temp_default, rate_default)
            settings["grid"]["size [m]"] = (window_shape*orig_resolution).tolist()

            # 4. define rotation angle
            #TODO check, dass 100% aligned
            rotation_angle_degree = estimate_box_rotation(properties_full["darcy_dir"], start_pos, window_shape)
            print(f"Estimated rotation: {rotation_angle_degree} [°]")

            # 5. coords of rotated window
            window_rotated_cells = calc_rotated_box(start_pos, window_shape, rotation_angle_degree)
        except Exception as e:
            print(f"{e} WARNING in run {i}, e.g. NaN error encountered")
            continue
        # 6. check window for nans
        valid = check_validity_window(properties_full["dtw"], window_rotated_cells)

        # if valid window..., else restart with next start_pos
        if valid:
            print(f"Valid window for start {start_pos} in round {i}, called RUN_{current_number_valid_windows}")

            filename = destination_path / f"RUN_{current_number_valid_windows}"
            filename.mkdir(parents=True, exist_ok=True)
            desti_resolution = settings["grid"]["resolution"]

            # 7. cut out window from full maps
            window_properties = {}
            for name, value in properties_full.items():
                window_properties[name] = cut_out_values(value, window_rotated_cells)
            window_properties["permeability"] = window_properties["hydraulic_conductivity"]/7.5E06

            # 8. calc box height (max thickness)
            window_height_in_meters = calc_box_height_from_TOK_n_GWGL(window_properties["tok"], window_properties["gwgl"])
            print(f"simulation box height: {window_height_in_meters} meters")

            # 9. generate mesh (height added to ncells, NOT to window_shape)
            # TODO include height
            ncells = window_shape[...] * orig_resolution / desti_resolution
            if False:
                ncells = np.append(ncells, np.ceil(window_height_in_meters / desti_resolution))
            else:
                ncells = np.append(ncells, 1)
            ncells = ncells.astype(int)
            if len(settings["grid"]["size [m]"]) == 2:
                settings["grid"]["size [m]"].append(int(ncells[2] * desti_resolution))
            else:
                settings["grid"]["size [m]"][2] = int(ncells[2] * desti_resolution)
            save_yaml(settings, filename)
            cells = create_mesh_files(filename, settings) # cells: np.ndarray of [cell id, x[m], y[m], z[m]]

            # 10. interpolate cut out data to mesh (i.e. new resolution), based on coords (in cells of orig resolution)
            # TODO add 3rd dim
            window_desti_values = interpolate_windows(orig_resolution, window_properties, cells["all"])

            # 11. calc and store BCs (hydraulic head) (convention: north=inflow, south=outflow, west=right, east=left)
            bcs_hh = cut_bcs_hh(window_desti_values["tok"], window_desti_values["gwgl"], cells, desti_resolution, ncells[1] * desti_resolution)
            save_bcs(filename, bcs_hh)
            
            # 12. store interpolated data and unique params to RUN-dir
            save_yaml({"start position [m]": [start_pos[0]*orig_resolution, start_pos[1]*orig_resolution], "rotation angle [°]": float(rotation_angle_degree), "orig resolution [m]": orig_resolution}, filename, "realistic_params", {"allow_unicode":True})
            for key, field in window_desti_values.items():
                store_hdf5_field(filename/f"{key}.h5", cells["all"], field, vary_property=key)

            current_number_valid_windows += 1
            valid_start_ids.append(start_pos)
        else:
            print(f"invalid window for start {start_pos} in run {i}")
            continue

        if current_number_valid_windows >= number_of_simulations:
            break

    print(current_number_valid_windows, " valid windows found within", i+1, "tries")
    if current_number_valid_windows < number_of_simulations:
        print("Not enough windows found. Only", current_number_valid_windows, "found.")


def store_hdf5_field(filename, cells, data, vary_property:str = "permeability"):
    data_flatten = data.reshape(len(cells[:,0]), order="F")

    with File(filename, mode="w") as h5file:
        h5file.create_dataset("Cell Ids", data=cells[:,0].astype(int))
        h5file.create_dataset(vary_property, data=data_flatten)

    h5file.close()