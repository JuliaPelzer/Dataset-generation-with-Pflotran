import argparse
import h5py
import logging
import os
import pathlib
import shutil
import time

from scripts.make_general_settings import load_yaml
from scripts.utils import beep
from scripts.visualisation import plot_sim
from scripts.write_parameters_input_files_parallel import write_parameter_input_files
from scripts.main_helpers import *

def run_simulation(args, run_ids: list):
    time_begin = time.perf_counter()
    timestamp_begin = time.ctime()
    avg_time_per_sim = 0
    logging.info(f"Working at {timestamp_begin} on folder {os.getcwd()}")
    assert_combinations(args, run_ids)

    confined_aquifer = False
    if args.benchmark:
        args = set_benchmark_args(args)

    if args.num_hps > 1:
        assert (args.vary_hp), f"If number of heatpumps is larger than 1, vary_hp must be True"

    output_dataset_dir = make_output_dir(args.name)

    # folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
    if not os.path.isdir(output_dataset_dir / "inputs"):
        (output_dataset_dir / "inputs").mkdir(parents=True)
        logging.info(f"...{output_dataset_dir}/inputs folder is created")

        # ONCE PER DATASET: generate set of perms, pressures and hp locations
        settings = make_parameter_set(args, output_dataset_dir, confined_aquifer_bool=confined_aquifer)
    else:
        logging.info(f"...{output_dataset_dir}/inputs folder already exists")

        # get settings
        settings = load_yaml(f"{output_dataset_dir}/inputs")

    pflotran_file = set_pflotran_file(args, confined_aquifer=confined_aquifer)

    pressures, perms, locs_hps, temp_in, rate_in = load_inputs_subset(run_ids, output_dataset_dir / "inputs", args.num_hps, settings, vary_perm=args.vary_perm, vary_pressure=args.vary_pressure, vary_inflow=args.vary_inflow)

    # make run folders
    for run_id in run_ids:
        output_dataset_run_dir = output_dataset_dir / f"RUN_{run_id}"

        # copy respective pflotran.in file
        shutil.copytree(output_dataset_dir/"pflotran_inputs", output_dataset_run_dir)
        shutil.copy(f"input_files/{pflotran_file}", f"{output_dataset_run_dir}/pflotran.in")

        if args.num_hps > 0 and args.vary_hp:
            write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm, args.vary_pressure, settings, locs_hps[run_ids.index(run_id)], temp=temp_in[run_ids.index(run_id)], rate=rate_in[run_ids.index(run_id)])
        else:
            write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm, args.vary_pressure, settings, temp=temp_in[run_ids.index(run_id)], rate=rate_in[run_ids.index(run_id)])

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
        os.chdir("../../../")

    clean_up_end(args, output_dataset_dir)
    avg_time_per_sim /= len(run_ids)
    save_args(output_dataset_dir, args, timestamp_begin, time_begin, time.perf_counter(), avg_time_per_sim)
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
    parser.add_argument("--domain_category", type=str, choices=["large", "small", "medium", "giant", "small_square"], default="large")
    parser.add_argument("--only_vary_distribution", type=bool, default=False)  # only vary distribution, for perm-field get min+max; for pressure:=0.003
    parser.add_argument("--vary_inflow", type=bool, default=False)  # vary injection parameters (inflow rate, temperature)

    args = parser.parse_args()

    run_ids = list(range(args.id_start, args.id_end))
    run_simulation(args, run_ids)

    # just_visualize(args)
