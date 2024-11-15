import numpy as np

def calc_injection_variation(number_datapoints: int, dataset_folder: str, num_hp_per_dp:int,):
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