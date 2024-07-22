import logging
import os
import shutil
import sys

import numpy as np

try:
    from scripts.create_grid_unstructured import write_loc_well_file
except:
    from create_grid_unstructured import write_loc_well_file


def write_parameter_input_files(p_gradient: float, permeability_iso: float, output_dataset_dir: str, run_id: int, perm_variation: bool = False, vary_pressure_field:bool=False, settings=None, loc_hps: np.ndarray = None, temp: np.ndarray = 15.6, rate: np.ndarray = 0.00024, p_angle:float=0):
    destination_dir = output_dataset_dir / f"RUN_{run_id}"

    # create pressure gradient file
    if not vary_pressure_field:
        p_gradient = np.array([0, p_gradient])
        p_gradient_z = 0
        
        if p_angle != 0:
            rotation_matrix = np.array([[np.cos(p_angle), -np.sin(p_angle)], [np.sin(p_angle), np.cos(p_angle)]])
            p_gradient = np.dot(rotation_matrix, p_gradient)

        pressure_text = f"    LIQUID_PRESSURE {p_gradient[0]} {p_gradient[1]} {p_gradient_z}"
        destination_file = destination_dir / "interim_pressure_gradient.txt"
        with open(destination_file, "w") as file:
            file.write(pressure_text)
        logging.info(
            f"Pressure Input: {p_gradient[0]}, {p_gradient[1]}, {p_gradient_z}"
        )
    else:
        pressure_files_location = output_dataset_dir / "inputs" / "pressure_fields"
        current_pressure_file = return_next_vary_field_file(pressure_files_location, run_id)
        shutil.copy(pressure_files_location / current_pressure_file, destination_dir / "interim_pressure_field.h5")
        # shutil.copy(output_dataset_dir / "inputs" / "pressure_fields" / "empty_pressure_field.h5", destination_dir / "empty_pressure_field.h5")

    # create permeability file (iso or field)
    if not perm_variation:
        permeability_text = f"    PERM_ISO {permeability_iso}"
        destination_file = destination_dir / "interim_iso_permeability.txt"
        with open(destination_file, "w") as file:
            file.write(permeability_text)
        logging.info(f"Permeability Input: {permeability_iso}")
    else:
        perm_files_location = output_dataset_dir / "inputs" / "permeability_fields"
        current_perm_file = return_next_vary_field_file(perm_files_location, run_id)
        shutil.copy(perm_files_location / current_perm_file, destination_dir / "interim_permeability_field.h5")

    if loc_hps is not None:
        try:
            for hp_id, loc_hp in enumerate(loc_hps):
                curr_loc_hp = list(loc_hp)
                curr_loc_hp.append(1)
                write_loc_well_file(destination_dir, settings, loc_hp=curr_loc_hp, idx=hp_id)
        except:
            curr_loc_hp = list(loc_hps)
            curr_loc_hp.append(1)
            write_loc_well_file(destination_dir, settings, loc_hp=curr_loc_hp, idx=hp_id)

    # create injection-temperature file
    temp_text = f"""TIME_UNITS yr
DATA_UNITS C
! <time> <value>
0.  0.
38. 0.
72. {temp[0]}d0""" # TODO for several hps, prettier solution
    destination_file = destination_dir / "interim_injection_temperature.txt"
    with open(destination_file, "w") as file:
        file.write(temp_text)
    logging.info(f"Temperature Input: {temp}")

    # create injection-rate file
    rate_text = f"""0.    0.
38.   0.
72.   {rate[0]}""" # TODO for several hps, prettier solution
    destination_file = destination_dir / "interim_injection_rate.txt"
    with open(destination_file, "w") as file:
        file.write(rate_text)
    logging.info(f"Rate Input: {rate}")


# copy next permeability field to the current folder
def return_next_vary_field_file(folder: str, index: int):
    files = []
    for file in os.listdir(folder):
        files.append(file)
    return files[index]


if __name__ == "__main__":
    cla = sys.argv
    files_location = cla[1]
    index_next_file = int(cla[2])
    destination_folder = cla[3]
    perm_files_location = files_location + "/inputs/permeability_fields"
    current_perm_file = return_next_vary_field_file(perm_files_location, index_next_file)
    current_perm_location = os.path.join(perm_files_location, current_perm_file)
    shutil.copy(current_perm_location, "./interim_permeability_field.h5")
    shutil.copy(
        current_perm_location,
        os.path.join(files_location, destination_folder, current_perm_file),
    )
