import numpy as np
import h5py
import pathlib
from typing import Dict, Tuple
import logging

from scripts.mesh_refinement_utils import *

logging.basicConfig(level=logging.WARNING)

def refine_regions_acc_to_hps(num_dp:int, settings:Dict, grids:np.array, dps_hps_locs:np.array):
    refined_cell_centers = []
    refined_cell_volumes = []
    # for each dp:
    for id in range(num_dp):

        # get cell centers in region
        resolutions = np.array([settings["grid"]["resolution"],]*np.prod(calc_n_cells_array(settings)))
        print(resolutions.shape, grids[id].shape)
        grid_and_resolutions = np.concatenate([grids[id], resolutions.reshape(-1, 1)], axis=1)
        plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, dps_hps_locs[id], factor=0.1)
        bounds = [[0, settings["grid"]["size [m]"][0]], [0, settings["grid"]["size [m]"][1]]]

        # for each hp:
        for hp in dps_hps_locs[id]:
            # refine region around hp
            grid_and_resolutions = refine_region(grid_and_resolutions, hp, settings, bounds)

        plot_grid(grid_and_resolutions[:,:-1], grid_and_resolutions[:,-1]**3, settings, dps_hps_locs[id], factor=0.1)

        refined_cell_centers.append(grid_and_resolutions[:,:-1])
        ## cell volumes
        refined_cell_volumes.append(grid_and_resolutions[:,-1]**3)
        # TODO store information
        
    return refined_cell_centers, refined_cell_volumes


def refine_mesh(path_to_output: pathlib.Path, settings: Dict, positions_hps: np.ndarray):
    ...
    # get mesh

    # refine mesh + store information:
    ## cell centers + cell volumes
    refined_cell_centers, refined_cell_volumes = refine_cell_centers_and_volumes_acc_to_hps(cell_centers, hps, settings)

    ## face areas
    ## face cell ids
    ## face centers
    ## correct face ids


    # TODO refine boundaries?