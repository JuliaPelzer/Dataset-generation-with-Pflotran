import h5py
import logging
import os
import pathlib
import shutil
import time
import numpy as np
import yaml
import argparse

from scripts.make_general_settings import load_yaml
from scripts.visualisation import plot_sim

def groundwater_temp() -> float:
    return 10

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

def load_inputs_subset(run_ids: list, origin_folder: pathlib.Path):

    # load perm files
    perms = load_vary_files(origin_folder, "permeability_fields")
    # load pressure files
    pressure_grads = load_iso_files(origin_folder, run_ids, "pressure_gradients.txt")
    
    return np.array(pressure_grads), np.array(perms)


def load_pump_params(args:argparse.Namespace, run_ids: list, origin_folder: pathlib.Path, num_hp: int, settings: dict = None):
    if args.vary_inflow:
        # load temp_in
        temp_in = load_list_files(origin_folder, run_ids, "injection_temperatures.txt")
        # load rate_in
        rate_in = load_list_files(origin_folder, run_ids, "injection_rates.txt")
    else:
        try:
            temp_in = np.ones([len(run_ids), num_hp]) * settings["injection"]["temperature"]
            rate_in = np.ones([len(run_ids), num_hp]) * settings["injection"]["rate"]
        except:
            temp_in = None
            rate_in = None

    # load hp locations
    locs_hps = []
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
            # take value from settings.yaml
            locs_hps.append(settings["grid"]["loc_hp [m]"][0:2])
    if len(np.array(locs_hps).shape) == 2:
        locs_hps = [locs_hps]
    elif len(np.array(locs_hps).shape) == 3:
        locs_hps = np.array(locs_hps)
        locs_hps = np.swapaxes(locs_hps, 0, 1)
    
    return np.array(locs_hps), np.array(temp_in), np.array(rate_in)

def assert_combinations(args, run_ids: list):
    # vary inflow only combinable with iso perm and pressure
    assert args.num_dp >= len(run_ids), f"number of datapoints must be smaller than number of run ids"

    if args.num_hps > 1:
        assert (args.vary_hp), f"If number of heatpumps is larger than 1, vary_hp must be True"

def clean_up():
    try:
        shutil.move("pflotran.in", f"../inputs/pflotran.in")
    except: ... # exists already in inputs
    
    # move all hps into hps folder
    hps_dir = pathlib.Path("./hps")
    hps_dir.mkdir(parents=True, exist_ok=True)
    for file in pathlib.Path(".").glob("*.vs"):
        shutil.move(file, hps_dir / file)

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

    for run_id in range(4):  # in case of testcases_4
        output_dataset_run_dir = f"{args.name}/RUN_{run_id}"
        plot_sim(output_dataset_run_dir, settings, case="2D")
        logging.info(f"...visualisation of RUN {run_id} is done")