# Phd_simulation_groundtruth
builds datasets with definable number of data points, one pflotran.in file, varying pressure gradients in external txt file

## if you use this script on a new computer
- remember to copy all (!) required files (see dummy_dataset)
- set the $PFLOTRAN_DIR (in ~/.zshrc or bashrc or similar)

## how to run the script
- run script via "bash ../<name_of_script> (here <name_of_script> is make_dataset.sh; file should be in parent directory or otherwise name full path to script) <CLA_DEBUG> <CLA_NUMBER_DATAPOINTS> <CLA_NAME> <CLA_VISUALISATION>"
- always start from the directory where your pflotran.in file is, otherwise it does not find make_dataset.sh
