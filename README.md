# Phd_simulation_groundtruth
builds datasets with definable number of data points; based on one pflotran.in file, varying pressure gradients in external .txt file

## if you use this script on a new computer
- remember to copy all (!) required files (see dummy_dataset + .sh bash-script + /scripts)
- set the $PFLOTRAN_DIR (in ~/.zshrc or bashrc or similar)

## how to run the script
- always start from the dataset-directory where your pflotran.in file is located, otherwise it does not find make_dataset_2.sh
- run script via "bash ../<name_of_script> (here <name_of_script> is make_dataset_2.sh; this file should be in a parent directory of the datasets you want to simulate - or otherwise give the full path to the script) <CLA_NUMBER_DATAPOINTS> <CLA_NAME> <CLA_CASE> <CLA_VISUALISATION>" with the respective commandline arguments
    - CLA_NUMBER_DATAPOINTS is the number of data points that should be generated in this dataset
    - CLA_NAME is the name of the dataset to create
    - CLA_CASE currently has two options: "1D" creates a dataset with a constant pressure field that only varies in the y-component; "2D" creates a dataset with a constant pressure field that varies in the x- and y-component
    - CLA_VISULISATION is an optional commandline argument defining whether to produce some automated pictures (builds on paraview and does not look very pretty...)
