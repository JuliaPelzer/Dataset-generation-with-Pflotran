# Prerequisite (installs)
- pflotran (explanation below)
- python 3.8.10 or newer (tested with this version)
- python packages (installation via pip possible): numpy, noise
- bash 5.0.17 or newer (tested with this version)

## how to install Pflotran using spack:
- git clone -c feature.manyFiles=true https://github.com/spack/spack.git
- . spack/share/spack/setup-env.sh
- copy spack.yaml to folder and go there (e.g. "cd test_nn/installs/")
- spack env activate .
- spack install pflotran (#needs internet access for it)
### next login: 
- . spack/share/spack/setup-env.sh
- go to folder with spack.yaml
- spack env activate .
- spack install pflotran

# Phd_simulation_groundtruth
builds datasets with definable number of data points; based on one pflotran.in file, varying pressure gradients in external .txt file (and varying permeability fields based on perlin_noise in external .h5 files)

## if you use this script on a new computer
- remember to copy all (!) required files (see /dummy_dataset + *.sh bash-script + /scripts)
- if you run the script for a varying permeability field, check that you have all required files in dummy_dataset:
    - pflotran.in
    - settings.yaml
- set the $PFLOTRAN_DIR (in ~/.zshrc or bashrc or similar)

## how to run the script
- decide on whether you want to vary the pressure and permeability field or only the pressure field
    - if you want to vary both, you need to rename the file pflotran_vary_perm.in to pflotran.in and run the bash script make_dataset_vary_perm.sh (MOST LIKELY WHAT YOU WANT)
    - if you want to vary only the pressure field, you need to rename the file pflotran_iso_perm.in to pflotran.in and run the bash script make_dataset_2.sh
- always start from the dataset-directory where your pflotran.in file is located, otherwise it does not find the respective bash file
- run script via "bash ../<name_of_script> (here <name_of_script> is make_dataset_2.sh or make_dataset_vary_perm.sh; this file should be in a parent directory of the datasets you want to simulate - or otherwise give the full path to the script) <CLA_NUMBER_DATAPOINTS> <CLA_NAME> <CLA_CASE> <CLA_VISUALISATION>" with the respective commandline arguments
    - CLA_NUMBER_DATAPOINTS is the number of data points that should be generated in this dataset OR if ..._vary_perm: CLA_NUMBER_VARIATIONS_PRESSURE and CLA_NUMBER_VARIATIONS_PERMEABILITY
    - CLA_NAME is the name of the dataset to create, i.e. of the subfolder to create in the current directory
    - CLA_CASE currently has two options: "1D" creates a dataset with a constant pressure field that only varies in the y-component (MOST LIKELY WHAT YOU WANT); "2D" creates a dataset with a constant pressure field that varies in the x- and y-component
    - CLA_VISULISATION is an **optional** commandline argument defining whether to produce some automated pictures (selfmade in python) : if you want it, write "vis" as CLA_VISUALISATION, else leave it empty

## if you encounter an unexpected error
- you can see that e.g. if a file fort.86 is produced
- comment "-screen_output off" out in the bash-script to get a log output from pflotran

## how to change the size of the domain
- pflotran.in :
    - adapt REGION all if domain should be larger than 200x2000x100m
- change the size and ncells in settings.yaml
- check whether the heat pump is still located reasonably and if you change that position, remember to adapt the visualization and slicing as well
- you probably also want to change the frequency (for the permeability field) in settings.yaml settings.frequency = (4,4,2)

## how to get vtk output to view in paraview
- in pflotran.in change the following line:
    - FORMAT VTK (approx. line 213)