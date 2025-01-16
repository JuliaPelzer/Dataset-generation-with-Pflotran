import numpy as np
from typing import Dict
import logging

from scripts.mesh_generation_utils import loc_to_id

def write_hps_strata_conditions_files(dataset_folder_interim: str, number_of_hps: int):
    with open(f"{dataset_folder_interim}/strata_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"STRATA\n  REGION heatpump_inject{hp}\n  MATERIAL gravel_inj\nEND\n\n")
    with open(f"{dataset_folder_interim}/conditions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"SOURCE_SINK heatpump_inject{hp}\n  FLOW_CONDITION injection{hp}\n  REGION heatpump_inject{hp}\nEND\n\n")
    
def calc_hp_cell_ids(vary_poss: bool, param_dataset_size: int, number_of_hps: int, grids_cells_centers: np.array, settings: Dict):
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
        # TODO better variation, TODO float instead of int for position
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
        for sim_run_id, loc_hp in enumerate(locs_hps):
            list_hps_ids.append(loc_to_id(grids_cells_centers[sim_run_id], loc_hp))
        hps_cell_ids[i] = list_hps_ids
    result = np.swapaxes(hps_cell_ids, 0, 1).astype(int)

    for i in range(result.shape[0]):
        print(result[i])
        assert len(np.unique(result[i])) == number_of_hps, f"Double entries in line {i}: {result[i]}"
    return result


def calc_locs_hp_float(vary_poss: bool, param_dataset_size: int, number_of_hps: int, settings: Dict):
    hps_locs_all = np.zeros((number_of_hps, param_dataset_size, 3))  # x, y, z
    # get boundaries of domain
    grid_size = settings["grid"]["size [m]"]
    
    if vary_poss:
        try:
            distance_to_border = settings["grid"]["distance_to_border"]
            logging.info(f"distance to border: {distance_to_border} m, {len(distance_to_border[1])} values")
        except:
            distance_to_border = [[5], [5,5], 5]

    for i in range(number_of_hps):
        # choose random position inside domain
        # TODO better variation
        # TODO 3D
        if vary_poss:
            try:
                locs_x = np.random.uniform(0 + distance_to_border[0][0],grid_size[0] - distance_to_border[0][1],param_dataset_size)
            except:
                try:
                    locs_x = np.random.uniform(0 + distance_to_border[0][0],grid_size[0] - distance_to_border[0][0],param_dataset_size)
                except:
                    locs_x = np.random.uniform(0 + distance_to_border,grid_size[0] - distance_to_border,param_dataset_size,)

            assert len(distance_to_border[1]) == 1 or len(distance_to_border[1]) == 2, "distance to border in y direction must be either one value or two values"
            if len(distance_to_border[1]) == 1:
                locs_y = np.random.uniform(0 + distance_to_border[1],grid_size[1] - distance_to_border[1],param_dataset_size)
            elif len(distance_to_border[1]) == 2:
                locs_y = np.random.uniform(distance_to_border[1][0],grid_size[1] - distance_to_border[1][1],param_dataset_size)

            locs_hps = np.array([locs_x, locs_y,np.ones_like(locs_x)]).T

        else:
            try:
                locs_hps = [settings["grid"]["loc_hp [m]"]]

            except:
                # if nothing specified: center position
                locs_hps = [list((np.array(settings["grid"]["size [m]"])/2))]

        hps_locs_all[i] = locs_hps
    hps_locs_all = np.swapaxes(hps_locs_all, 0, 1)
    return hps_locs_all