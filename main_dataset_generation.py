import argparse
import logging
import os
import shutil
import time
from pathlib import Path
import numpy as np

from scripts.hp_variation_2d import write_hps_strata_conditions_files, hps_locs_to_ids, calc_hps_locs_float
from scripts.calc_hp_parameter_variation import realistic_pump_params, write_pump_param_files
from scripts.visualisation_refined import plot_results
from scripts.main_helpers import assert_combinations, groundwater_temp
from scripts.create_parameter_set import realistic_hydrogeological_params_boxes_and_hp_params, interpolate_and_store_windows_and_bcs
from scripts.mesh_generation import mesh_generation_all_dps
from scripts.mesh_refinement import refinement_all_dps
from scripts.mesh_generation_boundaries import create_boundary_locs
from scripts.utils import load_yaml, save_yaml

def run_simulation(output_dataset_dir:Path, args:argparse.Namespace, run_ids: list):
    time_begin = time.perf_counter()
    avg_time_per_sim = 0
    output_dataset_dir, pflotran_file, settings = preparation(output_dataset_dir, args, run_ids)

    (output_dataset_dir / "interim").mkdir(exist_ok=True, parents=True)
    for run_id in np.arange(args.num_dp):
        output_run_dir = output_dataset_dir / f"RUN_{run_id}"
        output_run_dir.mkdir(exist_ok=True, parents=True)
        
    # if varying (automatic) window shape: load subsurface params directly from RUN folder, in every run -> no need to load and change location of files
    if not args.vary_inflow:
        temp_default = 5 + groundwater_temp() #[C]
        rate_default = 0.00024 #[m^3/s]
    else:
        temp_default, rate_default = None, None

    # strata_hps, condition_hps.txt - same for all datasets
    write_hps_strata_conditions_files(output_dataset_dir/"interim", args.num_hps)

    # generate set of hp locations
    hps_locs = calc_hps_locs_float(args.vary_hp, args.num_dp, args.num_hps, settings)

    # generate sets of subsurface parameter fields (for whole dataset)
    windows_collected, hps_params_collected, orig_resolution, settings = realistic_hydrogeological_params_boxes_and_hp_params(settings, args.num_dp, temp_default, rate_default)

    # generate operational heat pump parameters (location, pump rate, pump temperature)
    # TODO call of data_dir/"drawdown.h5" is wrong - get if form windows_collected?
    if None in hps_params_collected:
        hps_temps, hps_rates = realistic_pump_params(windows_collected, hps_locs, orig_resolution, temp_default, rate_default)
    else:
        hps_temps = np.array([dp["temp"] for dp in hps_params_collected])
        hps_rates = np.array([dp["rate"] for dp in hps_params_collected])

    # mesh generation + refinement
    if not settings["grid"]["refinement"]:
        meshs = mesh_generation_all_dps(settings, output_dataset_dir, windows_collected, orig_resolution)
        hps_cell_ids = hps_locs_to_ids(hps_locs, meshs)
    else:
        meshs, hps_cell_ids = refinement_all_dps(args.num_dp, settings["grid"], hps_locs, hps_temps, hps_rates, windows_collected, orig_resolution, output_dataset_dir)
    
    for run_id in np.arange(args.num_dp):
        output_run_dir = output_dataset_dir / f"RUN_{run_id}"
        shutil.copytree(output_dataset_dir/"interim", output_run_dir, dirs_exist_ok=True)

        # store realistic pump params for hp-cell_id, generate files regions_hps and inj-conditions_hps
        write_pump_param_files(output_run_dir, hps_cell_ids[run_id], hps_temps[run_id], hps_rates[run_id])

        bcs_cell_ids = {}
        for direction in ["north", "south"]: #, "west", "east", "top", "bottom"]:
            bcs_cell_ids[direction] = create_boundary_locs(meshs[run_id], direction, settings["grid"]["resolution"], windows_collected[run_id]["shape"], orig_resolution, output_run_dir)
            # TODO check for 1layer3D

        # evaluate and store (to h5) properties and BCs on refined mesh
        interpolate_and_store_windows_and_bcs(output_run_dir, windows_collected[run_id], meshs[run_id], bcs_cell_ids, orig_resolution)

    # RUN SIMULATIONS
    for run_id in run_ids:
        output_run_dir = output_dataset_dir / f"RUN_{run_id}"
        shutil.copy(f"input_files/{pflotran_file}", f"{output_run_dir}/pflotran.in")
    
        if (output_run_dir / "pflotran.h5").exists():
            continue
        else:
            os.chdir(output_run_dir)
            call_pflotran(avg_time_per_sim, run_id)

            os.chdir("../../../")

        if args.visu:
            plot_results(output_run_dir)

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

    shutil.copy(f"input_files/{settings_name}.yaml", output_dataset_dir/ "settings.yaml")  
    settings = load_yaml(output_dataset_dir)

    if settings["grid"]["size [m]"] is None:
        assert args.num_hps == 1, "If window_shape should be estimated automatically, the number of hps per box can only be 1"

    return output_dataset_dir,pflotran_file,settings

def call_pflotran(avg_time_per_sim, run_id:int, tmp_output:bool=False):
    start_sim = time.perf_counter()
    print(f"Starting PFLOTRAN simulation of RUN {run_id} at {time.ctime()}") # TODO logging.info
    output_extension = " -screen_output off" if not tmp_output else ""
    os.system(f"mpirun -n 32 {os.environ['PFLOTRAN_DIR']}/bin/pflotran -output_prefix pflotran{output_extension}")
    avg_time_per_sim += time.perf_counter() - start_sim
    print(f"Finished PFLOTRAN simulation at {time.ctime()} after {(time.perf_counter() - start_sim)//60} minutes and {((time.perf_counter() - start_sim)%60):.1f} seconds") # TODO logging.info


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
    output_dataset_dir = Path("outputs") 
    output_dataset_dir.mkdir(exist_ok=True, parents=True)
    run_simulation(output_dataset_dir, args, run_ids)
