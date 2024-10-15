import numpy as np
from pathlib import Path
from typing import Dict

from scripts.create_grid_unstructured import calc_well_location

def write_hps_strata_conditions_files(dataset_folder_interim: str, number_of_hps: int):
    with open(f"{dataset_folder_interim}/strata_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"STRATA\n  REGION heatpump_inject{hp}\n  MATERIAL gravel_inj\nEND\n\n")
    with open(f"{dataset_folder_interim}/conditions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"SOURCE_SINK heatpump_inject{hp}\n  FLOW_CONDITION injection{hp}\n  REGION heatpump_inject{hp}\nEND\n\n")
    
def calc_locs_hp(vary_poss: bool, param_dataset_size: int, number_of_hps: int, settings: Dict):
    hps_cell_ids = np.zeros((number_of_hps, param_dataset_size))
    # get boundaries of domain
    grid_size = settings["grid"]["size [m]"]
    
    if vary_poss:
        try:
            distance_to_border = settings["grid"]["distance_to_border"]
            print(f"distance to border: {distance_to_border} m, {len(distance_to_border[1])} values")
        except:
            distance_to_border = [[5], [5,5], 5]

    for i in range(number_of_hps):
        # choose random position inside domain
        if vary_poss:
            try:
                locs_x = np.random.randint(0 + distance_to_border[0][0],grid_size[0] - distance_to_border[0][1],param_dataset_size,)
            except:
                try:
                    locs_x = np.random.randint(0 + distance_to_border[0][0],grid_size[0] - distance_to_border[0][0],param_dataset_size,)
                except:
                    locs_x = np.random.randint(0 + distance_to_border,grid_size[0] - distance_to_border,param_dataset_size,)

            assert len(distance_to_border[1]) == 1 or len(distance_to_border[1]) == 2, "distance to border in y direction must be either one value or two values"
            if len(distance_to_border[1]) == 1:
                locs_y = np.random.randint(0 + distance_to_border[1],grid_size[1] - distance_to_border[1],param_dataset_size,)
            elif len(distance_to_border[1]) == 2:
                locs_y = np.random.randint(distance_to_border[1][0],grid_size[1] - distance_to_border[1][1],param_dataset_size,)

            locs_hps = np.array([locs_x, locs_y,np.ones_like(locs_x)]).T
            # save to file
            # with open(dataset_folder_inputs / f"locs_hp_x_{i+1}.txt", "w") as f:
            #     np.savetxt(f, locs_x)
            # with open(dataset_folder_inputs / f"locs_hp_y_{i+1}.txt", "w") as f:
            #     np.savetxt(f, locs_y)

        else:
            try:
                locs_hps = [settings["grid"]["loc_hp [m]"]]

            except:
                # if nothing specified: center position
                locs_hps = [list((np.array(settings["grid"]["size [m]"])/2).astype(int))]

        list_hps_ids = []
        for loc_hp in locs_hps:
            list_hps_ids.append(calc_well_location(settings, loc_hp))
        hps_cell_ids[i] = list_hps_ids
    return np.swapaxes(hps_cell_ids, 0, 1).astype(int)
