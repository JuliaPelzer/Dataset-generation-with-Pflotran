## run script by "bash ../<name_of_script> (file should be in parent directory or otherwise name full path to script)" 
## always start from same directory as pflotran.in file

# run variables
OUTPUT_DIR="output"
OUTPUT_PREFIX="${OUTPUT_DIR}/pflotran"
VISU_DIR="visualisation"

# check whether output folder exists else define
if [ ! -d $OUTPUT_DIR ]
then
    mkdir $OUTPUT_DIR
    echo $OUTPUT_DIR folder is created
fi

#command line arguments
args=("$@")
CLA_DEBUG=${args[0]} # expects true or false
CLA_VISUALISATION=${args[1]} # expects true or false

echo ...starting PFLOTRAN simulation at $(date) from $(pwd)

## calculate python stuff
#python3 python_write_datasets/hp_calculations.py

# pflotran simulation
if [ "$CLA_DEBUG" = "debug" ];
then
    #echo does debug
    #mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -pflotran.in -output_prefix $OUTPUT_PREFIX
else
    #echo does no debug
    #mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -pflotran.in -output_prefix $OUTPUT_PREFIX -screen_output off
fi
echo ...finished PFLOTRAN simulation at $(date)

# visualization (video with paraview)
if [ "$CLA_VISUALISATION" = "vis" ];
then
    echo ...starting visualisation at $(date)
    
    # check whether visualisation folder exists else define
    if [ ! -d $VISU_DIR ]
    then
        mkdir $VISU_DIR
        echo $VISU_DIR folder is created
    fi

    # run visualisation script(s)
    pvpython ../scripts_visualisation/test_paraview_automatisierung_screenshotgeneration_no_streamlines.py
    #pvpython ../scripts_visualisation/test_paraview_automatisierung_videogeneration.py
    #pvpython ../scripts_visualisation/test_paraview_automatisierung_screenshotgeneration.py
    echo ...finished paraview visualisation at $(date)
else
    echo ...no visualisation performed and saved
fi