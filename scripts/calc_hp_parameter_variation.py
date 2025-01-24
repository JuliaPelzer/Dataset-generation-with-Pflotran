import numpy as np
from typing import Tuple

from scripts.main_helpers import *
from scripts.realistic_window.param_sampling import random_delta_t, random_thresholded_v_tech, sample_median


def calc_pump_params(number_datapoints: int, dataset_folder: str, num_hp_per_dp:int,):
    temp_array, rate_array = None, None

    # sample temperature uniformly from the values [0.6-7.6;13.6-20.6]
    temp_array = np.random.uniform(13.6, 20.6, number_datapoints * num_hp_per_dp)
    temp_array = np.append(temp_array, np.random.uniform(0.6, 7.6, number_datapoints * num_hp_per_dp))
    temp_array = np.random.choice(temp_array, number_datapoints * num_hp_per_dp, replace=False) # should work that way since both arrays cover the same distance and are equally distributed
    # reshape to(number_datapoints, num_hp_per_dp)
    temp_array = temp_array.reshape(number_datapoints, num_hp_per_dp)

    # sample rate uniformly from the values [0.0001-0.001]
    rate_array = np.random.uniform(0.0001, 0.001, number_datapoints * num_hp_per_dp)
    # reshape to(number_datapoints, num_hp_per_dp)
    rate_array = rate_array.reshape(number_datapoints, num_hp_per_dp)

    with open(dataset_folder / "injection_temperatures.txt", "w") as injection_temperature_file:
        np.savetxt(injection_temperature_file, temp_array)
    with open(dataset_folder / "injection_rates.txt", "w") as injection_rate_file:
        np.savetxt(injection_rate_file, rate_array)

    return temp_array, rate_array

def make_pump_params(v_dd:np.ndarray, temp_default:float = None, rate_default:float = None):
    if temp_default == None:
        delta_t = random_delta_t() # delta of injection temperature, groundwater temperature in [K]
    else:
        delta_t = temp_default - groundwater_temp()
    if rate_default == None:
        v_tech = random_thresholded_v_tech(v_dd) # [m^3/s]  #TODO schiefe Verteilung?
    else:
        v_tech = rate_default

    return {"temp": delta_t + groundwater_temp(), "rate": v_tech}

def realistic_pump_params(windows_properties: list[dict], hps_locs: np.ndarray, orig_resolution: int, temp_default:float=None, rate_default:float=None) -> Tuple[np.ndarray, np.ndarray]:
    """returns temperatures and rates for all heat pumps in all datapoints"""
    temps = np.zeros((hps_locs.shape[0], hps_locs.shape[1]), dtype=float)
    rates = np.zeros((hps_locs.shape[0], hps_locs.shape[1]), dtype=float)
    for dp_id, dp in enumerate(hps_locs):
        for hp_id, hp_loc in enumerate(dp):
            if temp_default == None:
                delta_T = random_delta_t() # delta of injection temperature to groundwater temperature, TODO match to automatic window shape generation
                injection_T = groundwater_temp() + delta_T
                temps[dp_id, hp_id] = injection_T
            else:
                temps[dp_id, hp_id] = temp_default

            if rate_default == None:
                v_dd = windows_properties[dp_id]["properties"]["drawdown"]
                hp_loc = (hp_loc / orig_resolution).astype(int)
                max_dd = sample_median(v_dd, [hp_loc[1], hp_loc[0]], [3,3]) # does not work if directly at border # 
                v_tech = random_thresholded_v_tech(max_dd) # [m^3/s]
                rates[dp_id, hp_id] = np.round(v_tech, 8)
            else:
                rates[dp_id, hp_id] = rate_default

    return temps, rates


def write_pump_param_files(destination_dir: str, loc_hps: np.ndarray, temps: np.ndarray, rates: np.ndarray):

    np.savetxt(destination_dir / "injection_temps.txt", np.array([loc_hps, temps]).T)
    np.savetxt(destination_dir / "injection_rates.txt", np.array([loc_hps, rates]).T)

    with open(destination_dir / "regions_hps.txt", "w") as f:
        for hp_id, cell_id_hp in enumerate(loc_hps):
            loc_text = f"""REGION heatpump_inject{hp_id}\n  LIST\n    {cell_id_hp}\n  /\n/\n\n"""
            f.write(loc_text)

    with open(f"{destination_dir}/conditions_flow_inj.txt", "w") as f:
        for hp_id, cell_id_hp in enumerate(loc_hps):
            rate_schedule = f"""0.  {rates[hp_id]}"""
            temp_schedule = f"""0.  {temps[hp_id]}"""

            f.write(f"""FLOW_CONDITION injection{hp_id}\n  TYPE\n    RATE SCALED_VOLUMETRIC_RATE VOLUME\n    TEMPERATURE DIRICHLET\n  /\n  CYCLIC\n  RATE LIST\n    TIME_UNITS d\n    DATA_UNITS m^3/s\n    {rate_schedule}\n  /\n   TEMPERATURE LIST\n    TIME_UNITS yr\n    DATA_UNITS C\n    ! <time> <value>\n    {temp_schedule}\n  /\n/\n\n""")