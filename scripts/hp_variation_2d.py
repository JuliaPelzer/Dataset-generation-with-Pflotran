import numpy as np
from typing import Dict
import logging

from scripts.mesh_generation_utils import loc_to_id_closest

def write_hps_strata_conditions_files(dataset_folder_interim: str, number_of_hps: int):
    with open(f"{dataset_folder_interim}/strata_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"STRATA\n  REGION heatpump_inject{hp}\n  MATERIAL gravel_inj\nEND\n\n")
    with open(f"{dataset_folder_interim}/conditions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"SOURCE_SINK heatpump_inject{hp}\n  FLOW_CONDITION injection{hp}\n  REGION heatpump_inject{hp}\nEND\n\n")
    
def hps_locs_to_ids(hps_locs: np.ndarray, meshs_refined: np.ndarray):
    """
    Convert locations of heat pumps to cell ids
    
    Args:
        hps_locs: np.ndarray, shape (num_dps, num_hps, 3), locations of heat pumps in meters
    """
    hps_cell_ids = np.zeros((hps_locs.shape[0], hps_locs.shape[1]))
    for run_id, dp in enumerate(hps_locs):
        for hp_id, hp_loc in enumerate(dp):
            centers_and_ress = np.column_stack([meshs_refined[run_id]["cell_centers"], np.cbrt(meshs_refined[run_id]["cell_volumes"])])
            hp_cell_id = loc_to_id_closest(centers_and_ress, hp_loc)
            hps_cell_ids[run_id, hp_id] = hp_cell_id
            
    hps_cell_ids = hps_cell_ids.astype(int)
    for i in range(hps_cell_ids.shape[0]):
        assert len(np.unique(hps_cell_ids[i])) == hps_locs.shape[1], f"Double entries in line {i}: {hps_cell_ids[i]}"
    return hps_cell_ids


def calc_hps_locs_float(vary_poss: bool, num_dps: int, num_hps: int, settings: Dict):
    """
    Outputs:
        hps_locs: np.ndarray, shape (num_dps, num_hps, 3), locations of heat pumps in meters
    """
    
    # get boundaries of domain
    grid_size = settings["grid"]["size [m]"]
    res = settings["grid"]["resolution"]

    # expand 3rd dimension if not given
    if len(grid_size) == 2:
        grid_size.append(settings["grid"]["resolution"])
    
    # choose random position inside domain
    if vary_poss:

        # unify format of distance to border        
        if isinstance(settings["grid"]["distance_to_border"], int):
            distance_to_border = [settings["grid"]["distance_to_border"], settings["grid"]["distance_to_border"], settings["grid"]["distance_to_border"]]
        else:
            if settings["grid"]["distance_to_border"] is not None:
                distance_to_border = settings["grid"]["distance_to_border"]
                logging.info(f"distance to border: {distance_to_border} m values")
            else:
                distance_to_border = [res, res, res/2-1]
        assert len(distance_to_border) in [2,3], "distance_to_border must have 2 or 3 values"

        try:
            dists_x = [distance_to_border[0][0], distance_to_border[0][1]]
        except:
            dists_x = [distance_to_border[0], distance_to_border[0]]
        try:
            dists_y = [distance_to_border[1][0], distance_to_border[1][1]]
        except:
            dists_y = [distance_to_border[1], distance_to_border[1]]
        dists_z = [distance_to_border[2], ]*2

        # ensure that distance to both dit-to-borders together are smaller than domain size in that dimension
        for dist, size in zip([dists_x, dists_y, dists_z], grid_size):
            dist_sum = np.sum(dist)
            if dist_sum >= size:
                logging.warning(f"distance to border ({dist_sum}) must be smaller than domain size ({size})")
                for id, _ in enumerate(dist):
                    dist[id] = size/2 - 1

        locs_x = np.random.uniform(0 + dists_x[0],grid_size[0] - dists_x[1],num_dps*num_hps,)
        locs_y = np.random.uniform(0 + dists_y[0],grid_size[1] - dists_y[1],num_dps*num_hps,)
        locs_z = np.random.uniform(0 + dists_z[0], grid_size[2] - dists_z[1], num_dps*num_hps,)

        hps_locs = np.array([locs_x, locs_y, locs_z]).T # np.ones_like(locs_x)]).T
    else:
        try:
            hps_locs = [settings["grid"]["loc_hp [m]"]]

        except:
            # if nothing specified: center position
            hps_locs = [list((np.array(grid_size)/2))]

    hps_locs = hps_locs.reshape((num_hps, num_dps, 3))
    hps_locs = np.swapaxes(hps_locs, 0, 1)
    return hps_locs