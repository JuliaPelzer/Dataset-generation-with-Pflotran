import numpy as np
import sys
from typing import Union

def benchmark_pressure_perm():
    # benchmark: 3 testcases (see diss.tex)
    pressure_array = np.array([-0.0015, -0.0015, -0.003, -0.0035])
    permeability_iso_array = np.array([1.0193679918450561e-11, 2.038735983690112e-10, 1.0193679918450562e-09, 5.09683995922528e-09])
    return pressure_array, permeability_iso_array

def calc_perm_from_pressure_and_K(num_samples:int):
    # permeability values are calculated from the hydraulic conductivity values
    # values: same as in diss.tex (24.2.23)
    K_min, K_max = (1e-4, 5e-2)
    dynamic_viscosity_water = 1e-3
    rho_water = 1000
    g = 9.81

    hydraulic_conductivity = 10 ** np.random.uniform(np.log10(K_min), np.log10(K_max), num_samples) #-1)
    permeability_array = hydraulic_conductivity * dynamic_viscosity_water / (rho_water * g)
    return permeability_array

def calc_pressure_and_perm_fields(number_datapoints:int, dataset_folder:str, vary_perm_field:bool, benchmark_bool:bool = False):
    
    if number_datapoints == 0: # benchmark case 1hp, iso perm --> 4 datapoints
        pressure_array, permeability_iso_array = benchmark_pressure_perm()
    elif benchmark_bool: # benchmark case 2hps, varying perm
        pressure_array = np.array([-0.0015])
        permeability_iso_array = np.array([[9.0193679918450561e-11, 2.038735983690112e-10]])
    else: # normal dataset
        pressure_array = np.random.uniform(-0.0035, -0.0015, number_datapoints)
        permeability_iso_array = calc_perm_from_pressure_and_K(len(pressure_array))

        if vary_perm_field: # vary perm field case
            # calc max and min perm values
            perm_iso_array_2 = calc_perm_from_pressure_and_K(len(pressure_array))

            # zip the two arrays together
            perm_iso_array_2 = perm_iso_array_2.reshape(-1, 1)
            perm_iso_array_1 = permeability_iso_array.reshape(-1, 1)
            permeability_iso_array = np.concatenate((perm_iso_array_1, perm_iso_array_2), axis=1)

    # save pressure and permeability values
    with open(dataset_folder+"/pressure_values.txt", "w") as pressure_file:
        np.savetxt(pressure_file, pressure_array)
    with open(dataset_folder+"/permeability_values.txt", "w") as permeability_file:
        np.savetxt(permeability_file, permeability_iso_array)

    return pressure_array, permeability_iso_array