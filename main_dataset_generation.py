import argparse
import logging
import os
import shutil
import time
from pathlib import Path

from scripts.make_general_settings import load_yaml
from scripts.calc_loc_hp_variation_2d import calc_locs_hp, write_hps_strata_conditions_files
from scripts.calc_hp_parameter_variation import realistic_pump_params, write_pump_param_files
from scripts.visualisation import plot_sim
from scripts.main_helpers import *
from scripts.create_parameter_set import make_realistic_hydrogeological_parameter_windows
from scripts.make_general_settings import load_yaml, save_yaml

def run_simulation(output_dataset_dir:Path, args:argparse.Namespace, run_ids: list):
    time_begin = time.perf_counter()
    avg_time_per_sim = 0
    output_dataset_dir, pflotran_file, settings = preparation(output_dataset_dir, args, run_ids)

    # if varying (automatic) window shape: load subsurface params directly from RUN folder, in every run -> no need to load and change location of files
    if not args.vary_inflow:
        temp_default = 5+groundwater_temp() #[C]
        rate_default = 0.00024 #[m^3/s]
    else:
        temp_default, rate_default = None, None

    # generate set of subsurface parameter fields and grid files, for whole dataset
    make_realistic_hydrogeological_parameter_windows(output_dataset_dir, settings, args.num_dp, temp_default, rate_default)

    # generate operational heat pump parameters (location, pump rate, pump temperature)
    # strata_hps, condition_hps.txt - same for all datasets
    (output_dataset_dir / "interim").mkdir(exist_ok=True, parents=True)
    write_hps_strata_conditions_files(output_dataset_dir/"interim", args.num_hps)

    # generate set of hp locations
    if args.vary_hp:
        hps_cell_ids = calc_locs_hp(args.num_dp, args.num_hps, settings)
    else: ...
        # TODO read default (from settings?) and turn into cell_ids
    
    for run_id in np.arange(args.num_dp):
        output_dataset_run_dir = output_dataset_dir / f"RUN_{run_id}"
        shutil.copytree(output_dataset_dir/"interim", output_dataset_run_dir, dirs_exist_ok=True)
        shutil.copy(f"input_files/{pflotran_file}", f"{output_dataset_run_dir}/pflotran.in")
        
        temps_hps, rates_hps = realistic_pump_params(output_dataset_run_dir, hps_cell_ids[run_id], temp_default, rate_default)
        np.savetxt(output_dataset_run_dir / "injection_temps.txt", np.array([hps_cell_ids[run_id], temps_hps]).T)
        np.savetxt(output_dataset_run_dir / "injection_rates.txt", np.array([hps_cell_ids[run_id], rates_hps]).T)

        write_pump_param_files(output_dataset_run_dir, hps_cell_ids[run_id], temps_hps, rates_hps) # calls write_loc_well_file for each hp, and stores temp_in and rate_in to RUN folder, region_hps.txt
        # TODO ugly

    # RUN SIMULATIONS
    for run_id in run_ids:
        output_dataset_run_dir = output_dataset_dir / f"RUN_{run_id}"
    
        if (output_dataset_run_dir / "pflotran.h5").exists():
            continue
        else:
            os.chdir(output_dataset_run_dir)
            call_pflotran(avg_time_per_sim, run_id)

            if args.visu:
                plot_sim(".", settings, case="2D")

            # clean_up()
            os.chdir("../../../")

    shutil.rmtree(output_dataset_dir/"interim")
    save_yaml({"timestamp": time.ctime(), "duration [s]": (time.perf_counter()-time_begin), "avg duration sim [s]": (avg_time_per_sim/len(run_ids))}, output_dataset_dir, "args")
    logging.info(f"Finished dataset creation at {time.ctime()} after {(time.perf_counter() - time_begin)//60} minutes and {((time.perf_counter() - time_begin)%60):.1f} seconds")

def preparation(output_dataset_dir, args, run_ids):
    logging.info(f"Working at {time.ctime()} on folder {os.getcwd()}")
    assert_combinations(args, run_ids)
    assert args.realistic, "Only realistic case is implemented"

    pflotran_file = "pflotran_realistic.in"
    settings_name = f"settings_{args.dims}D_window_{args.domain_category}"

    output_dataset_dir = output_dataset_dir / args.name
    output_dataset_dir.mkdir(parents=True, exist_ok=True)

    (output_dataset_dir / "inputs").mkdir(parents=True, exist_ok=True) # TODO rm after pump correction

    shutil.copy(f"input_files/{settings_name}.yaml", output_dataset_dir/ "settings.yaml")  
    settings = load_yaml(output_dataset_dir)
    return output_dataset_dir,pflotran_file,settings

def call_pflotran(avg_time_per_sim, run_id):
    start_sim = time.perf_counter()
    logging.info(f"Starting PFLOTRAN simulation of RUN {run_id} at {time.ctime()}")
    tmp_output = False
    output_extension = " -screen_output off" if not tmp_output else ""
    os.system(f"mpirun -n 1 {os.environ['PFLOTRAN_DIR']}/bin/pflotran -output_prefix pflotran{output_extension}")
    avg_time_per_sim += time.perf_counter() - start_sim
    logging.info(f"Finished PFLOTRAN simulation at {time.ctime()} after {(time.perf_counter() - start_sim)//60} minutes and {((time.perf_counter() - start_sim)%60):.1f} seconds")


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
    parser.add_argument("--vary_inflow", type=bool, default=False) 
    parser.add_argument("--domain_category", type=str, choices=["manual", "automatic"], default="manual")
    parser.add_argument("--dims", type=int, choices=[2,3], default=2)  # 2D or 3D
    
    args = parser.parse_args()
    Path("outputs").mkdir(parents=True, exist_ok=True)
    with open("outputs/args.txt", "w") as f:
        f.write(str(args))

    run_ids = list(range(args.id_start, args.id_end))
    output_dataset_dir = pathlib.Path("outputs") 
    output_dataset_dir.mkdir(exist_ok=True, parents=True)
    run_simulation(output_dataset_dir, args, run_ids)