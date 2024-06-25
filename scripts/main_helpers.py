import h5py
import logging
import os
import pathlib
import shutil
import time
import numpy as np
import yaml

from scripts.calc_loc_hp_variation_2d import (calc_loc_hp_variation_2d,
                                              write_hp_additional_files)
from scripts.calc_p_and_K import calc_pressure_and_perm_values
from scripts.calc_hp_parameter_variation import calc_injection_variation
from scripts.create_grid_unstructured import create_all_grid_files
from scripts.create_varying_field import create_vary_fields, create_realistic_window
from scripts.make_general_settings import load_yaml, save_yaml
from scripts.visualisation import plot_sim


def make_parameter_set(args, output_dataset_dir, confined_aquifer_bool: bool = False):

    # copy settings file
    if "3D" in args.domain_category:
        # args.domain_category =  # rm 3D
        settings_name = f"settings_3D_{args.domain_category}"
    else:
        settings_name = f"settings_2D_{args.domain_category}"
    shutil.copy(f"input_files/{settings_name}.yaml", output_dataset_dir / "inputs" / "settings.yaml", )
    if args.benchmark or (args.num_hps - args.vary_hp_amount > 0):
        try:
            shutil.copy("input_files/benchmark_locs_hps.yaml", output_dataset_dir / "inputs" / "benchmark_locs_hps.yaml",)
        except:
            pass
            
    # getting settings
    settings = load_yaml(output_dataset_dir / "inputs")
    # make grid files
    path_interim_pflotran_files = output_dataset_dir / "pflotran_inputs"
    path_interim_pflotran_files.mkdir(parents=True, exist_ok=True)
    settings = create_all_grid_files(settings, confined=confined_aquifer_bool, path_to_output=path_interim_pflotran_files,)

    write_hp_additional_files(output_dataset_dir / "pflotran_inputs", args.num_hps, args.vary_hp_amount) # region_hps, strata_hps, condition_hps.txt

    # optional: calc 1 or more hp locations
    if args.vary_hp:
        (output_dataset_dir / "inputs" / "hps").mkdir(parents=True, exist_ok=True)
        calc_loc_hp_variation_2d(args.num_dp, output_dataset_dir / "inputs" / "hps", args.num_hps, settings, benchmark_bool=args.benchmark, num_hps_to_vary=args.vary_hp_amount, )

    # calc pressure and perm values
    pressures, perms = calc_pressure_and_perm_values(args.num_dp, output_dataset_dir / "inputs", args.vary_perm, vary_pressure_field=args.vary_pressure, benchmark_bool=args.benchmark, only_vary_distribution=args.only_vary_distribution,)
    settings["pressure"] = {}
    settings["pressure"]["min"] = float(np.min(pressures))
    settings["pressure"]["max"] = float(np.max(pressures))

    if settings["permeability"]["case"] == "realistic_window": 
        assert args.vary_perm == True, "vary_perm not combinable with realistic_window"
        perms = create_realistic_window(settings, args.num_dp, output_dataset_dir / "inputs")
        # and overwrite min, max perm values

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

def make_output_dir(name: str):
    output_dataset_dir = pathlib.Path("outputs") 
    output_dataset_dir.mkdir(parents=True, exist_ok=True)
    output_dataset_dir = output_dataset_dir / name
    output_dataset_dir.mkdir(parents=True, exist_ok=True)
    return output_dataset_dir

def load_iso_files(origin_folder: pathlib.Path, run_ids: list, curr_file: str):
    fields = []
    file_fixed = open(origin_folder/curr_file, "r")
    for line_nr, line in enumerate(file_fixed):
        if line_nr in run_ids:
            fields.append(float(line))
    file_fixed.close()

    return fields

def load_vary_files(origin_folder: pathlib.Path, fields_folder: str):
    fields = []
    for file in (origin_folder/fields_folder).iterdir():
        with h5py.File(file, "r") as f:
            fields.append(f)
    return fields

def load_list_files(origin_folder: pathlib.Path, run_ids: list, curr_file: str):
    fields = []
    with open(origin_folder/curr_file, "r") as file_fixed:
        for line_nr, line in enumerate(file_fixed):
            if line_nr in run_ids:
                print(np.array(line.split(" "), dtype=np.float32))
                fields.append(np.array(line.split(" "), dtype=np.float32))
    return fields

def load_inputs_subset(run_ids: list, origin_folder: pathlib.Path, num_hp: int, settings: dict = None, vary_perm: bool = False, vary_pressure: bool = False, vary_inflow: bool = False):

    # load perm files
    if not vary_perm:
        perms = load_iso_files(origin_folder, run_ids, "permeability_values.txt")
    else:
        perms = load_vary_files(origin_folder, "permeability_fields")

    # load pressure files
    if not vary_pressure:
        pressures = load_iso_files(origin_folder, run_ids, "pressure_values.txt")
    else:
        pressures = load_vary_files(origin_folder, "pressure_fields")

    # initialize lists
    locs_hps = []
    # load hp files
    origin_hps = origin_folder / "hps"
    for hp_id in range(1, num_hp + 1):
        hp_fixed = f"locs_hp_{hp_id}_fixed.txt"
        file_fixed = origin_hps/hp_fixed
        hp_x = f"locs_hp_x_{hp_id}.txt"
        file_x = origin_hps/hp_x
        hp_y = f"locs_hp_y_{hp_id}.txt"
        file_y = origin_hps/hp_y
        if file_fixed.exists():
            file_fixed = open(origin_hps/hp_fixed, "r")
            # TODO check whether line shift
            for line_nr, line in enumerate(file_fixed):
                if line_nr in run_ids:
                    locs_hps.append([float(pos) for pos in line.split()])
            file_fixed.close()
        elif file_x.exists() and file_y.exists():
            x = []
            file_x = open(origin_hps/hp_x, "r")
            for line_nr, line in enumerate(file_x):
                if line_nr in run_ids:
                    x.append(float(line))
            file_x.close()
            y = []
            file_y = open(origin_hps/hp_y, "r")
            for line_nr, line in enumerate(file_y):
                if line_nr in run_ids:
                    y.append(float(line))
            file_y.close()
            locs_hps.append(np.array([x, y]).T)
        else:
            # take value from settings.yaml in [m]
            locs_hps.append(settings["grid"]["loc_hp"][0:2])
    if len(np.array(locs_hps).shape) == 2:
        locs_hps = [locs_hps]
    elif len(np.array(locs_hps).shape) == 3:
        locs_hps = np.array(locs_hps)
        locs_hps = np.swapaxes(locs_hps, 0, 1)

    if vary_inflow:
        temp_in = load_list_files(origin_folder, run_ids, "injection_temperatures.txt")
        rate_in = load_list_files(origin_folder, run_ids, "injection_rates.txt")
    else:
        try:
            temp_in = np.ones([len(run_ids), num_hp]) * settings["injection"]["temperature"]
            rate_in = np.ones([len(run_ids), num_hp]) * settings["injection"]["rate"]
        except:
            temp_in = None
            rate_in = None
    return np.array(pressures), np.array(perms), np.array(locs_hps), np.array(temp_in), np.array(rate_in)


def set_pflotran_file(args, confined_aquifer):
    # build pflotran file name
    perm_case = "vary" if args.vary_perm else "iso"
    confined_extension = "_confined" if confined_aquifer else ""
    vary_pressure_extension = "_vary_pressure" if args.vary_pressure else ""
    vary_inflow_extension = "_vary_inflow" if args.vary_inflow else ""
    pflotran_file = (
        f"pflotran_{perm_case}_perm{vary_pressure_extension}{vary_inflow_extension}{confined_extension}.in"
    )
    return pflotran_file

def assert_combinations(args, run_ids: list):
    # vary inflow only combinable with iso perm and pressure
    if args.vary_inflow:
        assert (args.vary_perm == False) and (args.vary_pressure == False) and (args.vary_hp==False), f"vary_inflow only combinable with iso perm and pressure and 1hp"
    assert args.num_dp >= len(run_ids), f"number of datapoints must be smaller than number of run ids"

def clean_up():
    try:
        shutil.move("pflotran.in", f"../inputs/pflotran.in")
    except: ... # exists already in inputs
    for file in ["regions_hps.txt", "strata_hps.txt", "conditions_hps.txt", "east.ex", "west.ex", "south.ex", "north.ex", "top_cover.txt", "bottom_cover.txt", "mesh.uge", "settings.yaml",]:
        try:
            os.remove(file)
        except:
            continue
    # move all hps into hps folder
    hps_dir = pathlib.Path("./hps")
    hps_dir.mkdir(parents=True, exist_ok=True)
    for file in pathlib.Path(".").glob("*.vs"):
        shutil.move(file, hps_dir / file)

def clean_up_end(args, output_dataset_dir: pathlib.Path):
    if not args.benchmark:
        try:
            os.remove(output_dataset_dir / "inputs" / "benchmark_locs_hps.yaml")
        except:
            pass

def save_args(output_dataset_dir, args, timestamp_begin, time_begin, time_end, avg_time_per_sim):
    # save args as yaml file
    with open(output_dataset_dir / "inputs"/"args.yaml", "w") as f:
        yaml.dump(vars(args), f, default_flow_style=False)
        f.write(f"timestamp of beginning: {timestamp_begin}\n")
        f.write(f"timestamp of end: {time.ctime()}\n")
        f.write(
            f"duration of whole process including visualisation and clean up in seconds: {(time_end-time_begin)}\n"
        )
        f.write(f"average time per simulation in seconds: {avg_time_per_sim}\n")

def just_visualize(args):
    settings = load_yaml(f"{args.name}/inputs")
    confined_aquifer = False

    for run_id in range(4):  # in case of testcases_4
        output_dataset_run_dir = f"{args.name}/RUN_{run_id}"
        plot_sim(output_dataset_run_dir, settings, case="2D", confined=confined_aquifer)
        logging.info(f"...visualisation of RUN {run_id} is done")