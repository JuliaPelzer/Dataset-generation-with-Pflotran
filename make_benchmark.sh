#!/bin/bash

## run script by "bash make_benchmark.sh" optional: [number of datapoints] [name of dataset] [visualisation?]
#TODO user $PFLOTRAN_DIR neu setzen, wenn man in einer neuen Umgebung arbeitet (in ~/.zshrc or bashrc or similar)
# remote: after spack installation: export PFLOTRAN_DIR="/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-4.0.1-yilpwmx73suky3faq3ez4okbnpmnaezm"

# BENCHMARK
CLA_BENCHMARK=true # set to true if you want to produce the benchmark dataset (defined in diss.tex)

if $CLA_BENCHMARK;
then
    echo Benchmark dataset will be generated...
    CLA_DATAPOINTS=benchmark_3_testcases
    CLA_DIMENSIONS=2D
    CLA_NAME=benchmark_dataset
    CLA_VISUALISATION=vis
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
    cp dummy_dataset_benchmark/settings_2D.yaml $OUTPUT_DATASET_DIR/inputs/settings.yaml
else
    cp dummy_dataset_benchmark/settings.yaml $OUTPUT_DATASET_DIR/inputs/settings.yaml
fi

cp dummy_dataset_benchmark/pflotran_iso_perm.in pflotran.in

# make grid files
python3 scripts/create_grid_unstructured.py $OUTPUT_DATASET_DIR/inputs/ $(pwd)

python3 scripts/script_make_benchmark_testcases.py $OUTPUT_DATASET_DIR/inputs $CLA_DATAPOINTS
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PRESSURE=($(cat ${OUTPUT_DATASET_DIR}/inputs/pressure_values.txt))'
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PERM=($(cat ${OUTPUT_DATASET_DIR}/inputs/permeability_values.txt))'

run_id=0
len=${#PRESSURE[@]}
i=0
while [ $i -lt $len ];
do
    # TODO random combination of pressure+permeability field or all combinations? currently: all combinations
    # calculate pressure files
    python3 scripts/script_write_benchmark_to_pflotran_in_file.py INFO ${PRESSURE[$i]} ${PERM[$i]}

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
    mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off # local version
    # mpirun -n 16 $PFLOTRAN_DIR/pflotran -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off # remote version (pcsgs05)
    echo "finished PFLOTRAN simulation at $(date)"

    cp interim_pressure_gradient.txt $OUTPUT_DATASET_RUN_DIR/pressure_gradient.txt
    cp interim_iso_permeability.txt $OUTPUT_DATASET_RUN_DIR/permeability_iso.txt

    # # call visualisation
    if [ "$CLA_VISUALISATION" = "vis" ];
    then
        python3 scripts/visualisation_self.py $OUTPUT_DATASET_DIR $OUTPUT_DATASET_RUN_DIR "2D"
        echo "...visualisation of $NAME_OF_RUN is done"
    fi
    run_id=$(( $run_id + 1 ))
    i=$(( $i + 1 ))
done

mv pflotran.in $OUTPUT_DATASET_DIR/inputs/pflotran_copy.in
rm interim_pressure_gradient.txt
rm interim_iso_permeability.txt
rm -rf {east,west,south,north}.ex heatpump_inject1.vs mesh.uge settings.yaml