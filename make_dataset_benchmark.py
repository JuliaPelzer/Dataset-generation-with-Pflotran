import argparse
import logging
import datetime
import os
import shutil

from scripts.create_grid_unstructured import create_all_grid_files
from scripts.calc_loc_hp_variation_2d import calc_loc_hp_variation_2d
from scripts.calc_p_and_K import calc_pressure_and_perm_fields
from scripts.create_permeability_field import create_perm_fields
from scripts.make_general_settings import load_yaml
from scripts.write_benchmark_parameters_input_files import write_parameter_input_files
from scripts.visualisation import plot_sim

def run_simulation(args):

    logging.info(f"Working at {datetime.datetime.now()} on folder {os.getcwd()}")
    assert args.number_hps in [0,1,2], f"Number of heatpumps must be 0, 1 or 2 but it is {args.number_hps}"
    if args.number_hps > 1:
        assert args.hp_variation, f"If number of heatpumps is larger than 0, hp_variation must be True"

    confined_aquifer = False

    # dataset generation
    # check whether output folder exists else define
    output_dataset_dir = args.name
    if not os.path.isdir(output_dataset_dir):
        os.mkdir(output_dataset_dir)
        logging.info(f"...{output_dataset_dir} folder is created")

    # folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
    if not os.path.isdir(os.path.join(output_dataset_dir, "inputs")):
        os.mkdir(os.path.join(output_dataset_dir, "inputs"))
        logging.info(f"...{output_dataset_dir}/inputs folder is created")

    # copy settings file
    if args.dimensions == "2D":
        shutil.copy("dummy_dataset_benchmark/settings_2D.yaml", f"{output_dataset_dir}/inputs/settings.yaml")

    else:
        shutil.copy("dummy_dataset_benchmark/settings_3D_fine.yaml", f"{output_dataset_dir}/inputs/settings.yaml")

    # copy pflotran.in file, which one - depends
    perm_case = "vary" if args.perm_variation else "iso"
    confined_extension = "_confined" if confined_aquifer else ""
    hps_extension = f"_{args.number_hps}hps"
    pflotran_file = f"dummy_dataset_benchmark/pflotran_{perm_case}_perm{hps_extension}{confined_extension}.in"
    shutil.copy(pflotran_file, "pflotran.in")

    # getting settings
    settings = load_yaml(f"{output_dataset_dir}/inputs")
    # make grid files
    settings = create_all_grid_files(settings, confined=confined_aquifer)

    # potentially calc 1 or 2 hp locations
    if args.hp_variation:
        locs_hps = calc_loc_hp_variation_2d(args.num_datapoints, f"{output_dataset_dir}/inputs", args.number_hps, settings)
    
    # make benchmark testcases
    pressures, perms = calc_pressure_and_perm_fields(args.num_datapoints, f"{output_dataset_dir}/inputs", args.perm_variation)
    if args.perm_variation:
        create_perm_fields(args.num_datapoints, output_dataset_dir, settings, perms_min_max=perms)
    
    # make run folders
    for run_id in range(len(pressures)): #should only differ in case of benchmark_4_testcases from CLA_DATAPOINTS
        output_dataset_run_dir = f"{output_dataset_dir}/RUN_{run_id}"
        if not os.path.isdir(output_dataset_run_dir):
            os.mkdir(output_dataset_run_dir)

        if not args.hp_variation:
            write_parameter_input_files(pressures[run_id], perms[run_id], output_dataset_dir, run_id, args.perm_variation)
        elif args.number_hps > 0:
            write_parameter_input_files(pressures[run_id], perms[run_id], output_dataset_dir, run_id, args.perm_variation, settings, locs_hps[run_id])
        else:
            raise ValueError("If hp_variation is True, number_hps must be larger than 0")

        logging.info(f"Starting PFLOTRAN simulation of RUN {run_id} at {datetime.datetime.now()}")
        remote = True
        if not remote:
            os.system(f"mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -output_prefix {output_dataset_run_dir}/pflotran -screen_output off")
        else:
            PFLOTRAN_DIR="/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-3.0.2-toidqfdeqa4a5fbnn5yz4q7hm4adb6n3/bin"
            os.system(f"mpirun -n 16 {PFLOTRAN_DIR}/pflotran -output_prefix {output_dataset_run_dir}/pflotran -screen_output off")
        logging.info(f"Finished PFLOTRAN simulation at {datetime.datetime.now()}")

        # call visualisation
        if args.visualisation:
            plot_sim(output_dataset_run_dir, settings, case="2D", confined=confined_aquifer)
            logging.info(f"...visualisation of RUN {run_id} is done")

    
    # clean up
    shutil.move("pflotran.in", f"{output_dataset_dir}/inputs/pflotran_copy.in")
    for file in ["east.ex", "west.ex", "south.ex", "north.ex", "top_cover.txt", "bottom_cover.txt", "heatpump_inject1.vs", "heatpump_inject2.vs", "mesh.uge", "settings.yaml", "interim_pressure_gradient.txt", "interim_permeability_field.h5", "interim_iso_permeability.txt"]:
        try:
            os.remove(file)
        except:
            continue
    if args.perm_variation:
        shutil.rmtree(f"{output_dataset_dir}/permeability_fields")

def just_visualize(args):
    output_dataset_dir = args.name
    settings = load_yaml(f"{output_dataset_dir}/inputs")
    confined_aquifer = False

    for run_id in range(4): # in case of testcases_4
        output_dataset_run_dir = f"{output_dataset_dir}/RUN_{run_id}"
        plot_sim(output_dataset_run_dir, settings, case=args.dimensions, confined=confined_aquifer)
        logging.info(f"...visualisation of RUN {run_id} is done")

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_datapoints", type=int, default=1) #int 100) #str benchmark_4_testcases
    parser.add_argument("--dimensions", type=str, default="2D")
    parser.add_argument("--name", type=str, default="default") #benchmark_dataset_2d_100dp_vary_perm")
    parser.add_argument("--visualisation", type=bool, default=True)
    parser.add_argument("--hp_variation", type=bool, default=False)
    parser.add_argument("--number_hps", type=int, default=0)
    parser.add_argument("--perm_variation", type=bool, default=False)

    args = parser.parse_args()

    run_simulation(args)
    # just_visualize(args)