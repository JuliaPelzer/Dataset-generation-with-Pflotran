## run script by "bash ../<name_of_script> (file should be in parent directory or otherwise name full path to script) <CLA_DEBUG> <CLA_NUMBER_DATAPOINTS> <CLA_NAME> <CLA_VISUALISATION>"
## always start from same directory as pflotran.in file
#TODO user $PFLOTRAN_DIR neu setzen, wenn man in einer neuen Umgebung arbeitet (in ~/.zshrc or bashrc or similar)

#command line arguments
args=("$@")
CLA_DEBUG=${args[0]} # expects "debug" or "no_debug"
CLA_NUMBER_DATAPOINTS=${args[1]} # expects the number of desired datapoints in the dataset
CLA_NAME=${args[2]} # expects an string with the name of the dataset
CLA_VISUALISATION=${args[3]} # expects "vis" or "no_vis"

echo working at $(date) on folder $(pwd)
# dataset generation

# check whether output folder exists else define
OUTPUT_DATASET_DIR=$CLA_NAME #"uniformly_distributed_data_velo"
if [ ! -d $OUTPUT_DATASET_DIR ]
then
    mkdir $OUTPUT_DATASET_DIR
    echo ...$OUTPUT_DATASET_DIR folder is created
fi

# LOOP
# calc parameters, read them for PRESSURE_XY
MIN_DATASET_POINTS=$CLA_NUMBER_DATAPOINTS #1 #5 #100
python3 ../scripts/scripts_pressure/script_calc_pressure_variation_working_copy.py $MIN_DATASET_POINTS $OUTPUT_DATASET_DIR
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PRESSURE_XY=($(cat ${OUTPUT_DATASET_DIR}/pressure_array_2D_xy.txt))'

cp pflotran.in $OUTPUT_DATASET_DIR/pflotran.in

i=0
len=${#PRESSURE_XY[@]}
# len=$(( $len /2 ))
# number of datapoints can differ from number of wished datapoints in 2D case (see calc pressure_variation)

# len_perm = 1
# # calculate permeability fields
# python3 ../scripts/scripts_permeability/create_permeability_field.py INFO $len_perm "test" "False"

while [ $i -lt $len ];
do
    # calculate pressure files
    python3 ../scripts/scripts_pressure/script_write_pressure_to_pflotran_in_file.py INFO ${PRESSURE_XY[$i]} ${PRESSURE_XY[$i+1]}

    # j=0
    # while [ $j -lt $len_perm ];
    # do
    #     # copy next permeability field file to pflotran.in folder
        
    #     cp ../vary_permeability/perm_field_1.txt $OUTPUT_DATASET_DIR/perm_field_1.txt
    #     j=$(( $j + 1 ))
    # done

    # call pflotran
    NAME_OF_RUN="RUN_$(($i/2))"
    OUTPUT_DATASET_RUN_DIR="${OUTPUT_DATASET_DIR}/${NAME_OF_RUN}"
    OUTPUT_DATASET_RUN_PREFIX="${OUTPUT_DATASET_RUN_DIR}/pflotran"
    echo starting PFLOTRAN simulation of $NAME_OF_RUN at $(date)

    # check whether output folder exists else define
    if [ ! -d $OUTPUT_DATASET_RUN_DIR ]
    then
        mkdir $OUTPUT_DATASET_RUN_DIR
        #echo ...$OUTPUT_DATASET_RUN_DIR folder is created
    fi
    
    if [ "$CLA_DEBUG" = "debug" ];
    then
    # DEBUG simulation (one single run)
        mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -$OUTPUT_DATASET_DIR/pflotran.in -output_prefix $OUTPUT_DATASET_RUN_PREFIX
    else
        mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -$OUTPUT_DATASET_DIR/pflotran.in -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off
    fi

    cp interim_pressure_gradient.txt $OUTPUT_DATASET_RUN_DIR/pressure_gradient.txt
    echo finished PFLOTRAN simulation at $(date)

    # call visualisation
    # problem with visualisation, if less than 50 pics TODO
    bash ../scripts/scripts_visualisation/call_visualisation.sh $CLA_VISUALISATION $OUTPUT_DATASET_RUN_DIR

    # pressure consists of two values, so only half of the number of pressure values in loop
    i=$(( $i + 2 ))
done

rm interim_pressure_gradient.txt
