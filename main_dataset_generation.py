import argparse
import logging
import os
import shutil
import time
from pathlib import Path

from scripts.make_general_settings import load_yaml
from scripts.visualisation import plot_sim
from scripts.write_parameters_input_files_parallel import write_parameter_input_files
from scripts.main_helpers import *
from scripts.create_parameter_set import make_parameter_set, make_realistic_windowed_parameter_set

def run_simulation(args, run_ids: list):
    time_begin = time.perf_counter()
    timestamp_begin = time.ctime()
    avg_time_per_sim = 0
    logging.info(f"Working at {timestamp_begin} on folder {os.getcwd()}")
    assert_combinations(args, run_ids)
    assert args.realistic, "Only realistic case is implemented"

    output_dataset_dir = make_output_dir(args.name)

    # folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
    # if (output_dataset_dir / "inputs").exists() == False: # TODO einkommentieren
    (output_dataset_dir / "inputs").mkdir(parents=True, exist_ok=True)
    logging.info(f"...{output_dataset_dir}/inputs folder is created")

    # ONCE PER DATASET: generate set of perms, pressures and hp locations; and make grid files
    if args.realistic:
        settings = make_realistic_windowed_parameter_set(args, output_dataset_dir, args.num_dp)
    else:
        settings = make_parameter_set(args, output_dataset_dir)
    # else: # TODO eikommentieren
    #     logging.info(f"...{output_dataset_dir}/inputs folder already exists")

    #     # get settings
    #     settings = load_yaml(output_dataset_dir/"inputs")

    pflotran_file = "pflotran_realistic.in"

    p_grads, perms, locs_hps, temp_in, rate_in = load_inputs_subset(run_ids, output_dataset_dir / "inputs", args.num_hps, settings) # TODO check naming

    # make run folders
    for run_id in run_ids:
        output_dataset_run_dir = output_dataset_dir / f"RUN_{run_id}"

        # copy respective pflotran.in file
        shutil.copytree(output_dataset_dir/"pflotran_inputs", output_dataset_run_dir)
        shutil.copy(f"input_files/{pflotran_file}", f"{output_dataset_run_dir}/pflotran.in")

        run_idx = run_ids.index(run_id)
        if args.num_hps > 0 and args.vary_hp:
            loc_hps = locs_hps[run_idx]
        else:
            loc_hps = None
        write_parameter_input_files(p_grads[run_idx], output_dataset_dir, run_id, settings, loc_hps, temp_in[run_idx], rate_in[run_idx])

        os.chdir(output_dataset_run_dir)
        start_sim = time.perf_counter()
        logging.info(f"Starting PFLOTRAN simulation of RUN {run_id} at {time.ctime()}")
        tmp_output = False
        output_extension = " -screen_output off" if not tmp_output else ""
        PFLOTRAN_DIR = os.environ["PFLOTRAN_DIR"]
        os.system(f"mpirun -n 1 {PFLOTRAN_DIR}/bin/pflotran -output_prefix pflotran{output_extension}")
        avg_time_per_sim += time.perf_counter() - start_sim
        logging.info(f"Finished PFLOTRAN simulation at {time.ctime()} after {(time.perf_counter() - start_sim)//60} minutes and {((time.perf_counter() - start_sim)%60):.1f} seconds")

        # call visualisation
        if args.visu:
            try:
                plot_sim(".", settings, case="2D")
                logging.info(f"...visualisation of RUN {run_id} is done")
            except:
                logging.info(f"...visualisation of RUN {run_id} failed")

        clean_up()
        os.chdir("../../../")

    clean_up_end(args, output_dataset_dir)
    avg_time_per_sim /= len(run_ids)
    save_args(output_dataset_dir, args, timestamp_begin, time_begin, time.perf_counter(), avg_time_per_sim)
    logging.info(f"Finished dataset creation at {time.ctime()} after {time.perf_counter() - time_begin}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--realistic", type=bool, default=True)
    parser.add_argument("--num_dp", type=int, default=1)  # int = 100 # number of datapoints
    parser.add_argument("--id_start", type=int, default=0)  # start id
    parser.add_argument("--id_end", type=int, default=1)  # end id
    parser.add_argument("--name", type=str, default="test_dataset_manual_window")  
    parser.add_argument("--visu", type=bool, default=False)  # visualisation
    parser.add_argument("--num_hps", type=int, default=1)  # number of hp locations
    parser.add_argument("--vary_hp", type=bool, default=False)  # vary hp location
    parser.add_argument("--domain_category", type=str, choices=["manual", "automatic"], default="manual")
    parser.add_argument("--dims", type=int, choices=[2,3], default=2)  # 2D or 3D
    
    args = parser.parse_args()
    Path("outputs").mkdir(parents=True, exist_ok=True)
    with open("outputs/args.txt", "w") as f:
        f.write(str(args))

    run_ids = list(range(args.id_start, args.id_end))
    run_simulation(args, run_ids)