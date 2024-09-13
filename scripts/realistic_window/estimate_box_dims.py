import numpy as np
from typing import Union, Tuple

from scripts.realistic_window.param_sampling import sample_median, random_delta_t, random_thresholded_v_tech
from scripts.realistic_window.lahm.analytical_model_lahm import estimate_plume_shapeparams_lahm
from scripts.realistic_window.tap import estimate_plume_shapeparams_tap

def estimate_box_size(properties:dict[str,np.ndarray], start: Tuple[int,int], sample_size:np.ndarray[int,int] = np.array([100,100]), safety_factor:float = 1.0, method: str = "TAP"):
    # sample_size is in number of cells in orig-data
    v_d = sample_median(properties["darcy_velocity"], start, sample_size) # Darcy vel [m/s]
    b = sample_median(properties["thickness"], start, sample_size) # Aquifer thickness [m]
    v_dd = sample_median(properties["drawdown"], start, sample_size) # max-drawdown # TODO Einheitsumrechnung -> SI-Einheiten
    delta_t = random_delta_t() # delta of injection temperature, groundwater temperature in [K]
    v_tech = random_thresholded_v_tech(v_dd) # [m^3/s]  #TODO schiefe Verteilung?
    # print("sampled props", "vd", v_d, "b", b, "vdd", v_dd, "deltaT", delta_t, "vtech", v_tech)

    if method == "TAP":
        # Formel aus Poster von Fabian
        plume_len, plume_width = estimate_plume_shapeparams_tap(v_tech, delta_t, v_d, b)

    elif method == "LAHM":        
        plume_len, plume_width = estimate_plume_shapeparams_lahm(T_inj_diff=delta_t, q_inj=v_tech, v_a=v_d, m_aquifer=b)
        # print(f"Downstream-length of plume: {plume_len} m")
        # print(f"Width of plume at half length: {plume_width} m")

    box_shape = safety_factor * np.array([plume_len, plume_width])
    return box_shape

def make_window_shape(window_shape: Union[None, np.array], resolution: int, properties_full: np.ndarray, start: Tuple[int,int]) -> np.ndarray[int, int]:
    """
    this function estimates the size of the simulation box in cells if no window_shape is given manually"""
    if window_shape is None:
        window_shape = estimate_box_size(properties_full, start, method="LAHM")
        print("estim. size of simulation box in meters", window_shape)
    else:
        print("manually set window_shape", window_shape, "[m]")
        
    # convert to cells
    window_shape = np.array([window_shape[0]/resolution, window_shape[1]/resolution]) 
    window_shape = window_shape.astype(int)

    for i in range(2):
        if window_shape[i] == 0:
            window_shape[i] = 2
            print(f"WARNING: window_shape too small (zero in one direction) -> set to 2 cells")
   
    print("size of box", window_shape, "[orig. cells]")
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