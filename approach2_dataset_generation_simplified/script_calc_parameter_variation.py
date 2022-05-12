import numpy as np
import matplotlib.pyplot as plt
import sys

# calc pressure array
#pressure_array = np.random.uniform(
#  -0.00005, -0.003, 1
#)
param_dataset_size = int(sys.argv[1])
np.random.SeedSequence()
pressure_array = np.random.normal(
  loc=-0.0003, scale=0.0001, size=param_dataset_size # mu, sigma, e.g. size=100 
)
pressure_array.sort()

# save in txt file
pressure_file = open("parameter_values_pressure_y.txt", "w")
np.savetxt(pressure_file, pressure_array)


#y = [1 for i in range(0,100)]
#plt.scatter(pressure_array, y)
#plt.show()

## test values for pressure_y
#-0.00003
#-0.00004
#-0.00005
#-0.00006
#-0.00007
#-0.00008
#-0.00009
#-0.0001
#-0.0002
#-0.0003
#-0.0004
#-0.0005
#-0.0006
#-0.0007
#-0.0008
#-0.0009
#-0.001
#-0.002
#-0.003