import numpy as np
from scipy.interpolate import RegularGridInterpolator
from typing import Dict

def interpolate_properties(property_fields:Dict[str,np.array], orig_resolution: int) -> Dict[str, RegularGridInterpolator]:
    # make property continuous through interpolation
    x,y = np.arange(property_fields["dtw"].shape[0]*orig_resolution, step=orig_resolution), np.arange(property_fields["dtw"].shape[1]*orig_resolution, step=orig_resolution)
    interpolators = {}
    for key in property_fields.keys():
        interpolators[key] = RegularGridInterpolator((x,y), property_fields[key], bounds_error=False, fill_value=None)
    return interpolators


def interpolate_windows(orig_resolution:int, window_properties:Dict[str,np.ndarray], cells:np.ndarray):
    # TODO where? pixel ist orientiert an lower left -> korrektur notwendig: +0.5 resolution in beide richtungen 
    window_desti_cells = cells[:,1:3] # [m] 1:3 if 2D
    # window_orig_cells = tuple(np.meshgrid(np.arange(window_shape[0]*orig_resolution, step=orig_resolution),
    #                                  np.arange(window_shape[1]*orig_resolution, step=orig_resolution)))
    interpolators = interpolate_properties(window_properties, orig_resolution)
    window_desti_values = {}
    # orig_values = {}
    for key in interpolators.keys():
        window_desti_values[key] = interpolators[key](window_desti_cells)

        # import matplotlib.pyplot as plt
        # plt.figure()
        # plt.subplot(1, 3,1)
        # plt.title(key)
        # plt.scatter(cells[:,1], cells[:,2], c=window_desti_values[key])

        # plt.subplot(1, 3,2)
        # print(window_desti_cells.shape, window_orig_cells[0].shape)
        # orig_values[key] = interpolators[key](window_orig_cells)
        # plt.title(key)
        # plt.imshow(orig_values[key], origin="lower")
        # plt.show()
        # exit()

    return window_desti_values
