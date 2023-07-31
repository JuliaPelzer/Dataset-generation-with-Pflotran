import logging
import os
import shutil
import sys

import numpy as np

try:
    from scripts.create_grid_unstructured import write_loc_well_file
    from scripts.make_general_settings import load_yaml
except:
    from create_grid_unstructured import write_loc_well_file
    from make_general_settings import load_yaml


def write_parameter_input_files(
    pressure_grad_y: float,
    perm_iso: float,
    output_dataset_dir: str,
    run_id: int,
    perm_variation: bool = False,
    settings=None,
    loc_hps: np.ndarray = None,
):
    path_to_output = "."

    # create pressure gradient file
    pressure_gradient_x = 0
    pressure_gradient_y = pressure_grad_y
    pressure_gradient_z = 0
    pressure_text = f"    PRESSURE {pressure_gradient_x} {pressure_gradient_y} {pressure_gradient_z}"
    with open("interim_pressure_gradient.txt", "w") as file:
        file.write(pressure_text)
    logging.info(
        f"Pressure Input: {pressure_gradient_x}, {pressure_gradient_y}, {pressure_gradient_z}"
    )
    shutil.copy(
        "interim_pressure_gradient.txt",
        os.path.join(output_dataset_dir, f"RUN_{run_id}", "pressure_gradient.txt"),
    )

    # create permeability file (iso or field)
    if not perm_variation:
        permeability_iso = perm_iso
        permeability_text = f"    PERM_ISO {permeability_iso}"
        with open("interim_iso_permeability.txt", "w") as file:
            file.write(permeability_text)
        logging.info(f"Permeability Input: {permeability_iso}")
        shutil.copy(
            "interim_iso_permeability.txt",
            os.path.join(output_dataset_dir, f"RUN_{run_id}", "permeability_iso.txt"),
        )
    else:
        perm_files_location = output_dataset_dir + "/permeability_fields"
        current_perm_file = return_next_perm_file(perm_files_location, run_id)
        current_perm_location = os.path.join(perm_files_location, current_perm_file)
        shutil.copy(current_perm_location, "./interim_permeability_field.h5")
        shutil.copy(
            current_perm_location,
            os.path.join(output_dataset_dir, f"RUN_{run_id}", current_perm_file),
        )

    if loc_hps is not None:
        assert settings is not None, "Settings must be provided if loc_hps is provided"
        for hp_id, loc_hp in enumerate(loc_hps):
            loc_hp = list(loc_hp)
            loc_hp.append(1)
            logging.info(f"HP {hp_id} Position: {loc_hp}")
            write_loc_well_file(path_to_output, settings, loc_hp=loc_hp, idx=hp_id)
            shutil.copy(
                f"heatpump_inject{hp_id}.vs",
                os.path.join(
                    output_dataset_dir, f"RUN_{run_id}", f"heatpump_inject{hp_id}.vs"
                ),
            )


# copy next permeability field to the current folder
def return_next_perm_file(perm_folder: str, index: int):
    perm_files = []
    for file in os.listdir(perm_folder):
        perm_files.append(file)
    return perm_files[index]


if __name__ == "__main__":
    cla = sys.argv
    files_location = cla[1]
    index_next_file = int(cla[2])
    destination_folder = cla[3]
    perm_files_location = files_location + "/inputs/permeability_fields"
    current_perm_file = return_next_perm_file(perm_files_location, index_next_file)
    current_perm_location = os.path.join(perm_files_location, current_perm_file)
    shutil.copy(current_perm_location, "./interim_permeability_field.h5")
    shutil.copy(
        current_perm_location,
        os.path.join(files_location, destination_folder, current_perm_file),
    )
