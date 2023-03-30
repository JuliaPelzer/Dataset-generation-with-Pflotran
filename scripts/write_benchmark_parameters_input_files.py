import logging
import sys
import os
import shutil
import numpy as np
try:
	from scripts.make_general_settings import load_settings
	from scripts.create_grid_unstructured import write_loc_well_file
	from scripts.write_next_perm_field import return_next_perm_file
except:
	from make_general_settings import load_settings
	from create_grid_unstructured import write_loc_well_file
	from write_next_perm_field import return_next_perm_file

def write_parameter_input_files(pressure_grad_y: float, perm_iso: float, output_dataset_dir: str, run_id: int, perm_variation: bool = False, settings = None, loc_hp1: list = None, loc_hp2: list = None):
	path_to_output = "."

	# create pressure gradient file
	pressure_gradient_x = 0
	pressure_gradient_y = pressure_grad_y
	pressure_gradient_z = 0
	pressure_text = f"    PRESSURE {pressure_gradient_x} {pressure_gradient_y} {pressure_gradient_z}"
	with open("interim_pressure_gradient.txt","w") as file:
		file.write(pressure_text)
	logging.info(f"Pressure Input: {pressure_gradient_x}, {pressure_gradient_y}, {pressure_gradient_z}")
	shutil.copy("interim_pressure_gradient.txt", os.path.join(output_dataset_dir, f"RUN_{run_id}", "pressure_gradient.txt"))
	
	# create permeability file (iso or field)
	if not perm_variation:
		permeability_iso = perm_iso
		permeability_text = f"    PERM_ISO {permeability_iso}"
		with open("interim_iso_permeability.txt","w") as file:
			file.write(permeability_text)
		logging.info(f"Permeability Input: {permeability_iso}")
		shutil.copy("interim_iso_permeability.txt", os.path.join(output_dataset_dir, f"RUN_{run_id}", "permeability_iso.txt"))
	else:
		perm_files_location = output_dataset_dir+"/permeability_fields"
		current_perm_file = return_next_perm_file(perm_files_location, run_id)
		current_perm_location = os.path.join(perm_files_location, current_perm_file)
		shutil.copy(current_perm_location, "./interim_permeability_field.h5")
		shutil.copy(current_perm_location, os.path.join(output_dataset_dir, f"RUN_{run_id}", current_perm_file))
	
	if loc_hp1 is not None:
		assert settings is not None, "Settings must be provided if loc_hp1 is provided"
		loc_hp1 = list(loc_hp1)
		loc_hp1.append(1)
		logging.info(f"HP1 Position: {loc_hp1}")
		write_loc_well_file(path_to_output, settings, loc_hp=loc_hp1, idx=1)
		shutil.copy("heatpump_inject1.vs", os.path.join(output_dataset_dir, f"RUN_{run_id}", "heatpump_inject1.vs"))

		if loc_hp2 is not None:
			loc_hp2 = list(loc_hp2)
			loc_hp2.append(1)
			logging.info(f"HP2 Position: {loc_hp2}")
			write_loc_well_file(path_to_output, settings, loc_hp=loc_hp2, idx=2)
			shutil.copy("heatpump_inject2.vs", os.path.join(output_dataset_dir, f"RUN_{run_id}", "heatpump_inject2.vs"))
 


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

	pressure_text = f"    PRESSURE {pressure_gradient_x} {pressure_gradient_y} {pressure_gradient_z}"
	with open("interim_pressure_gradient.txt","w") as file:
		file.write(pressure_text)
	logging.info(f"Pressure Input: {pressure_gradient_x}, {pressure_gradient_y}, {pressure_gradient_z}")

	permeability_text = f"    PERM_ISO {permeability_iso}"
	with open("interim_iso_permeability.txt","w") as file:
		file.write(permeability_text)
	logging.info(f"Permeability Input: {permeability_iso}")

	print(cla_args)
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
 
