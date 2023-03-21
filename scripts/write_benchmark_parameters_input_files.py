import logging
import sys
import numpy as np
from make_general_settings import load_settings
from create_grid_unstructured import write_loc_well_file

if __name__ == "__main__":
	# read input parameters
	cla_args = sys.argv

	# how much output should be printed
	logging.basicConfig(level = cla_args[1])

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

	if len(cla_args) > 4:
		hp_x = int(float(cla_args[4]))
		hp_y = int(float(cla_args[5]))
		hp_z = 1
		loc_hp = np.array([hp_x, hp_y, hp_z])
		path_to_output = "."

		logging.info(f"HP 1 Position: {loc_hp}")
		write_loc_well_file(path_to_output, settings=load_settings(path_to_output), loc_hp=loc_hp, idx=1)

		if len(cla_args) > 6:
			hp_x = int(float(cla_args[6]))
			hp_y = int(float(cla_args[7]))
			hp_z = 1
			loc_hp = np.array([hp_x, hp_y, hp_z])

			logging.info(f"HP 2 Position: {loc_hp}")
			write_loc_well_file(path_to_output, settings=load_settings(path_to_output), loc_hp=loc_hp, idx=2)
 
