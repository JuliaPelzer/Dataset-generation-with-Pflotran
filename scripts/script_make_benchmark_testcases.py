import numpy as np
import sys

def benchmark_pressure_perm():
    # benchmark: 3 testcases (see diss.tex)
    pressure_array = [-0.0015, -0.003, -0.0035]
    permeability_iso_array = [2.038735983690112e-10, 1.0193679918450562e-09, 5.09683995922528e-09]
    return pressure_array, permeability_iso_array
  
if __name__ == "__main__":

    dataset_folder = sys.argv[1]
    pressure_array, permeability_iso_array = benchmark_pressure_perm()
    pressure_file = open(dataset_folder+"/pressure_values.txt", "w")
    np.savetxt(pressure_file, pressure_array)
    permeability_file = open(dataset_folder+"/permeability_values.txt", "w")
    np.savetxt(permeability_file, permeability_iso_array)
    