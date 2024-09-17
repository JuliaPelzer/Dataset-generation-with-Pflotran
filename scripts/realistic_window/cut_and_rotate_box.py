from scipy.interpolate import RegularGridInterpolator
import numpy as np
from typing import List, Dict, Tuple

from scripts.utils import timing

# rotated_box_values = data[rotated_box_coords[::-1]]
# rotated_box_values = rotated_box_values[::-1,::-1]
   
def cut_out_values(data:np.ndarray, rotated_box_cells: Tuple[np.ndarray, np.ndarray]) -> np.ndarray:  
    cells_x = rotated_box_cells[0].flatten()
    cells_y = rotated_box_cells[1].flatten()
    # extract data on meshgrid coordinates "rotated box coords"
    rotated_box_values = data[cells_y.astype(int), cells_x.astype(int)]
    rotated_box_values = rotated_box_values.reshape(rotated_box_cells[0].shape)

    return rotated_box_values

def calc_rotated_box(start:Tuple[int, int], window_shape:Tuple[int, int], rotation_in_degree:float) -> Tuple[np.ndarray, np.ndarray]:
    '''returns rotated (x,y) cell-coordinates as meshgrid(s)'''
    original_orientation_degree = 90
    rotation_in_rad = np.deg2rad(rotation_in_degree + original_orientation_degree)
    # create box as rectangle with coordinates
    x, y = define_cell_mesh(window_shape)
    assert (x.shape[0] == window_shape[0] and x.shape[1] == window_shape[1]), f"x shape {x.shape} should be {window_shape}"

    rot_x = x * np.cos(rotation_in_rad) - y * np.sin(rotation_in_rad)
    rot_y = x * np.sin(rotation_in_rad) + y * np.cos(rotation_in_rad)

    # add start point
    rot_x += start[0]
    rot_y += start[1]

    return rot_x, rot_y 

def define_cell_mesh(window_shape: Tuple[int,int]) -> Tuple[np.ndarray, np.ndarray]:
    x, y = np.meshgrid(np.arange(0, window_shape[1]),
                       np.arange(0, window_shape[0]))
                       
    return x,y
    
def check_validity_window(data:np.ndarray, window:Tuple[np.ndarray,np.ndarray]) -> bool: #Tuple[bool, np.ndarray]:
    """ window is still in cell "coords" of original data """

    # check that window within data range
    if np.any(window[0] < 0) or np.any(window[1] < 0) or np.any(window[0] >= data.shape[1]) or np.any(window[1] >= data.shape[0]):
        print("WARNING: window out of range")
        return False #, None

    # check window for nan values
    box = cut_out_values(data, window)

    if np.any(np.isnan(box)):
        print("WARNING: window contains nan")
        return False #, box
    else:
        return True #, box