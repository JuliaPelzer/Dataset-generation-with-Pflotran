import argparse
import logging
import datetime
import os
import shutil
import yaml
import pathlib
import numpy as np

from scripts.create_grid_unstructured import create_all_grid_files
from scripts.calc_loc_hp_variation_2d import calc_loc_hp_variation_2d
from scripts.calc_p_and_K import calc_pressure_and_perm_fields
from scripts.create_permeability_field import create_perm_fields
from scripts.make_general_settings import load_yaml, save_yaml
from scripts.write_benchmark_parameters_input_files_parallel import write_parameter_input_files
from scripts.visualisation import plot_sim

def make_parameter_set(args, confined_aquifer_bool: bool = False):
    output_dataset_dir = args.name

    # save args as yaml file
    with open(f"{output_dataset_dir}/inputs/args.yaml", "w") as outfile:
        yaml.dump(vars(args), outfile, default_flow_style=False)

    # copy settings file
    shutil.copy("dummy_dataset_pipeline_large/settings_2D_large.yaml", f"{output_dataset_dir}/inputs/settings.yaml")
    if args.benchmark or (args.num_hps - args.vary_hp_amount > 0):
        shutil.copy("dummy_dataset_pipeline_large/benchmark_locs_hps.yaml", f"{output_dataset_dir}/inputs/benchmark_locs_hps.yaml")

    # getting settings
    settings = load_yaml(f"{output_dataset_dir}/inputs")
    # make grid files
    path_interim_pflotran_files = pathlib.Path(f"{output_dataset_dir}/pflotran_inputs")
    path_interim_pflotran_files.mkdir(parents=True)
    settings = create_all_grid_files(settings, confined=confined_aquifer_bool, path_to_output=path_interim_pflotran_files)
    save_yaml(settings, f"{output_dataset_dir}/inputs")

    # potentially calc 1 or 2 hp locations
    if args.vary_hp:
        calc_loc_hp_variation_2d(args.num_dp, f"{output_dataset_dir}/inputs", f"{output_dataset_dir}/pflotran_inputs", args.num_hps, settings, benchmark_bool=args.benchmark, num_hps_to_vary = args.vary_hp_amount)
    
    # make benchmark testcases
    _, perms = calc_pressure_and_perm_fields(args.num_dp, f"{output_dataset_dir}/inputs", args.vary_perm, benchmark_bool=args.benchmark)
    if args.vary_perm:
        create_perm_fields(args.num_dp, output_dataset_dir, settings, perms_min_max=perms)
        # TODO f"{output_dataset_dir}/inputs" ?
    return settings
    
def load_inputs_subset(run_ids: list, origin_folder: str, num_hp: int):
    # initialize lists
    pressures = []
    perms = []
    locs_hps = []

    # load files
    perm_file = "permeability_values.txt"
    # TODO or vary perm laden
    file = open(f"{origin_folder}/{perm_file}", "r")
    for line_nr, line in enumerate(file):
        if line_nr in run_ids:
            perms.append(float(line))
    file.close()

    pressure_file = "pressure_values.txt"
    file = open(f"{origin_folder}/{pressure_file}", "r")
    for line_nr, line in enumerate(file):
        if line_nr in run_ids:
            pressures.append(float(line))
    file.close()

    for hp_id in range(1,num_hp+1):
        hp_fixed = f"locs_hp_{hp_id}_fixed.txt"
        hp_x = f"locs_hp_x_{hp_id}.txt"
        hp_y = f"locs_hp_y_{hp_id}.txt"
        try:
            file = open(f"{origin_folder}/{hp_fixed}", "r")
            # TODO check whether line shift
            for line_nr, line in enumerate(file):
                if line_nr in run_ids:
                    locs_hps.append([float(pos) for pos in line.split()])
            file.close()
        except:
            x = []
            file_x = open(f"{origin_folder}/{hp_x}", "r")
            for line_nr, line in enumerate(file_x):
                if line_nr in run_ids:
                    x.append(float(line))
            file_x.close()
            y = []
            file_y = open(f"{origin_folder}/{hp_y}", "r")
            for line_nr, line in enumerate(file_y):
                if line_nr in run_ids:
                    y.append(float(line))
            file_y.close()
            locs = np.array([x, y]).T
            for id, hp in enumerate(locs):
                locs_hps[id] = [locs_hps[id], list(hp)]

    return np.array(pressures), np.array(perms), np.array(locs_hps)

def run_simulation(args, run_ids: list):
    assert not args.vary_perm, "Parallel version not yet for varying permeability implemented"
    logging.info(f"Working at {datetime.datetime.now()} on folder {os.getcwd()}")

    confined_aquifer=False 
    if args.benchmark:
        args = set_benchmark_args(args)

    if args.num_hps > 1:
        assert args.vary_hp, f"If number of heatpumps is larger than 1, vary_hp must be True"
    
    # check whether output folder exists else define
    output_dataset_dir = pathlib.Path(args.name)
    output_dataset_dir.mkdir(parents=True, exist_ok=True)

    # folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
    output_dataset_dir_general_inputs = pathlib.Path(output_dataset_dir, "inputs")
    if not os.path.isdir(output_dataset_dir_general_inputs):
        print("tes")
        output_dataset_dir_general_inputs.mkdir(parents=True)
        logging.info(f"...{output_dataset_dir}/inputs folder is created")

        # ONCE PER DATASET: generate set of perms, pressures and hp locations
        settings = make_parameter_set(args, confined_aquifer_bool=confined_aquifer)
        print("deo")
    else:
        logging.info(f"...{output_dataset_dir}/inputs folder already exists")

        # get settings
        settings = load_yaml(f"{output_dataset_dir}/inputs")

    pflotran_file = set_pflotran_file(args, confined_aquifer=confined_aquifer)

    # TODO
    pressures, perms, locs_hps = load_inputs_subset(run_ids, output_dataset_dir_general_inputs, args.num_hps)
    
    # TODO check whether all files erstellt, die gebraucht, aber auch im richtigen Ordner!!
    
    top_level_dir = os.getcwd()
    # make run folders
    for run_id in run_ids:
        output_dataset_run_dir = pathlib.Path(f"{output_dataset_dir}/RUN_{run_id}")
        # output_dataset_run_dir.mkdir(parents=True)

        # copy pflotran.in file, which one - depends
        shutil.copytree(f"{output_dataset_dir}/pflotran_inputs", f"{output_dataset_run_dir}") # TODO in special folder? - so later better to remove? or keep or remove all?
        shutil.copy(pflotran_file, f"{output_dataset_run_dir}/pflotran.in")

        if not args.vary_hp:
            write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm)
        else:
            if args.num_hps > 0:
                write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm, settings, locs_hps[run_ids.index(run_id)])
            else:
                write_parameter_input_files(pressures[run_ids.index(run_id)], perms[run_ids.index(run_id)], output_dataset_dir, run_id, args.vary_perm)

        os.chdir(output_dataset_run_dir)
        time_now = datetime.datetime.now()
        logging.info(f"Starting PFLOTRAN simulation of RUN {run_id} at {time_now}")
        PFLOTRAN_DIR="/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-3.0.2-toidqfdeqa4a5fbnn5yz4q7hm4adb6n3/bin"
        os.system(f"mpirun -n 16 {PFLOTRAN_DIR}/pflotran -output_prefix pflotran -screen_output off")
        logging.info(f"Finished PFLOTRAN simulation at {datetime.datetime.now()} after {datetime.datetime.now() - time_now}")

        # call visualisation
        if args.visu:
            plot_sim(".", settings, case="2D", confined=confined_aquifer)
            logging.info(f"...visualisation of RUN {run_id} is done")
        
        # clean up
        shutil.move("pflotran.in", f"../inputs/pflotran_copy.in")
        for file in ["regions_hps.txt", "strata_hps.txt", "conditions_hps.txt", "east.ex", "west.ex", "south.ex", "north.ex", "top_cover.txt", "bottom_cover.txt", "heatpump_inject1.vs", "heatpump_inject2.vs", "mesh.uge", "settings.yaml", "interim_pressure_gradient.txt", "interim_permeability_field.h5", "interim_iso_permeability.txt"]:
            try:
                os.remove(file)
            except:
                continue

        os.chdir(top_level_dir)

    if args.vary_perm:
        shutil.rmtree(f"{output_dataset_dir}/permeability_fields")
    if not args.benchmark:
        try:
            os.remove(f"{output_dataset_dir}/inputs/benchmark_locs_hps.yaml")
        except:
            pass
    
    logging.info(f"Finished dataset creation at {datetime.datetime.now()}")

def set_benchmark_args(args):
    args.num_dp = 1
    args.visu = True
    args.vary_hp = True
    args.vary_hp_amount = 0
    args.num_hps = 2
    args.vary_perm = False #True
    logging.info(f"Running benchmark testcases with settings: {args}")
    return args

def set_pflotran_file(args, confined_aquifer):
    # build pflotran file name
    perm_case = "vary" if args.vary_perm else "iso"
    confined_extension = "_confined" if confined_aquifer else ""
    hps_extension = f"_xhps" if args.num_hps >= 1 else f"_{args.num_hps}hps"
    pflotran_file = f"dummy_dataset_pipeline_large/pflotran_{perm_case}_perm{hps_extension}{confined_extension}.in"
    return pflotran_file

def just_visualize(args):
    output_dataset_dir = args.name
    settings = load_yaml(f"{output_dataset_dir}/inputs")
    confined_aquifer = False

    for run_id in range(4): # in case of testcases_4
        output_dataset_run_dir = f"{output_dataset_dir}/RUN_{run_id}"
        plot_sim(output_dataset_run_dir, settings, case="2D", confined=confined_aquifer)
        logging.info(f"...visualisation of RUN {run_id} is done")

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", type=bool, default=False)
    parser.add_argument("--num_dp", type=int, default=1) #int = 100 # number of datapoints
    parser.add_argument("--name", type=str, default="default") #benchmark_large_vary_perm_2hps")
    parser.add_argument("--visu", type=bool, default=False) # visualisation
    parser.add_argument("--num_hps", type=int, default=0)   # number of hp locations
    parser.add_argument("--vary_hp", type=bool, default=False)  # vary hp location
    parser.add_argument("--vary_hp_amount", type=int, default=0) # how many hp locations should be varied
    parser.add_argument("--vary_perm", type=bool, default=False)    # vary permeability
    parser.add_argument("--id_start", type=int, default=0) # start id
    parser.add_argument("--id_end", type=int, default=1000) # end id

    args = parser.parse_args()

    run_ids = list(range(args.id_start, args.id_end))
    run_simulation(args, run_ids)

    # just_visualize(args)