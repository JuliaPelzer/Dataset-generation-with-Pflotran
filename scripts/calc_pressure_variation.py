from copy import deepcopy
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

def sampling_random_OLD(param_dataset_size, debug):
    
    # random distribution : log-normal
    samples_clean = []
    number_runs = 0
    while not len(samples_clean) == param_dataset_size:
        samples = np.random.lognormal(np.log(0.0004), 0.8, int(param_dataset_size*1.2))
        samples = samples - 2* 0.0004 
        
        samples_clean = np.sort(samples)
        def negative(x):
            return x < 0
        number_negative_values = sum(negative(value) for value in samples_clean)
        samples_clean = samples_clean[:number_negative_values]
        number_runs += 1

        assert number_runs < 100, "ERROR no valid sample set found, see calc_pressure_variation line 30"
    
    if debug:
      log_bins = np.logspace(-3, -2.1, 100) - 7*10**-3
      count, bins, ignored = plt.hist(samples_clean, bins=log_bins)
      print(f"mean {np.mean(samples)}, var {np.var(samples)}, max {np.max(samples)}, min {np.min(samples)}")
      print(sum(count))
      print(count)
      print(np.max(bins), np.min(bins))
      plt.xscale('symlog')
      plt.grid()
      plt.show()

      print(samples_clean)
    return samples_clean

def sampling_regular_log(param_dataset_size):
    # regular spacing: logarithmically
    x_log = np.logspace(-6,-3.5,param_dataset_size)
    x_log = x_log * -1
    return x_log

def sampling_regular_uniform(param_dataset_size):
    # regular spacing: uniform
    if param_dataset_size == 1:
      return np.array([-0.002])
    else:
      value_start = -0.001 #-1*10**-6 #
      value_stop = -0.01 #-2.5*10**-4 #-0.005 #fabian:
      x_array = np.linspace(value_start, value_stop, param_dataset_size)
      return x_array
  
def sampling_regular_uniform_2D(param_dataset_size):
    samples_pressure_sqrt = math.isqrt(param_dataset_size)+1
    total_pressure = sampling_regular_uniform(samples_pressure_sqrt)

    pressure_array_2D = []
    for value in total_pressure:
      pressure_x_array = np.linspace(0, value/2, samples_pressure_sqrt)
      pressure_y_array = - np.sqrt(value**2 - pressure_x_array**2)
      pressure_array_2D += zip(pressure_x_array, pressure_y_array)

    return pressure_array_2D

if __name__ == "__main__":
  debug = False

  # set dataset size
  if not debug:
    param_dataset_size = int(sys.argv[1])
    dataset_folder = sys.argv[2]
  else:
    param_dataset_size = 20

  if sys.argv[3] == "1D":
    case = "1D"
  else:
    case = "2D"

  if case=="1D":
    pressure_array = sampling_regular_uniform(param_dataset_size)
    pressure_file = open(dataset_folder+"/pressure_values.txt", "w")
    np.savetxt(pressure_file, pressure_array)
  elif case=="2D":
    pressure_array_2D = sampling_regular_uniform_2D(param_dataset_size)
    with open(dataset_folder+"/pressure_values.txt", "w") as f:
      f.writelines([f"{value[0]} {value[1]}\n" for value in pressure_array_2D])