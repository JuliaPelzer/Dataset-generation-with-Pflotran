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
from scripts.calc_p_and_K import calc_pressure_and_perm_fields
from scripts.create_grid_unstructured import create_all_grid_files
from scripts.create_varying_field import create_vary_fields
from scripts.make_general_settings import load_yaml, save_yaml
from scripts.utils import beep
from scripts.visualisation import plot_sim
from scripts.write_benchmark_parameters_input_files_parallel import \
    write_parameter_input_files


def make_parameter_set(args, confined_aquifer_bool: bool = False):
    output_dataset_dir = args.name

    # copy settings file
    shutil.copy(
        f"input_files/settings_2D_{args.domain_category}.yaml",
        f"{output_dataset_dir}/inputs/settings.yaml",
    )
    if args.benchmark or (args.num_hps - args.vary_hp_amount > 0):
        try:
            shutil.copy(
                "input_files/benchmark_locs_hps.yaml",
                f"{output_dataset_dir}/inputs/benchmark_locs_hps.yaml",
            )
        except:
            pass
            
    # getting settings
    settings = load_yaml(f"{output_dataset_dir}/inputs")
    # make grid files
    path_interim_pflotran_files = pathlib.Path(f"{output_dataset_dir}/pflotran_inputs")
    path_interim_pflotran_files.mkdir(parents=True)
    settings = create_all_grid_files(settings, confined=confined_aquifer_bool, path_to_output=path_interim_pflotran_files,)
    save_yaml(settings, f"{output_dataset_dir}/inputs")

    write_hp_additional_files(
        f"{output_dataset_dir}/pflotran_inputs", args.num_hps, args.vary_hp_amount
    )

    # potentially calc 1 or 2 hp locations
    if args.vary_hp:
        calc_loc_hp_variation_2d(args.num_dp, f"{output_dataset_dir}/inputs", args.num_hps, settings, benchmark_bool=args.benchmark, num_hps_to_vary=args.vary_hp_amount, )

    # make benchmark testcases
    pressures, perms = calc_pressure_and_perm_fields(args.num_dp, f"{output_dataset_dir}/inputs", args.vary_perm, vary_pressure_field=args.vary_pressure, benchmark_bool=args.benchmark, )
    if args.vary_perm:
        create_vary_fields(args.num_dp, f"{output_dataset_dir}/inputs", settings, min_max=perms)
    if args.vary_pressure:
        create_vary_fields(args.num_dp, f"{output_dataset_dir}/inputs", settings, min_max=pressures, vary_property="pressure")

    return settings

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

    for hp_id in range(1, num_hp + 1):
        hp_fixed = f"locs_hp_{hp_id}_fixed.txt"
        file_fixed = origin_folder/hp_fixed
        hp_x = f"locs_hp_x_{hp_id}.txt"
        file_x = origin_folder/hp_x
        hp_y = f"locs_hp_y_{hp_id}.txt"
        file_y = origin_folder/hp_y
        if file_fixed.exists():
            file_fixed = open(origin_folder/hp_fixed, "r")
            # TODO check whether line shift
            for line_nr, line in enumerate(file_fixed):
                if line_nr in run_ids:
                    locs_hps.append([float(pos) for pos in line.split()])
            file_fixed.close()
        elif file_x.exists() and file_y.exists():
            x = []
            file_x = open(origin_folder/hp_x, "r")
            for line_nr, line in enumerate(file_x):
                if line_nr in run_ids:
                    x.append(float(line))
            file_x.close()
            y = []
            file_y = open(origin_folder/hp_y, "r")
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


def run_simulation(args, run_ids: list):
    time_begin = time.perf_counter()
    timestamp_begin = time.ctime()
    avg_time_per_sim = 0
    logging.info(f"Working at {timestamp_begin} on folder {os.getcwd()}")

    confined_aquifer = False
    if args.benchmark:
        args = set_benchmark_args(args)

    if args.num_hps > 1:
        assert (args.vary_hp), f"If number of heatpumps is larger than 1, vary_hp must be True"

    # check whether output folder exists else define
    output_dataset_dir = pathlib.Path(args.name)
    output_dataset_dir.mkdir(parents=True, exist_ok=True)

    # folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
    output_dataset_dir_general_inputs = pathlib.Path(output_dataset_dir, "inputs")
    if not os.path.isdir(output_dataset_dir_general_inputs):
        output_dataset_dir_general_inputs.mkdir(parents=True)
        logging.info(f"...{output_dataset_dir}/inputs folder is created")

        # ONCE PER DATASET: generate set of perms, pressures and hp locations
        settings = make_parameter_set(args, confined_aquifer_bool=confined_aquifer)
    else:
        logging.info(f"...{output_dataset_dir}/inputs folder already exists")

        # get settings
        settings = load_yaml(f"{output_dataset_dir}/inputs")

    pflotran_file = set_pflotran_file(args, confined_aquifer=confined_aquifer)

    pressures, perms, locs_hps = load_inputs_subset(run_ids, output_dataset_dir_general_inputs, args.num_hps, settings, vary_perm=args.vary_perm, vary_pressure=args.vary_pressure,)

    top_level_dir = os.getcwd()
    # make run folders
    for run_id in run_ids:
        output_dataset_run_dir = pathlib.Path(f"{output_dataset_dir}/RUN_{run_id}")

        # copy respective pflotran.in file
        shutil.copytree(output_dataset_dir/"pflotran_inputs", output_dataset_run_dir)
        shutil.copy(pflotran_file, f"{output_dataset_run_dir}/pflotran.in")

        if not args.vary_hp:
            write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm, args.vary_pressure,)
        else:
            if args.num_hps > 0:
                write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm, args.vary_pressure, settings, locs_hps[run_ids.index(run_id)], )
            else:
                write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm, vary_pressure_field=args.vary_pressure,)

        os.chdir(output_dataset_run_dir)
        start_sim = time.perf_counter()
        logging.info(f"Starting PFLOTRAN simulation of RUN {run_id} at {time.ctime()}")
        PFLOTRAN_DIR = "/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-3.0.2-toidqfdeqa4a5fbnn5yz4q7hm4adb6n3/bin"
        tmp_output = False
        output_extension = " -screen_output off" if not tmp_output else ""
        os.system(f"mpirun -n 64 {PFLOTRAN_DIR}/pflotran -output_prefix pflotran{output_extension}")
        avg_time_per_sim += time.perf_counter() - start_sim
        logging.info(f"Finished PFLOTRAN simulation at {time.ctime()} after {time.perf_counter() - start_sim}")

        # call visualisation
        if args.visu:
            try:
                plot_sim(".", settings, case="2D", confined=confined_aquifer)
                logging.info(f"...visualisation of RUN {run_id} is done")
            except:
                logging.info(f"...visualisation of RUN {run_id} failed")
                # beep()

        clean_up()
        os.chdir(top_level_dir)

    clean_up_end(args, output_dataset_dir)
    avg_time_per_sim /= len(run_ids)
    save_args(args, output_dataset_dir, timestamp_begin, time_begin, time.perf_counter(), avg_time_per_sim)
    logging.info(f"Finished dataset creation at {time.ctime()} after {time.perf_counter() - time_begin}")


def set_benchmark_args(args):
    args.num_dp = 1
    args.visu = True
    args.vary_hp = True
    args.vary_hp_amount = 0
    args.num_hps = 2
    args.vary_perm = False  # True
    logging.info(f"Running benchmark testcases with settings: {args}")
    return args


def set_pflotran_file(args, confined_aquifer):
    # build pflotran file name
    perm_case = "vary" if args.vary_perm else "iso"
    confined_extension = "_confined" if confined_aquifer else ""
    hps_extension = f"_xhps" if args.num_hps >= 1 else f"_{args.num_hps}hps"
    vary_pressure_extension = "_vary_pressure" if args.vary_pressure else ""
    pflotran_file = (
        f"input_files/pflotran_{perm_case}_perm{vary_pressure_extension}{hps_extension}{confined_extension}.in"
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
    (pathlib.Path(".") / "hps").mkdir(parents=True, exist_ok=True)
    for file in pathlib.Path(".").glob("*.vs"):
        shutil.move(file, "hps")

def clean_up_end(args, output_dataset_dir):
    if args.vary_perm:
        shutil.rmtree(output_dataset_dir/"inputs"/"permeability_fields")
    if not args.benchmark:
        try:
            os.remove(f"{output_dataset_dir}/inputs/benchmark_locs_hps.yaml")
        except:
            pass

def save_args(args, output_dataset_dir, timestamp_begin, time_begin, time_end, avg_time_per_sim):
    # save args as yaml file
    with open(f"{output_dataset_dir}/inputs/args.yaml", "w") as f:
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", type=bool, default=False)
    parser.add_argument("--num_dp", type=int, default=1)  # int = 100 # number of datapoints
    parser.add_argument("--name", type=str, default="default")  # benchmark_large_vary_perm_2hps")
    parser.add_argument("--visu", type=bool, default=False)  # visualisation
    parser.add_argument("--num_hps", type=int, default=0)  # number of hp locations
    parser.add_argument("--vary_hp", type=bool, default=False)  # vary hp location
    parser.add_argument("--vary_hp_amount", type=int, default=0)  # how many hp locations should be varied
    parser.add_argument("--vary_perm", type=bool, default=False)  # vary permeability
    parser.add_argument("--vary_pressure", type=bool, default=False)  # vary pressure
    parser.add_argument("--id_start", type=int, default=0)  # start id
    parser.add_argument("--id_end", type=int, default=1)  # end id
    parser.add_argument("--domain_category", type=str, choices=["large", "small", "medium", "giant"], default="large")

    args = parser.parse_args()

    run_ids = list(range(args.id_start, args.id_end))
    run_simulation(args, run_ids)

    # just_visualize(args)
