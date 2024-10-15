import numpy as np
from typing import Union, Tuple, Dict

from scripts.main_helpers import *
from scripts.realistic_window.param_sampling import sample_median, random_delta_t, random_thresholded_v_tech
from scripts.realistic_window.lahm.analytical_model_lahm import estimate_plume_shapeparams_lahm
from scripts.realistic_window.tap import estimate_plume_shapeparams_tap

def estimate_box_size(properties:dict[str,np.ndarray], center: Tuple[int,int], sample_size:np.ndarray[int,int] = np.array([100,100]), safety_factor:float = 1.5, method: str = "TAP", temp_default:float = None, rate_default:float = None):
    # sample_size is in number of cells in orig-data
    v_d = sample_median(properties["darcy_velocity"], center, sample_size) # Darcy vel [m/s]
    b = sample_median(properties["thickness"], center, sample_size) # Aquifer thickness [m]
    v_dd = sample_median(properties["drawdown"], center, sample_size) # max-drawdown # TODO Einheitsumrechnung -> SI-Einheiten
    if temp_default == None:
        delta_t = random_delta_t() # delta of injection temperature, groundwater temperature in [K]
    else:
        delta_t = temp_default - groundwater_temp()
    if rate_default == None:
        v_tech = random_thresholded_v_tech(v_dd) # [m^3/s]  #TODO schiefe Verteilung?
    else:
        v_tech = rate_default

    if method == "TAP":
        # Formel aus Poster von Fabian
        plume_len, plume_width = estimate_plume_shapeparams_tap(v_tech, delta_t, v_d, b)

    elif method == "LAHM":        
        plume_len, plume_width = estimate_plume_shapeparams_lahm(T_inj_diff=delta_t, q_inj=v_tech, v_a=v_d, m_aquifer=b)
        # print(f"Downstream-length of plume: {plume_len} m")
        # print(f"Width of plume at half length: {plume_width} m")

    box_shape = safety_factor * np.array([plume_len, plume_width])
    return box_shape

def make_window_shape(settings: Dict, resolution: int, properties_full: np.ndarray, start: Tuple[int,int], temp_default: float, rate_default: float) -> np.ndarray[int, int]:
    """
    this function estimates the size of the simulation box in cells if no window_shape is given manually"""
    window_shape_in_meters = settings["grid"]["size [m]"]

    if window_shape_in_meters is None:
        window_shape_in_meters = estimate_box_size(properties_full, start, method="LAHM", temp_default=temp_default, rate_default=rate_default)
        print(f"estimated window size: {window_shape_in_meters} [m]")
    else:
        print(f"manually set window size: {window_shape_in_meters} [m]")
        
    # convert to cells
    window_shape = np.array([window_shape_in_meters[0]/resolution, window_shape_in_meters[1]/resolution]) 
    window_shape = window_shape.astype(int)

    for i in range(2):
        if window_shape[i] == 0:
            window_shape[i] = 2
            print(f"WARNING: window_shape too small (zero in one direction) -> set to 2 cells")
   
    return window_shape

def estimate_box_rotation(direction_field: np.ndarray, start: Tuple[int,int], window_shape: np.ndarray[int, int]) -> float:
    # estimate rotation of box in degrees;
    # 0 = flow FROM north TO south; clockwise rotation
    rotation = sample_median(direction_field, start, window_shape)
    return rotation

# def calc_box_height(box_thickness_20):
#     window_height_in_meters = np.max(box_thickness_20)
#     return window_height_in_meters

def calc_box_height_from_TOK_n_GWGL(tok, gwgl):
    window_height_in_meters = -np.nanmin(tok) + np.nanmax(gwgl)
    return window_height_in_meters

def reference_box_size(safety_factor:float = 1.0):
    # Formel aus Poster von Fabian
    v_d = 0.0015*0.005 # Darcy vel [m/s](=8.7e-5)
    b = 5  # Aquifer thickness [m]
    delta_t = 5  # delta of injection temperature, groundwater temperature in [K]
    v_tech = 52 / 86400 # [m^3/s]  (=0.0006)
    print("SOLL: len = 1km, width = 55m")

    plume_len, plume_width = estimate_plume_shapeparams_tap(v_tech, delta_t, v_d, b)
    print("TAP: len=", plume_len, "width=", plume_width)
    plume_len, plume_width = estimate_plume_shapeparams_lahm(T_inj_diff=delta_t, q_inj=v_tech, v_a=v_d, m_aquifer=b)
    print("LAHM: len=", plume_len, "width=", plume_width)
    
    box_shape = safety_factor * np.array([plume_len, plume_width])

    return box_shape