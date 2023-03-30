import numpy as np
import sys
from typing import Union

def benchmark_pressure_perm():
    # benchmark: 3 testcases (see diss.tex)
    pressure_array = np.array([-0.0015, -0.0015, -0.003, -0.0035])
    permeability_iso_array = np.array([1.0193679918450561e-11, 2.038735983690112e-10, 1.0193679918450562e-09, 5.09683995922528e-09])
    return pressure_array, permeability_iso_array

def make_pressure_array(number_datapoints):
    # random pressure values between -0.0035 and -0.0015
    pressure_array = np.random.uniform(-0.0035, -0.0015, number_datapoints)
    # pressure_array = np.append(pressure_array, -0.0015)
    return pressure_array

def calc_perm_from_pressure_and_K(pressure_array):
    # permeability values are calculated from the pressure values
    # values: same as in diss.tex (24.2.23)
    K_min, K_max = (1e-4, 5e-2)
    dynamic_viscosity_water = 1e-3
    rho_water = 1000
    g = 9.81

    hydraulic_conductivity = 10 ** np.random.uniform(np.log10(K_min), np.log10(K_max), len(pressure_array)) #-1)
    permeability_array = hydraulic_conductivity * dynamic_viscosity_water / (rho_water * g)
    # permeability_array = np.append(permeability_array, 2.038735983690112025e-10) # add the permeability of the benchmark testcase
    return permeability_array

def calc_pressure_and_perm_fields(number_datapoints:Union[int, str], dataset_folder:str, vary_perm_field:bool):
    
    if number_datapoints == "benchmark_4_testcases":
        pressure_array, permeability_iso_array = benchmark_pressure_perm()
    else: # normal dataset
        pressure_array = make_pressure_array(number_datapoints)
        permeability_iso_array = calc_perm_from_pressure_and_K(pressure_array)

        if vary_perm_field: # vary perm field case
            # calc max and min perm values
            perm_iso_array_2 = calc_perm_from_pressure_and_K(pressure_array)

            # zip the two arrays together
            perm_iso_array_2 = perm_iso_array_2.reshape(-1, 1)
            perm_iso_array_1 = permeability_iso_array.reshape(-1, 1)
            permeability_iso_array = np.concatenate((perm_iso_array_1, perm_iso_array_2), axis=1)

    pressure_file = open(dataset_folder+"/pressure_values.txt", "w")
    np.savetxt(pressure_file, pressure_array)
    permeability_file = open(dataset_folder+"/permeability_values.txt", "w")
    np.savetxt(permeability_file, permeability_iso_array)

    return pressure_array, permeability_iso_array
    
  
if __name__ == "__main__":

    dataset_folder = sys.argv[1]

    if sys.argv[2] == "benchmark_4_testcases":
        pressure_array, permeability_iso_array = benchmark_pressure_perm()
    else: # normal dataset
        number_datapoints = int(sys.argv[2])
        pressure_array = make_pressure_array(number_datapoints)
        permeability_iso_array = calc_perm_from_pressure_and_K(pressure_array)

        if sys.argv[3] != "false":
            # vary perm field case
            # calc max and min perm values
            perm_iso_array_2 = calc_perm_from_pressure_and_K(pressure_array)

            # zip the two arrays together
            perm_iso_array_2 = perm_iso_array_2.reshape(-1, 1)
            perm_iso_array_1 = permeability_iso_array.reshape(-1, 1)
            permeability_iso_array = np.concatenate((perm_iso_array_1, perm_iso_array_2), axis=1)

    pressure_file = open(dataset_folder+"/pressure_values.txt", "w")
    np.savetxt(pressure_file, pressure_array)
    permeability_file = open(dataset_folder+"/permeability_values.txt", "w")
    np.savetxt(permeability_file, permeability_iso_array)
    