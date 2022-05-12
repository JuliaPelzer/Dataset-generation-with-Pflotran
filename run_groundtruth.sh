## run script by "bash ../<name_of_script> (file should be in parent directory or otherwise name full path to script) <CLA_DEBUG> <CLA_VISUALISATION>"
## always start from same directory as pflotran.in file
## does not expect debug mode + dataset mode ! either debug+single run or dataset and no debugging

#command line arguments
args=("$@")
CLA_SINGLE_RUN=${args[0]} # expects "single_run" or "dataset" - depending on whether single run or dataset should be generated
CLA_DEBUG=${args[1]} # expects "debug" or "no_debug"
CLA_VISUALISATION=${args[2]} # expects "vis" or "no_vis"

echo working at $(date) on folder $(pwd)
# pflotran simulation
if [ "$CLA_SINGLE_RUN" = "single_run" ];
then
    # check whether output folder exists else define
    OUTPUT_SINGLE_RUN_DIR="single_run"
    OUTPUT_SINGLE_RUN_PREFIX="${OUTPUT_SINGLE_RUN_DIR}/pflotran"
    if [ ! -d $OUTPUT_SINGLE_RUN_DIR ]
    then
        mkdir $OUTPUT_SINGLE_RUN_DIR
        echo ...$OUTPUT_SINGLE_RUN_DIR folder is created
    fi

    # one single run
    echo starting PFLOTRAN simulation at $(date)
    PRESSURE_Y=-0.0003

    if [ "$CLA_DEBUG" = "debug" ];
    then # debugging output
        # calculate python stuff
        python3 script_dataset_generation.py INFO ${PRESSURE_Y}
        cp pflotran.in $OUTPUT_SINGLE_RUN_DIR/pflotran-SINGLE_RUN.in
        mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -$OUTPUT_SINGLE_RUN_DIR/pflotran-SINGLE_RUN.in -output_prefix $OUTPUT_SINGLE_RUN_PREFIX

    else # no debugging output
        # calculate python stuff
        python3 script_dataset_generation.py WARN ${PRESSURE_Y}
        cp pflotran.in $OUTPUT_SINGLE_RUN_DIR/pflotran-SINGLE_RUN.in
        mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -$OUTPUT_SINGLE_RUN_DIR/pflotran-SINGLE_RUN.in -output_prefix $OUTPUT_SINGLE_RUN_PREFIX -screen_output off
    
    echo finished PFLOTRAN simulation at $(date)

    # call visualisation
    bash ../scripts_visualisation/call_visualisation.sh $CLA_VISUALISATION $OUTPUT_SINGLE_RUN_DIR
    fi

else 
    # dataset generation
    if [ "$CLA_DEBUG" = "debug" ];
    then
        echo DOES NOT EXPECT DEBUG MODE + DATASET MODE ! either debug+single_run or dataset+no_debug
    
    else
        # check whether output folder exists else define
        OUTPUT_DATASET_DIR="dataset_HDF5"
        if [ ! -d $OUTPUT_DATASET_DIR ]
        then
            mkdir $OUTPUT_DATASET_DIR
            echo ...$OUTPUT_DATASET_DIR folder is created
        fi
        
        # LOOP
        # calc parameters, read them for pressure_y
        DATASET_POINTS=100
        python3 script_calc_parameter_variation.py $DATASET_POINTS
        IFS=$'\r\n' GLOBIGNORE='*' command eval  'PRESSURE_Y=($(cat parameter_values_pressure_y.txt))'
        
        i=0
        len=${#PRESSURE_Y[@]}

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

            cp pflotran.in $OUTPUT_DATASET_RUN_DIR/pflotran-$NAME_OF_RUN.in
            mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -$OUTPUT_DATASET_RUN_DIR/pflotran-$NAME_OF_RUN.in -output_prefix $OUTPUT_DATASET_RUN_PREFIX -screen_output off
            echo finished PFLOTRAN simulation at $(date)

            # call visualisation
            # problem with visualisation, if less than 50 pics TODO
            bash ../scripts_visualisation/call_visualisation.sh $CLA_VISUALISATION $OUTPUT_DATASET_RUN_DIR

            i=$(( $i + 1 ))
        done
    fi
fi