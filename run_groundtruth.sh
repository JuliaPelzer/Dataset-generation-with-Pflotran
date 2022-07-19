## run script by "bash ../<name_of_script> (file should be in parent directory or otherwise name full path to script) <CLA_DEBUG> <CLA_NUMBER_DATAPOINTS> <CLA_NAME> <CLA_VISUALISATION>"
## always start from same directory as pflotran.in file
## does not expect debug mode + dataset mode ! either debug+single run or dataset and no debugging

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
# calc parameters, read them for pressure_y
DATASET_POINTS=$CLA_NUMBER_DATAPOINTS #1 #5 #100
python3 script_calc_parameter_variation.py $DATASET_POINTS
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PRESSURE_Y=($(cat parameter_values_pressure_y.txt))'

i=0
len=${#PRESSURE_Y[@]}

cp pflotran.in $OUTPUT_DATASET_DIR/pflotran.in
    
while [ $i -lt $len ];
do
    # calculate python stuff
    python3 script_pflotran_in_file_generation.py INFO ${PRESSURE_Y[$i]}

    # call pflotran
    NAME_OF_RUN="RUN_${i}"
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

    cp pressure_gradient.txt $OUTPUT_DATASET_RUN_DIR/pressure_gradient.txt
    echo finished PFLOTRAN simulation at $(date)

    # call visualisation
    # problem with visualisation, if less than 50 pics TODO
    bash ../scripts_visualisation/call_visualisation.sh $CLA_VISUALISATION $OUTPUT_DATASET_RUN_DIR

    i=$(( $i + 1 ))
done

cp parameter_values_pressure_y.txt $OUTPUT_DATASET_DIR/parameter_values_pressure_y.txt
rm parameter_values_pressure_y.txt
rm pressure_gradient.txt
