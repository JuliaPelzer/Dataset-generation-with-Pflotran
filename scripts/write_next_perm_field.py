# copy next permeability field to the current folder

import sys
import os
import shutil

def return_next_perm_file(perm_folder:str, index:int):
    perm_files = []
    for file in os.listdir(perm_folder):
        perm_files.append(file)
    return perm_files[index]

if __name__ == "__main__":
    cla = sys.argv
    files_location = cla[1]
    index_next_file = int(cla[2])
    destination_folder = cla[3]
    perm_files_location = files_location+"/inputs/permeability_fields"
    current_perm_file = return_next_perm_file(perm_files_location, index_next_file)
    current_perm_location = os.path.join(perm_files_location, current_perm_file)
    shutil.copy(current_perm_location, "./interim_permeability_field.h5")
    shutil.copy(current_perm_location, os.path.join(files_location, destination_folder, current_perm_file))