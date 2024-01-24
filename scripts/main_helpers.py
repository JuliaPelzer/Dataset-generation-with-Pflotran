import argparse
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
from scripts.create_grid_unstructured import create_all_grid_files
from scripts.create_varying_field import create_vary_fields
from scripts.make_general_settings import load_yaml, save_yaml
from scripts.visualisation import plot_sim


def make_parameter_set(args, output_dataset_dir, confined_aquifer_bool: bool = False):

    # copy settings file
    shutil.copy(f"input_files/settings_2D_{args.domain_category}.yaml", output_dataset_dir / "inputs" / "settings.yaml", )
    if args.benchmark or (args.num_hps - args.vary_hp_amount > 0):
        try:
            shutil.copy("input_files/benchmark_locs_hps.yaml", output_dataset_dir / "inputs" / "benchmark_locs_hps.yaml",)
        except:
            pass
            
    # getting settings
    settings = load_yaml(output_dataset_dir / "inputs")
    # make grid files
    path_interim_pflotran_files = output_dataset_dir / "pflotran_inputs"
    path_interim_pflotran_files.mkdir(parents=True)
    settings = create_all_grid_files(settings, confined=confined_aquifer_bool, path_to_output=path_interim_pflotran_files,)
    save_yaml(settings, output_dataset_dir / "inputs")

    write_hp_additional_files(output_dataset_dir / "pflotran_inputs", args.num_hps, args.vary_hp_amount)

    # potentially calc 1 or 2 hp locations
    if args.vary_hp:
        (output_dataset_dir / "inputs" / "hps").mkdir(parents=True, exist_ok=True)
        calc_loc_hp_variation_2d(args.num_dp, output_dataset_dir / "inputs" / "hps", args.num_hps, settings, benchmark_bool=args.benchmark, num_hps_to_vary=args.vary_hp_amount, )

    # make benchmark testcases
    pressures, perms = calc_pressure_and_perm_values(args.num_dp, output_dataset_dir / "inputs", args.vary_perm, vary_pressure_field=args.vary_pressure, benchmark_bool=args.benchmark, only_vary_distribution=args.only_vary_distribution,)
    settings["permeability"]["min"] = np.min(perms)
    settings["permeability"]["max"] = np.max(perms)
    settings["pressure"] = {}
    settings["pressure"]["min"] = np.min(pressures)
    settings["pressure"]["max"] = np.max(pressures)

    if args.vary_perm:
        create_vary_fields(args.num_dp, output_dataset_dir / "inputs", settings, min_max=perms)
    if args.vary_pressure:
        create_vary_fields(args.num_dp, output_dataset_dir / "inputs", settings, min_max=pressures, vary_property="pressure")

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

def load_inputs_subset(run_ids: list, origin_folder: pathlib.Path, num_hp: int, settings: dict = None, vary_perm: bool = False, vary_pressure: bool = False,):
    # initialize lists
    locs_hps = []

    # load files
    if not vary_perm:
        perms = load_iso_files(origin_folder, run_ids, "permeability_values.txt")
    else:
        perms = load_vary_files(origin_folder, "permeability_fields")

    if not vary_pressure:
        pressures = load_iso_files(origin_folder, run_ids, "pressure_values.txt")
    else:
        pressures = load_vary_files(origin_folder, "pressure_fields")

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

    return np.array(pressures), np.array(perms), np.array(locs_hps)


def set_pflotran_file(args, confined_aquifer):
    # build pflotran file name
    perm_case = "vary" if args.vary_perm else "iso"
    confined_extension = "_confined" if confined_aquifer else ""
    vary_pressure_extension = "_vary_pressure" if args.vary_pressure else ""
    pflotran_file = (
        f"input_files/pflotran_{perm_case}_perm{vary_pressure_extension}{confined_extension}.in"
    )
    return pflotran_file

def clean_up():
    shutil.move("pflotran.in", f"../inputs/pflotran.in")
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

def clean_up_end(args):
    if args.vary_perm:
        shutil.rmtree("inputs/permeability_fields")
    if args.vary_pressure:
        shutil.rmtree("inputs/pressure_fields")
    if not args.benchmark:
        try:
            os.remove("inputs/benchmark_locs_hps.yaml")
        except:
            pass

def save_args(args, timestamp_begin, time_begin, time_end, avg_time_per_sim):
    # save args as yaml file
    with open("inputs/args.yaml", "w") as f:
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