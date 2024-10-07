import numpy as np
import pathlib
from typing import Dict
import h5py

from scripts.realistic_window.param_sampling import sample_median, random_delta_t, random_thresholded_v_tech

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

def realistic_pump_params(data_dir: pathlib.Path, hps_cell_ids: np.ndarray, temp_default:float=None, rate_default:float=None):
    temps = np.zeros_like(hps_cell_ids, dtype=float)
    rates = np.zeros_like(hps_cell_ids, dtype=float)
    for hp_id, hp_cell_id in enumerate(hps_cell_ids):
        if temp_default == None:
            delta_T = random_delta_t() # delta of injection temperature to groundwater temperature
            injection_T = 10.6 + delta_T
            temps[hp_id] = injection_T
        else:
            temps[hp_id] = temp_default

        if rate_default == None:
            with h5py.File(data_dir / "drawdown.h5", "r") as v_dd:
                line_id = np.where(v_dd["Cell Ids"] == hp_cell_id)
                max_dd = v_dd["drawdown"][line_id]
                v_tech = random_thresholded_v_tech(max_dd) # [m^3/s]
                rates[hp_id] = np.round(v_tech, 8)
        else:
            rates[hp_id] = rate_default

    return temps, rates

def write_pump_param_files(destination_dir: str, loc_hps: np.ndarray = None, temp: np.ndarray = 15.6, rate: np.ndarray = 0.00024):

    # REGION_HPS.TXT
    with open(destination_dir / "regions_hps.txt", "w") as f:
        
        for hp_id, cell_id_hp in enumerate(loc_hps):
            loc_text = f"""REGION heatpump_inject{hp_id}\nLIST\n    {cell_id_hp}\n/\n/\n\n"""
            f.write(loc_text)

    # # INJECTION_X_TEMPERATURE.TXT
    # temp_schedule = f"""TIME_UNITS yr\nDATA_UNITS C\n! <time> <value>\n0.  0.\n38. 0.\n72. {temp[0]}d0"""
    # with open(destination_dir / f"injection_{hp_id}_temperature.txt", "w") as file:
    #     file.write(temp_schedule)

    # # INJECTION_X_RATE.TXT
    # rate_schedule = f"""0.    0.\n38.   0.\n72.   {rate[0]}"""
    # with open(destination_dir / f"injection_{hp_id}_rate.txt", "w") as file:
    #     file.write(rate_schedule)


    with open(f"{destination_dir}/conditions_flow_inj.txt", "w") as f:
        for hp_id, cell_id_hp in enumerate(loc_hps):
            rate_schedule = f"""0.  {rate[hp_id]}"""
            temp_schedule = f"""0.  {temp[hp_id]}"""

            f.write(f"""FLOW_CONDITION injection{hp_id}\n  TYPE\n    RATE SCALED_VOLUMETRIC_RATE VOLUME\n    TEMPERATURE DIRICHLET\n  /\n  CYCLIC\n  RATE LIST\n    TIME_UNITS d\n    DATA_UNITS m^3/s\n    {rate_schedule}\n  /\n   TEMPERATURE LIST\n    TIME_UNITS yr\n    DATA_UNITS C\n    ! <time> <value>\n    {temp_schedule}\n  /\n/\n\n""")
            




#   FLOW_CONDITION injection !influx starting at day 72
#     TYPE
#       RATE SCALED_VOLUMETRIC_RATE VOLUME
#       TEMPERATURE DIRICHLET
#     /
#     RATE LIST
#       TIME_UNITS d
#       DATA_UNITS m^3/s
#       EXTERNAL_FILE injection_rate.txt
#     /
#     TEMPERATURE FILE injection_temperature.txt
#   /
