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
    
def calc_hp_locs(vary_poss: bool, num_dps: int, num_hps: int, settings: Dict):
    """
    Outputs:
        hps_locs: np.ndarray, shape (num_dps, num_hps, 3), locations of heat pumps in meters
    """
    
    # get boundaries of domain
    grid_size = settings["grid"]["size [m]"]
    
    if vary_poss:
        try:
            distance_to_border = settings["grid"]["distance_to_border"]
            print(f"distance to border: {distance_to_border} m, {len(distance_to_border[1])} values")
        except:
            distance_to_border = [[5], [5,5], 5]
        assert len(distance_to_border[1]) == 1 or len(distance_to_border[1]) == 2, "distance to border in y direction must be either one value or two values"

    # choose random position inside domain
    # TODO better variation, TODO float instead of int for position TODO 3D
    if vary_poss:
        try:
            locs_x = np.random.randint(0 + distance_to_border[0][0],grid_size[0] - distance_to_border[0][1],num_dps*num_hps,)
        except:
            try:
                locs_x = np.random.randint(0 + distance_to_border[0][0],grid_size[0] - distance_to_border[0][0],num_dps*num_hps,)
            except:
                locs_x = np.random.randint(0 + distance_to_border,grid_size[0] - distance_to_border,num_dps*num_hps,)

        if len(distance_to_border[1]) == 1:
            locs_y = np.random.randint(0 + distance_to_border[1],grid_size[1] - distance_to_border[1],num_dps*num_hps,)
        elif len(distance_to_border[1]) == 2:
            locs_y = np.random.randint(distance_to_border[1][0],grid_size[1] - distance_to_border[1][1],num_dps*num_hps,)

        hps_locs = np.array([locs_x, locs_y,np.ones_like(locs_x)]).T

    else:
        try:
            hps_locs = [settings["grid"]["loc_hp [m]"]]

        except:
            # if nothing specified: center position
            hps_locs = [list((np.array(settings["grid"]["size [m]"])/2).astype(int))]
    hps_locs = hps_locs.reshape((num_hps, num_dps, 3))
    hps_locs = np.swapaxes(hps_locs, 0, 1)
    return hps_locs

def hps_locs_to_ids(hps_locs: np.ndarray, grids_cells_centers: np.ndarray):
    """
    Convert locations of heat pumps to cell ids
    
    Args:
        hps_locs: np.ndarray, shape (num_dps, num_hps, 3), locations of heat pumps in meters
    """
    hps_cell_ids = np.zeros((hps_locs.shape[0], hps_locs.shape[1]))
    for run_id, dp in enumerate(hps_locs):
        for hp_id, hp_loc in enumerate(dp):
            hp_cell_id = loc_to_id(grids_cells_centers[run_id], hp_loc)
            hps_cell_ids[run_id, hp_id] = hp_cell_id
            
    hps_cell_ids = hps_cell_ids.astype(int)
    for i in range(hps_cell_ids.shape[0]):
        assert len(np.unique(hps_cell_ids[i])) == hps_locs.shape[1], f"Double entries in line {i}: {hps_cell_ids[i]}"
    return hps_cell_ids


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