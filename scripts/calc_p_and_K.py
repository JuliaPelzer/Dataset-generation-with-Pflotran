import sys
from typing import Union

import numpy as np


def benchmark_pressure_perm():
    # benchmark: 3 testcases (see diss.tex)
    pressure_array = np.array([-0.0015, -0.0015, -0.003, -0.0035])
    permeability_iso_array = np.array(
        [
            1.0193679918450561e-11,
            2.038735983690112e-10,
            1.0193679918450562e-09,
            5.09683995922528e-09,
        ]
    )
    return pressure_array, permeability_iso_array


def calc_perm_from_pressure_and_K(num_samples: int, random_bool: bool = True):
    # permeability values are calculated from the hydraulic conductivity values
    # values: same as in diss.tex (24.2.23)
    K_min, K_max = (1e-4, 5e-2)
    dynamic_viscosity_water = 1e-3
    rho_water = 1000
    g = 9.81

    hydraulic_conductivity = 10 ** np.random.uniform(np.log10(K_min), np.log10(K_max), num_samples)
    if not random_bool and num_samples == 2: # TODO NOT SAFE
        hydraulic_conductivity = np.array([K_min, K_max])
    permeability_array = (hydraulic_conductivity * dynamic_viscosity_water / (rho_water * g))
    # perm logdistributed between 10^-11 and 3*10^-10
    # permeability_array = 10 ** np.random.uniform(-11, np.log10(3*10**(-10)), num_samples) # for Danyal
    return permeability_array


def calc_pressure_and_perm_values(
    number_datapoints: int,
    dataset_folder: str,
    vary_perm_field: bool,
    vary_pressure_field: bool = False,
    benchmark_bool: bool = False,
    only_vary_distribution:bool = False,
):
    if number_datapoints == 0:  # benchmark case 1hp, iso perm --> 4 datapoints
        pressure_array, permeability_iso_array = benchmark_pressure_perm()
    
    elif benchmark_bool:  # benchmark case 2hps, varying perm
        pressure_array = np.array([-0.0016]) # -0.0020 Danyal
        if vary_perm_field:
            permeability_iso_array = np.array(
                [[9.0193679918450561e-11, 2.038735983690112e-10]]
            )
        else:
            permeability_iso_array = np.array([9e-11]) # 3e-10 Danyal
    else:  # normal dataset
        if not only_vary_distribution:
            const_perm_pressure = False
            if const_perm_pressure:
                pressure_array = np.array([-0.003,] * number_datapoints)
                permeability_iso_array = np.array([1e-10,] * number_datapoints)
                print(pressure_array, permeability_iso_array, number_datapoints)
            else:
                pressure_array = np.random.uniform(-0.0035, -0.0015, number_datapoints)
                permeability_iso_array = calc_perm_from_pressure_and_K(number_datapoints)
        else:
            pressure_array = np.array([-0.003,] * number_datapoints)

        if vary_perm_field:
            if only_vary_distribution:
                permeability_iso_array = calc_perm_from_pressure_and_K(2, random_bool=False)
                permeability_iso_array = np.array([permeability_iso_array,] * len(pressure_array))
            else:    
                # calc max and min perm values
                perm_iso_array_2 = calc_perm_from_pressure_and_K(len(pressure_array))
                permeability_iso_array = np.concatenate((permeability_iso_array.reshape(-1, 1),perm_iso_array_2.reshape(-1, 1)),axis=1)

        if vary_pressure_field:
            pressure_array_2 = np.random.uniform(-0.0035, -0.0015, number_datapoints)
            pressure_array = np.concatenate(
                (pressure_array.reshape(-1, 1), pressure_array_2.reshape(-1, 1)), axis=1
            )

    # save pressure and permeability values
    with open(dataset_folder / "pressure_values.txt", "w") as pressure_file:
        np.savetxt(pressure_file, pressure_array)
    with open(dataset_folder / "permeability_values.txt", "w") as permeability_file:
        np.savetxt(permeability_file, permeability_iso_array)

    return pressure_array, permeability_iso_array
