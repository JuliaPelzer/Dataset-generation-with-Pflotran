# vary grad(p)

import logging
import sys

if __name__ == "__main__":
      # parameters
      skip = 1
      file_pressure_grad = 0 #TODO

      # read input parameters
      cla_args = sys.argv

      # how much output should be printed
      logging.basicConfig(level = cla_args[1])
      #logging.info(f"input arguments: {cla_args}")

      # test varying pressure gradient, for one heat pump
      if len(cla_args) > 3:
        pressure_gradient_x = cla_args[3]
      else:
        pressure_gradient_x = 0
      pressure_gradient_y = cla_args[2]
      pressure_gradient_z = 0

      pressure_text = f"    PRESSURE {pressure_gradient_x} {pressure_gradient_y} {pressure_gradient_z}"
      with open("interim_pressure_gradient.txt","w") as file:
        file.write(pressure_text)
      logging.info(f"Pressure Input: {pressure_gradient_x}, {pressure_gradient_y}, {pressure_gradient_z}")