#!/bin/bash

## run script by "bash ../<name_of_script> (file should be in parent directory or otherwise name full path to script) 
## <CLA_NUMBER_VARIATIONS_PRESSURE> <CLA_PRESSURE_CASE> <CLA_NUMBER_VARIATIONS_PERMEABILITY> <CLA_PERM_CASE> <CLA_DIMENSIONS> <CLA_NAME> <CLA_VISUALISATION>"
## always start from same directory as pflotran.in file

#TODO user $PFLOTRAN_DIR neu setzen, wenn man in einer neuen Umgebung arbeitet (in ~/.zshrc or bashrc or similar)
# remote: after spack installation: export PFLOTRAN_DIR="/home/pelzerja/pelzerja/spack/opt/spack/linux-ubuntu20.04-zen2/gcc-9.4.0/pflotran-4.0.1-yilpwmx73suky3faq3ez4okbnpmnaezm"

#command line arguments
args=("$@")
if [ ${#args[@]} = 0 ];
then
    args=(10 1D 10 iso 3D default_valued_dataset)
    echo "No command line arguments given. Using default values:"
    echo "<Number of pressure variations>       default: ${args[0]}"
    echo "<Pressure case> (1D / 2D)             default: ${args[1]}"
    echo "<Number permeability variations>      default: ${args[2]}"
    echo "<Perm case> (Iso / vary)              default: ${args[3]}"
    echo "<Dimensions of domain> (2D / 3D)      default: ${args[4]}"
    echo "<Name of folder for dataset>          default: ${args[5]}"
    echo "<Visualization?> (vis / -)            default: ${args[6]}"
fi
CLA_NUMBER_VARIATIONS_PRESSURE=${args[0]} # expects the number of desired variations of the pressure field in the dataset
CLA_PRESSURE_CASE=${args[1]} # expects a string: "2D" or "1D" (for the pressure field)
CLA_NUMBER_VARIATIONS_PERMEABILITY=${args[2]} # expects the number of desired variations of the permeability field in the dataset
CLA_PERM_CASE=${args[3]} # expects a string: "iso" or "vary" (for the permeability field)
CLA_DIMENSIONS=${args[4]} # expects a string: "2D" or "3D"
CLA_NAME=${args[5]} # expects a string with the name of the dataset
CLA_VISUALISATION=${args[6]} # expects "vis" or "no_vis"

if [ ! "$CLA_PRESSURE_CASE" = "1D" ] && [ ! "$CLA_PRESSURE_CASE" = "2D" ];
then
    echo "CLA_PRESSURE_CASE must be 1D or 2D"
    exit 1
fi
if [ ! "$CLA_DIMENSIONS" = "2D" ] && [ ! "$CLA_DIMENSIONS" = "3D" ];
then
    echo "CLA_DIMENSIONS must be 2D or 3D"
    exit 1
fi

echo working at $(date) on folder $(pwd)
# dataset generation

# check whether output folder exists else define
OUTPUT_DATASET_DIR=$CLA_NAME
if [ ! -d $OUTPUT_DATASET_DIR ];
then
    mkdir $OUTPUT_DATASET_DIR
    echo ...$OUTPUT_DATASET_DIR folder is created
fi
# folder for files like pflotran.in, pressure_values.txt and perm_field_parameters.txt, mesh.uge etc.
if [ ! -d $OUTPUT_DATASET_DIR/inputs ];
then
    mkdir $OUTPUT_DATASET_DIR/inputs
    echo ...$OUTPUT_DATASET_DIR/inputs folder is created
fi
if [ "$CLA_DIMENSIONS" = "2D" ];
then
    cp dummy_dataset/settings_2D.yaml $OUTPUT_DATASET_DIR/inputs/settings.yaml
else
    cp dummy_dataset/settings.yaml $OUTPUT_DATASET_DIR/inputs/settings.yaml
fi

if [ "$CLA_PERM_CASE" = "vary" ]; 
then
    cp dummy_dataset/pflotran_vary_perm.in pflotran.in
else
    cp dummy_dataset/pflotran_iso_perm.in pflotran.in
fi

# make grid files
python3 scripts/create_grid_unstructured.py $OUTPUT_DATASET_DIR/inputs/ $(pwd)

MIN_VARIATIONS_PRESSURE=$CLA_NUMBER_VARIATIONS_PRESSURE #1 #5 #100  # calc parameters, read them for PRESSURE
python3 scripts/script_calc_pressure_variation.py $MIN_VARIATIONS_PRESSURE $OUTPUT_DATASET_DIR/inputs $CLA_PRESSURE_CASE
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PRESSURE=($(cat ${OUTPUT_DATASET_DIR}/inputs/pressure_values.txt))'
# number of datapoints can differ from number of wished datapoints in 2D case (see calc_pressure_variation.py)

# calculate permeability fields
len_perm=$CLA_NUMBER_VARIATIONS_PERMEABILITY # calc parameters, read them for PERMEABILITY
# TODO later set random_bool in settings.yaml to True
if [ "$CLA_PERM_CASE" = "vary" ]; 
then
    python3 scripts/create_permeability_field.py INFO $len_perm $(pwd) $OUTPUT_DATASET_DIR
fi

run_id=0

len=${#PRESSURE[@]}
i=0
while [ $i -lt $len ];
do
    # TODO random combination of pressure+permeability field or all combinations? currently: all combinations
    j=0
    while [ $j -lt $len_perm ];
    do  
        current_id=-1 #79 # TODO set to -1 if you want to start from the beginning
        if [ $j -gt $current_id ];
        then

            # calculate pressure files
            if [ "$CLA_PRESSURE_CASE" = "1D" ]; 
            then
                python3 scripts/script_write_pressure_to_pflotran_in_file.py INFO ${PRESSURE[$i]}
            else # 2D case
                python3 scripts/script_write_pressure_to_pflotran_in_file.py INFO ${PRESSURE[$i]} ${PRESSURE[$i+1]}
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

            # copy next permeability field file to pflotran.in folder
            if [ "$CLA_PERM_CASE" = "vary" ]; 
            then
                python3 scripts/script_copy_next_perm_field.py $OUTPUT_DATASET_DIR $j $NAME_OF_RUN
            fi
        
            echo starting PFLOTRAN simulation of $NAME_OF_RUN at $(date)
            # to DEBUG the simulation turn screen_output on
            # mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off # local version
            mpirun -n 16 $PFLOTRAN_DIR/pflotran -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off # remote version (pcsgs05)
            echo finished PFLOTRAN simulation at $(date)

            cp interim_pressure_gradient.txt $OUTPUT_DATASET_RUN_DIR/pressure_gradient.txt

            # # call visualisation
            if [ "$CLA_VISUALISATION" = "vis" ]; 
            then
                if [ "$CLA_DIMENSIONS" = "2D" ];
                then
                    python3 scripts/visualisation_self.py $OUTPUT_DATASET_DIR $OUTPUT_DATASET_RUN_DIR "2D"
                else
                    python3 scripts/visualisation_self.py $OUTPUT_DATASET_DIR $OUTPUT_DATASET_RUN_DIR
                    python3 scripts/visualisation_self.py $OUTPUT_DATASET_DIR $OUTPUT_DATASET_RUN_DIR "top_hp"
                fi
                echo ...visualisation of $NAME_OF_RUN is done
            fi
        fi
        j=$(( $j + 1 ))
        run_id=$(( $run_id + 1 ))
    done
    i=$(( $i + 1 ))
done

mv pflotran.in $OUTPUT_DATASET_DIR/inputs/pflotran_copy.in
rm interim_pressure_gradient.txt
rm -rf {east,west,south,north}.ex heatpump_inject1.vs mesh.uge settings.yaml
if [ "$CLA_PERM_CASE" = "vary" ];
then
    rm interim_permeability_field.h5
    rm -r $OUTPUT_DATASET_DIR/permeability_fields
fi