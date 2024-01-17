import argparse
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
from scripts.utils import beep
from scripts.visualisation import plot_sim
from scripts.write_parameters_input_files_parallel import \
    write_parameter_input_files
from scripts.main_helpers import make_output_dir

from make_pipeline_parallel import *

def run_bm_cases_small():
    time_begin = time.perf_counter()
    timestamp_begin = time.ctime()

    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    args.domain_category = "small"
    args.name = "BENCHMARK_BOXES"
    args.benchmark = True
    args = set_benchmark_args(args)
    args.num_hps = 1
    args.vary_hp = False
    pflotran_file = ("input_files/pflotran_iso_perm_xhps.in")
    top_level_dir = os.getcwd()
    PFLOTRAN_DIR = "/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-3.0.2-toidqfdeqa4a5fbnn5yz4q7hm4adb6n3/bin"

    # prepare pflotran sim
    output_dataset_dir = make_output_dir(args.name)
    output_dataset_dir_general_inputs = pathlib.Path(output_dataset_dir, "inputs")
    if not os.path.isdir(output_dataset_dir_general_inputs):
        output_dataset_dir_general_inputs.mkdir(parents=True)
        settings = make_parameter_set(args, output_dataset_dir)
    else:
        settings = load_yaml(f"{output_dataset_dir}/inputs")

    # get benchmark cases
    locs_hps = np.array([settings["grid"]["loc_hp"][0], settings["grid"]["loc_hp"][1]])
    with open("input_files/benchmark_pks_2308_SMALL.yaml", "r") as f:
        pk_cases = yaml.load(f, Loader=yaml.FullLoader)

    time_general_prep = time.perf_counter() - time_begin

    avg_time_prep = 0
    avg_time_sim = 0
    avg_time_visu_post = 0
    counter = 0

    # run benchmark cases
    for  k_name, (_, perm) in pk_cases.items():
        for p_name, (pressure, _) in pk_cases.items():
            time_begin_run_prep = time.perf_counter()
            run_name = f"p_{p_name}_k_{k_name}"
            output_dataset_run_dir = output_dataset_dir / ("RUN_"+run_name)

            shutil.copytree(f"{output_dataset_dir}/pflotran_inputs", f"{output_dataset_run_dir}")
            shutil.copy(pflotran_file, f"{output_dataset_run_dir}/pflotran.in")

            write_parameter_input_files(
                    pressure, perm,
                    output_dataset_dir,
                    run_name,
                    args.vary_perm,
                    settings,
                    locs_hps,
                )
            avg_time_prep += time.perf_counter() - time_begin_run_prep
            
            # run pflotran sim
            time_begin_run_sim = time.perf_counter()
            os.chdir(output_dataset_run_dir)
            os.system(f"mpirun -n 64 {PFLOTRAN_DIR}/pflotran -output_prefix pflotran -screen_output off")
            logging.info(f"Finished Pflotran simulation at {time.ctime()}")
            avg_time_sim += time.perf_counter() - time_begin_run_sim

            # call visualisation
            time_begin_run_visu_post = time.perf_counter()
            if args.visu:
                plot_sim(".", settings, case="2D")
                logging.info(f"Finished visualisation of RUN {run_name} is done")
            shutil.move("pflotran.in", f"../inputs/pflotran_copy.in")
            for file in ["regions_hps.txt", "strata_hps.txt", "conditions_hps.txt", "east.ex", "west.ex", "south.ex", "north.ex", "top_cover.txt", "bottom_cover.txt", "mesh.uge", "settings.yaml",]:
                try:
                    os.remove(file)
                except:
                    continue
            avg_time_visu_post += time.perf_counter() - time_begin_run_visu_post

            counter += 1
            os.chdir(top_level_dir)

    avg_time_prep /= counter
    avg_time_sim /= counter
    avg_time_visu_post /= counter

    # save args as yaml file
    with open(f"{output_dataset_dir}/inputs/args.yaml", "w") as f:
        yaml.dump(vars(args), f, default_flow_style=False)
        f.write(f"timestamp of beginning: {timestamp_begin}\n")
        f.write(f"timestamp of end: {time.ctime()}\n")
        f.write(f"duration of whole process including visualisation and clean up in seconds: {(time.perf_counter()-time_begin)}\n")
        f.write(f"duration of general preparation in seconds: {time_general_prep}\n")
        f.write(f"avg. duration of add. preparation per run in seconds: {avg_time_prep}\n")
        f.write(f"avg. duration of simulation per run in seconds: {avg_time_sim}\n")
        f.write(f"avg. duration of visualisation and postprocessing per run in seconds: {avg_time_visu_post}\n")
        f.write(f"number of runs: {counter}\n")

def run_bm_cases_large():
    time_begin = time.perf_counter()
    timestamp_begin = time.ctime()

    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    args.domain_category = "large"
    args.name = "BENCHMARK_DOMAIN"
    args.benchmark = True
    args = set_benchmark_args(args)
    args.vary_hp = False
    pflotran_file = ("input_files/pflotran_iso_perm_xhps.in")
    top_level_dir = os.getcwd()
    PFLOTRAN_DIR = "/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-3.0.2-toidqfdeqa4a5fbnn5yz4q7hm4adb6n3/bin"

    # prepare pflotran sim
    output_dataset_dir = make_output_dir(args.name)
    output_dataset_dir_general_inputs = pathlib.Path(output_dataset_dir, "inputs")
    if not os.path.isdir(output_dataset_dir_general_inputs):
        output_dataset_dir_general_inputs.mkdir(parents=True)
        settings = make_parameter_set(args, output_dataset_dir)
    else:
        settings = load_yaml(f"{output_dataset_dir}/inputs")

    # get benchmark cases
    with open("input_files/benchmark_locs_hps_train_2hps_1fixed.yaml", "r") as f:
        locs_fixed = yaml.load(f, Loader=yaml.FullLoader)
    with open("input_files/benchmark_locs_hps_2308.yaml", "r") as f:
        loc_cases = yaml.load(f, Loader=yaml.FullLoader)
    with open("input_files/benchmark_pks_2308.yaml", "r") as f:
        pk_cases = yaml.load(f, Loader=yaml.FullLoader)

    time_general_prep = time.perf_counter() - time_begin

    avg_time_prep = 0
    avg_time_sim = 0
    avg_time_visu_post = 0
    counter = 0

    # run benchmark cases
    for loc_name, pos in loc_cases.items():
        for pk_name, (pressure, perm) in pk_cases.items():
            time_begin_run_prep = time.perf_counter()
            run_name = f"pos_{loc_name}_pk_{pk_name}"
            output_dataset_run_dir = output_dataset_dir / ("RUN_"+run_name)

            shutil.copytree(f"{output_dataset_dir}/pflotran_inputs", f"{output_dataset_run_dir}")
            shutil.copy(pflotran_file, f"{output_dataset_run_dir}/pflotran.in")

            locs_hps = np.array([locs_fixed[1], pos])
            write_parameter_input_files(
                    pressure, perm,
                    output_dataset_dir,
                    run_name,
                    args.vary_perm,
                    settings,
                    locs_hps,
                )
            avg_time_prep += time.perf_counter() - time_begin_run_prep
            
            # run pflotran sim
            time_begin_run_sim = time.perf_counter()
            os.chdir(output_dataset_run_dir)
            os.system(f"mpirun -n 64 {PFLOTRAN_DIR}/pflotran -output_prefix pflotran -screen_output off")
            logging.info(f"Finished Pflotran simulation at {time.ctime()}")
            avg_time_sim += time.perf_counter() - time_begin_run_sim

            # call visualisation
            time_begin_run_visu_post = time.perf_counter()
            if args.visu:
                plot_sim(".", settings, case="2D")
                logging.info(f"Finished visualisation of RUN {run_name} is done")
            shutil.move("pflotran.in", f"../inputs/pflotran_copy.in")
            for file in ["regions_hps.txt", "strata_hps.txt", "conditions_hps.txt", "east.ex", "west.ex", "south.ex", "north.ex", "top_cover.txt", "bottom_cover.txt", "mesh.uge", "settings.yaml",]:
                try:
                    os.remove(file)
                except:
                    continue
            avg_time_visu_post += time.perf_counter() - time_begin_run_visu_post

            counter += 1
            os.chdir(top_level_dir)

    avg_time_prep /= counter
    avg_time_sim /= counter
    avg_time_visu_post /= counter

    # save args as yaml file
    with open(f"{output_dataset_dir}/inputs/args.yaml", "w") as f:
        yaml.dump(vars(args), f, default_flow_style=False)
        f.write(f"timestamp of beginning: {timestamp_begin}\n")
        f.write(f"timestamp of end: {time.ctime()}\n")
        f.write(f"duration of whole process including visualisation and clean up in seconds: {(time.perf_counter()-time_begin)}\n")
        f.write(f"duration of general preparation in seconds: {time_general_prep}\n")
        f.write(f"avg. duration of add. preparation per run in seconds: {avg_time_prep}\n")
        f.write(f"avg. duration of simulation per run in seconds: {avg_time_sim}\n")
        f.write(f"avg. duration of visualisation and postprocessing per run in seconds: {avg_time_visu_post}\n")
        f.write(f"number of runs: {counter}\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    domain = "large"
    
    if domain == "small":
        run_bm_cases_small()
    elif domain == "large":
        run_bm_cases_large()
    else:
        raise ValueError(f"Unknown case {domain}")