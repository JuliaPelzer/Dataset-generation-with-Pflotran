## run script by "bash ../<name_of_script> (file should be in parent directory or otherwise name full path to script)" 
## always start from same directory as pflotran.in file

echo ...starting PFLOTRAN simulation at $(date) from $(pwd)

# run variables
OUTPUT_DIR="output"
OUTPUT_PREFIX="${OUTPUT_DIR}/pflotran"

# check whether output folder exists else define
if [ ! -d $OUTPUT_DIR ]
then
    mkdir $OUTPUT_DIR
    echo $OUTPUT_DIR folder is created
fi

#command line arguments
args=("$@")
CLA_DEBUG=${args[0]} # expects true or false
CLA_VISUALIZATION=${args[1]} # expects true or false

# calculate python stuff
python3 python_write_datasets/hp_calculations.py

# pflotran simulation
if [ "$CLA_DEBUG" = "debug" ];
then
    echo does debug
    mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -pflotran.in -output_prefix $OUTPUT_PREFIX
else
    echo does no debug
    mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -pflotran.in -output_prefix $OUTPUT_PREFIX -screen_output off
fi
echo ...finished PFLOTRAN simulation at $(date)

# visualization (video with paraview)
if [ "$CLA_VISUALIZATION" = "vis" ];
then
    pvpython test_video/test_paraview_automatisierung_videogeneration.py
    pvpython test_video/test_paraview_automatisierung_screenshotgeneration.py
    echo ...finished paraview visualization at $(date)
else
    echo ...no visualization performed and saved
fi