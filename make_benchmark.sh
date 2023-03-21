#!/bin/bash

## run script by "bash make_benchmark.sh" optional: [number of datapoints] [name of dataset] [visualisation?]
#TODO user $PFLOTRAN_DIR neu setzen, wenn man in einer neuen Umgebung arbeitet (in ~/.zshrc or bashrc or similar)
# remote: after spack installation: export PFLOTRAN_DIR="/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-4.0.1-yilpwmx73suky3faq3ez4okbnpmnaezm"

# BENCHMARK
CLA_BENCHMARK=true # set to true if you want to produce the benchmark dataset (defined in diss.tex)

if $CLA_BENCHMARK;
then
    echo Benchmark dataset will be generated...
    CLA_DATAPOINTS=300            #benchmark_4_testcases
    CLA_DIMENSIONS=2D
    CLA_NAME=benchmark_dataset_2d_300dp_vary_hp_loc
    CLA_VISUALISATION=no_vis
    CLA_HP_VARIATION=true   # needs to be "false" to not get HP-location-variations
fi

args=("$@")
if [ ! ${#args[@]} = 0 ]; then
    CLA_DATAPOINTS=${args[0]}
    CLA_NAME=${args[1]}
    CLA_VISUALISATION=${args[2]}
fi

echo working at $(date) on folder $(pwd)
# dataset generation

# check whether output folder exists else define
OUTPUT_DATASET_DIR=$CLA_NAME
if [ ! -d $OUTPUT_DATASET_DIR ];
then
    mkdir $OUTPUT_DATASET_DIR
    echo "...$OUTPUT_DATASET_DIR folder is created"
fi
# folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
if [ ! -d $OUTPUT_DATASET_DIR/inputs ];
then
    mkdir $OUTPUT_DATASET_DIR/inputs
    echo "...$OUTPUT_DATASET_DIR/inputs folder is created"
fi

if [ "$CLA_DIMENSIONS" = "2D" ];
then
    cp dummy_dataset_benchmark_squarish/settings_2D.yaml $OUTPUT_DATASET_DIR/inputs/settings.yaml
else
    cp dummy_dataset_benchmark_squarish/settings_3D_fine.yaml $OUTPUT_DATASET_DIR/inputs/settings.yaml
    # does not exist
fi

cp dummy_dataset_benchmark_squarish/pflotran_iso_perm.in pflotran.in

# make grid files
python3 scripts/create_grid_unstructured.py $OUTPUT_DATASET_DIR/inputs/

if [ "$CLA_HP_VARIATION" != "false" ] && [ "$CLA_DATAPOINTS" != "benchmark_4_testcases" ];
then
    python3 scripts/script_calc_loc_hp_variation_2d.py $CLA_DATAPOINTS $OUTPUT_DATASET_DIR/inputs
    IFS=$'\r\n' GLOBIGNORE='*' command eval  'HP_X=($(cat ${OUTPUT_DATASET_DIR}/inputs/locs_hp_x.txt))'
    IFS=$'\r\n' GLOBIGNORE='*' command eval  'HP_Y=($(cat ${OUTPUT_DATASET_DIR}/inputs/locs_hp_y.txt))'
fi

python3 scripts/script_make_benchmark_testcases.py $OUTPUT_DATASET_DIR/inputs $CLA_DATAPOINTS
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PRESSURE=($(cat ${OUTPUT_DATASET_DIR}/inputs/pressure_values.txt))'
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PERM=($(cat ${OUTPUT_DATASET_DIR}/inputs/permeability_values.txt))'

run_id=0
len=${#PRESSURE[@]}
i=0
while [ $i -lt $len ];
do
    # calculate pressure and permeability files
    if [ "$CLA_HP_VARIATION" != "false" ];
    then
        python3 scripts/write_benchmark_parameters_input_files.py INFO ${PRESSURE[$i]} ${PERM[$i]} ${HP_X[$i]} ${HP_Y[$i]}
    else
        python3 scripts/write_benchmark_parameters_input_files.py INFO ${PRESSURE[$i]} ${PERM[$i]}
    fi

    # create run folder
    NAME_OF_RUN="RUN_${run_id}"
    OUTPUT_DATASET_RUN_DIR="${OUTPUT_DATASET_DIR}/${NAME_OF_RUN}"
    OUTPUT_DATASET_RUN_PREFIX="${OUTPUT_DATASET_RUN_DIR}/pflotran"
    # check whether output folder exists else define
    if [ ! -d $OUTPUT_DATASET_RUN_DIR ]
    then
        mkdir $OUTPUT_DATASET_RUN_DIR
    fi

    echo "starting PFLOTRAN simulation of $NAME_OF_RUN at $(date)"
    # mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off # local version
    PFLOTRAN_DIR=/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-3.0.2-toidqfdeqa4a5fbnn5yz4q7hm4adb6n3/bin
    mpirun -n 16 $PFLOTRAN_DIR/pflotran -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off # remote version (pcsgs05)
    echo "finished PFLOTRAN simulation at $(date)"

    cp interim_pressure_gradient.txt $OUTPUT_DATASET_RUN_DIR/pressure_gradient.txt
    cp interim_iso_permeability.txt $OUTPUT_DATASET_RUN_DIR/permeability_iso.txt
    cp heatpump_inject1.vs $OUTPUT_DATASET_RUN_DIR/heatpump_inject1.vs

    # # call visualisation
    if [ "$CLA_VISUALISATION" = "vis" ];
    then
        python3 scripts/visualisation_self.py $OUTPUT_DATASET_DIR $OUTPUT_DATASET_RUN_DIR $CLA_DIMENSIONS
        echo "...visualisation of $NAME_OF_RUN is done"
    fi
    run_id=$(( $run_id + 1 ))
    i=$(( $i + 1 ))
done

mv pflotran.in $OUTPUT_DATASET_DIR/inputs/pflotran_copy.in
rm interim_pressure_gradient.txt
rm interim_iso_permeability.txt
rm -rf {east,west,south,north}.ex heatpump_inject1.vs mesh.uge settings.yaml