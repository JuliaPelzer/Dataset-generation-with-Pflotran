from scipy.interpolate import RegularGridInterpolator
import numpy as np
from typing import List, Dict, Tuple

def cut_box(interpolator:RegularGridInterpolator, rotated_box_coords: Tuple[np.array, np.array]) -> np.array:    
    rotated_box_values = interpolator(rotated_box_coords[::-1])
    rotated_box_values = rotated_box_values[::-1,::-1]
    return rotated_box_values

def calc_rotated_box(start:List[int], window_shape:List[int], resolution_destination:float, rotation_in_degree:float) -> Tuple[np.array, np.array]:
    #TODO check, dass 100% aligned
    original_orientation_degree = 90
    rotation_in_rad = np.deg2rad(rotation_in_degree + original_orientation_degree)
    # create box as rectangle with coordinates
    x, y = np.meshgrid(np.arange(0, window_shape[1]*resolution_destination, resolution_destination), 
                       np.arange(0, window_shape[0]*resolution_destination, resolution_destination))
    assert (x.shape == window_shape).all(), f"x shape {x.shape} should be {window_shape}"

    rot_x = x * np.cos(rotation_in_rad) - y * np.sin(rotation_in_rad)
    rot_y = x * np.sin(rotation_in_rad) + y * np.cos(rotation_in_rad)

    # add start point
    rot_x += start[0]
    rot_y += start[1]

    return rot_x, rot_y # meshgrid x, meshgrid y


def check_validity_window(interpolated_data:np.array, window:np.array) -> bool:
    # check that window within data range
    if np.any(window[0] < 0) or np.any(window[1] < 0) or np.max(window[0].astype(int)) >= interpolated_data.shape[0] or np.max(window[1].astype(int)) >= interpolated_data.shape[1]:
        print("WARNING: window out of range")
        return False

    # check window for nan values
    box = cut_box(interpolated_data, window)

    if np.any(np.isnan(box)):
        print("WARNING: window contains nan")
        return False, box
    else:
        return True, box
    
def cut_bcs_hh(tok:np.array, gwgl:np.array) -> Dict[str, np.array]:
    tok_min = np.nanmin(tok)
    bcs = {}

    bcs["inflow"] = gwgl[0,:] - tok_min
    bcs["outflow"] = gwgl[-1,:] - tok_min
    bcs["top"] = gwgl[:,-1] - tok_min
    bcs["bottom"] = gwgl[:,0] - tok_min

    # sample
    hydraulic_head = gwgl[0,:] - gwgl[-1,:]

    return bcs, hydraulic_head