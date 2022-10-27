import numpy as np
import matplotlib.pyplot as plt
import sys

## calc pressure array

debug = False

# set dataset size
if not debug:
  param_dataset_size = int(sys.argv[1])
else:
  param_dataset_size = 20

def sampling_random(param_dataset_size, debug):
    
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

        if number_runs >= 100:
              print("ERROR no valid sample set found, see script_calc_parameter_variation line 30")
              exit()
    
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
    value_start = -1*10**-6
    value_stop = -2.5*10**-4
    x_array = np.linspace(value_start, value_stop, param_dataset_size)
    return x_array

# calc pressure array
pressure_array = sampling_regular_uniform(param_dataset_size)

if not debug:
  # save in txt file
  pressure_file = open("parameter_values_pressure_y.txt", "w")
  np.savetxt(pressure_file, pressure_array)

else:
  # print for debugging purposes
  y = [i for i in range(0,param_dataset_size)]
  #plt.scatter(pressure_array, y)
  #plt.show()