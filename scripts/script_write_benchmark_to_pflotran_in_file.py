# vary grad(p)

import logging
import sys

if __name__ == "__main__":
      # read input parameters
      cla_args = sys.argv

      # how much output should be printed
      logging.basicConfig(level = cla_args[1])
      #logging.info(f"input arguments: {cla_args}")

      # test varying pressure gradient and permeabilities, for one heat pump (BENCHMARK)
      pressure_gradient_x = 0
      pressure_gradient_y = cla_args[2]
      pressure_gradient_z = 0
      permeability_iso = cla_args[3]

      pressure_text = f"    LIQUID_PRESSURE {pressure_gradient_x} {pressure_gradient_y} {pressure_gradient_z}"
      with open("interim_pressure_gradient.txt","w") as file:
        file.write(pressure_text)
      logging.info(f"Pressure Input: {pressure_gradient_x}, {pressure_gradient_y}, {pressure_gradient_z}")
      permeability_text = f"    PERM_ISO {permeability_iso}"
      with open("interim_iso_permeability.txt","w") as file:
        file.write(permeability_text)
      logging.info(f"Permeability Input: {permeability_iso}")