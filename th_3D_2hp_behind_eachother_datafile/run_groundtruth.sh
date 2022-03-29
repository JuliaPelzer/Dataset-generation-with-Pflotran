## run script by "bash name/of/script" , always start from same directory as pflotran.in file

echo ...starting PFLOTRAN simulation at $(date)

# run variables
OUTPUT_DIR="output"

# check whether output folder exists else define
if [ ! -d $OUTPUT_DIR ]
then
    echo Does not exist
    mkdir $OUTPUT_DIR
fi

# calculate python stuff
python3 python_write_datasets/hp_calculations.py

# start pflotran simulation
mpirun -n 1 $PFLOTRAN_DIR/src/pflotran/pflotran -pflotran.in -output_prefix $OUTPUT_DIR #-screen_output off

echo ... finished PFLOTRAN simulation at $(date)