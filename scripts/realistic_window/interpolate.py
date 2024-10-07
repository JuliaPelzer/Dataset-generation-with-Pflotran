import numpy as np
from scipy.interpolate import RegularGridInterpolator
from typing import Dict

def interpolate_properties(property_fields:Dict[str,np.ndarray], orig_resolution: int) -> Dict[str, RegularGridInterpolator]:
    # make property continuous through interpolation
    x,y = np.arange(property_fields["dtw"].shape[0]*orig_resolution, step=orig_resolution), np.arange(property_fields["dtw"].shape[1]*orig_resolution, step=orig_resolution)
    interpolators = {}
    for key in property_fields.keys():
        interpolators[key] = RegularGridInterpolator((x,y), property_fields[key], bounds_error=False, fill_value=None)
    return interpolators


def interpolate_windows(orig_resolution:int, window_properties:Dict[str,np.ndarray], cells:np.ndarray):
    # TODO where? pixel ist orientiert an lower left -> korrektur notwendig: +0.5 resolution in beide richtungen 
    window_desti_cells = cells[:,1:3] # [m] 1:3 if 2D
    interpolators = interpolate_properties(window_properties, orig_resolution)
    window_desti_values = {}
    for key in interpolators.keys():
        window_desti_values[key] = interpolators[key](window_desti_cells)
    return window_desti_values
