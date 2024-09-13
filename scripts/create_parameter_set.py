import matplotlib.pyplot as plt
import argparse
import numpy as np
import pathlib
import shutil
import yaml

from scripts.calc_loc_hp_variation_2d import (calc_loc_hp_variation_2d,
                                              write_hp_additional_files)
from scripts.calc_p_and_K import calc_pressure_and_perm_values
from scripts.calc_hp_parameter_variation import calc_injection_variation
from scripts.create_grid_unstructured import create_all_grid_files
from scripts.create_varying_field import create_vary_fields
from scripts.make_general_settings import load_yaml, save_yaml

from scripts.realistic_window.load_and_align_tiffs import load_properties_after_R_prep, interpolate_properties
from scripts.realistic_window.estimate_box_dims import make_window_shape, estimate_box_rotation, calc_box_height_from_TOK_n_GWGL
from scripts.realistic_window.cut_and_rotate_box import cut_out_values, calc_rotated_box, check_validity_window, cut_bcs_hh, define_cell_mesh
from scripts.realistic_window.param_sampling import get_start_positions
from scripts.create_varying_field import save_vary_field

def make_parameter_set(args, output_dataset_dir):
    settings = prepare_settings(args, output_dataset_dir)

    if not args.realistic:
        # calc pressure and perm values
        pressures, perms = calc_pressure_and_perm_values(args.num_dp, output_dataset_dir / "inputs", args.vary_perm, vary_pressure_field=args.vary_pressure, benchmark_bool=args.benchmark, only_vary_distribution=args.only_vary_distribution,)
        settings["pressure"] = {}
        settings["pressure"]["min"] = float(np.min(pressures))
        settings["pressure"]["max"] = float(np.max(pressures))

        # if settings["permeability"]["case"] == "realistic_window": 
        #     assert args.vary_perm == True, "vary_perm not combinable with realistic_window"
        #     perms = create_realistic_window(settings, args.num_dp, output_dataset_dir / "inputs")
        #     # and overwrite min, max perm values

        settings["permeability"]["min"] = float(np.min(perms))
        settings["permeability"]["max"] = float(np.max(perms))
        save_yaml(settings, output_dataset_dir / "inputs")

        if not settings["permeability"]["case"] == "realistic_window":
            if args.vary_perm:
                create_vary_fields(args.num_dp, output_dataset_dir / "inputs", settings, min_max=perms)
            if args.vary_pressure:
                create_vary_fields(args.num_dp, output_dataset_dir / "inputs", settings, min_max=pressures, vary_property="pressure")
            if args.vary_inflow:
                calc_injection_variation(args.num_dp, output_dataset_dir / "inputs", args.num_hps)

    # make grid files
    path_interim_pflotran_files = output_dataset_dir / "pflotran_inputs"
    path_interim_pflotran_files.mkdir(parents=True, exist_ok=True)
    settings = create_all_grid_files(settings, path_to_output=path_interim_pflotran_files,) # TODO

    write_hp_additional_files(output_dataset_dir / "pflotran_inputs", args.num_hps) # region_hps, strata_hps, condition_hps.txt

    # calc hp locations (if vary hp, then vary all hp locations)
    if args.vary_hp:
        (output_dataset_dir / "inputs" / "hps").mkdir(parents=True, exist_ok=True)
        calc_loc_hp_variation_2d(args.num_dp, output_dataset_dir / "inputs" / "hps", args.num_hps, settings)

    return settings

def prepare_settings(args, output_dataset_dir):
    # 0. preparation
    # copy settings file
    settings_name = f"settings_{args.dims}D_window_{args.domain_category}"
    shutil.copy(f"input_files/{settings_name}.yaml", output_dataset_dir / "inputs" / "settings.yaml", )  
    # get settings
    settings = load_yaml(output_dataset_dir / "inputs")
    return settings



    # make grid files
    path_interim_pflotran_files = output_dataset_dir / "pflotran_inputs"
    path_interim_pflotran_files.mkdir(parents=True, exist_ok=True)
    settings = create_all_grid_files(settings, path_to_output=path_interim_pflotran_files,) # TODO

    write_hp_additional_files(output_dataset_dir / "pflotran_inputs", args.num_hps) # region_hps, strata_hps, condition_hps.txt

    # calc hp locations (if vary hp, then vary all hp locations)
    if args.vary_hp:
        (output_dataset_dir / "inputs" / "hps").mkdir(parents=True, exist_ok=True)
        calc_loc_hp_variation_2d(args.num_dp, output_dataset_dir / "inputs" / "hps", args.num_hps, settings)

    # calc pressure and perm values
    pressures, perms = calc_pressure_and_perm_values(args.num_dp, output_dataset_dir / "inputs", args.vary_perm, vary_pressure_field=args.vary_pressure, benchmark_bool=args.benchmark, only_vary_distribution=args.only_vary_distribution,)
    settings["pressure"] = {}
    settings["pressure"]["min"] = float(np.min(pressures))
    settings["pressure"]["max"] = float(np.max(pressures))

    # if settings["permeability"]["case"] == "realistic_window": 
    #     assert args.vary_perm == True, "vary_perm not combinable with realistic_window"
    #     perms = create_realistic_window(settings, args.num_dp, output_dataset_dir / "inputs")
    #     # and overwrite min, max perm values

    settings["permeability"]["min"] = float(np.min(perms))
    settings["permeability"]["max"] = float(np.max(perms))
    save_yaml(settings, output_dataset_dir / "inputs")

    if not settings["permeability"]["case"] == "realistic_window":
        if args.vary_perm:
            create_vary_fields(args.num_dp, output_dataset_dir / "inputs", settings, min_max=perms)
        if args.vary_pressure:
            create_vary_fields(args.num_dp, output_dataset_dir / "inputs", settings, min_max=pressures, vary_property="pressure")
        if args.vary_inflow:
            calc_injection_variation(args.num_dp, output_dataset_dir / "inputs", args.num_hps)

    return settings

def make_realistic_windowed_parameter_set(args:argparse.Namespace, destination_path:pathlib.Path, number_of_simulations:int):
    settings = prepare_settings(args, destination_path)

    # 0. load data
    orig_data_path = pathlib.Path("/home/pelzerja/pelzerja/test_nn/dataset_generation_laptop/Phd_simulation_groundtruth/input_files/real_Munich_input_fields/prepared_with_R")
    # destination_path = pathlib.Path("../test_dataset_manual_window")
    # destination_path = pathlib.Path("../test_dataset_automatic_window")
    properties_full, orig_resolution = load_properties_after_R_prep(data_path=orig_data_path)
    # properties_full: 1px (=1cell) = 20m (=orig_resolution)

    # 1. random startpunkt (NOT checked for validity yet) or manual start point, e.g.  # start_positions = [[2100, 2300]]
    start_positions_in_orig_cells = get_start_positions(properties_full["dtw"], settings["general"])
    print("Number of start positions:", len(start_positions_in_orig_cells))

    valid_start_ids = [] # e.g. [(1508, 2031), (1967, 1825), (1914, 2197), (1803, 3142), (731, 2271)]
    current_number_valid_windows = 0
    for i, start_pos in enumerate([[1883, 1241]]): #start_positions_in_orig_cells): 
        try:
            # 2. Größe Box [in cells] bestimmen: 100x100 median oder manuell, e.g. window_shape = np.array([int(12800/20), int(12800/20/2)])
            window_shape = make_window_shape(settings["grid"]["size [m]"], orig_resolution, properties_full, start_pos)
            
            # 3. window drehen
            rotation_angle_degree = estimate_box_rotation(properties_full["darcy_dir"], start_pos, window_shape)
            print(f"Rotation: {rotation_angle_degree} [°]")
            window_rotated_cells = calc_rotated_box(start_pos, window_shape, rotation_angle_degree)
        except Exception as e: # NanError, e.g. RuntimeWarning: All-NaN slice encountered
            print(f"{e} WARNING in run {i}, e.g. NaN error encountered")
            continue

        # 4. check if box is valid, i.e. does not contain nan's, otherwise restart with next start_pos
        valid = check_validity_window(properties_full["dtw"], window_rotated_cells)

        if valid:
            print(f"Valid window for start {start_pos} in run {i}")

            # 5. Data in window ausschneiden
            window_properties = {}
            for name, value in properties_full.items():
                window_properties[name] = cut_out_values(value, window_rotated_cells)
            window_properties["permeability"] = window_properties["hydraulic_conductivity"]/7.5E06

            # 6. max Dicke bestimmen
            # TODO check again (Sept)
            window_height_in_meters = calc_box_height_from_TOK_n_GWGL(window_properties["tok"], window_properties["gwgl"])
            print(f"simulation box height: {window_height_in_meters} meters")

            # TODO Fabian hydraulic head
            # TODO check again (Sept)
            bcs_hh, hh = cut_bcs_hh(window_properties["tok"], window_properties["gwgl"])

            # interpolate in boxes acc. to new resolution, based on coords (in cells of orig resolution) "window_rotated" and values "wondow_properties"
            desti_resolution = settings["grid"]["resolution"]
            window_desti_cells = tuple(np.meshgrid(np.arange(0, window_shape[0],
                                                       step=desti_resolution/orig_resolution),
                                             np.arange(0, window_shape[1],
                                                       step=desti_resolution/orig_resolution)))
            # window_orig_cells = tuple(np.meshgrid(np.arange(0, window_shape[0]),
            #                                  np.arange(0, window_shape[1])))
            interpolators = interpolate_properties(window_properties)
            window_desti_values = {}
            # orig_values = {}
            for key in interpolators.keys():
                window_desti_values[key] = interpolators[key](window_desti_cells)
                # plt.figure()
                # plt.title(key)
                # plt.imshow(window_desti_values[key], origin="lower")
                # plt.savefig("test_interpo.png")

                # plt.figure()
                # orig_values[key] = interpolators[key](window_orig_cells)
                # plt.title(key)
                # plt.imshow(orig_values[key], origin="lower")
                # plt.savefig("test_.png")

                # plt.figure()
                # plt.title(key)
                # plt.scatter(window_rotated_cells[1], window_rotated_cells[0], c=window_properties[key])
                # plt.savefig("test_orig.png")
                # exit()
            
            # 7. store values (and visualize)
            # TODO save box_properties_20 and start, rotation_angle_degree
            # use function "save_vary_field in create_varying_field.py"
            # save_vary_field(filename, ncells=window_shape_in_orig_cells, cells, dims, vary_property="permeability")
            # [plot_img(property, name, resolution) for name, property in box_properties_20.items()]

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
