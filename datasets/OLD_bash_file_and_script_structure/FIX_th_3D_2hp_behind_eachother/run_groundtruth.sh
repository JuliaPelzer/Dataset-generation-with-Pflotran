## run script by "bash name/of/script" , always start from same directory as pflotran.in file

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

# calculate python stuff
python3 python_write_datasets/hp_calculations.py

# start pflotran simulation
mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -pflotran.in -output_prefix $OUTPUT_PREFIX #-screen_output off

echo ...finished PFLOTRAN simulation at $(date)