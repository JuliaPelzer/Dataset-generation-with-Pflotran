import yaml
from typing import List, Dict
# import numpy as np
# from dataclasses import dataclass

# @dataclass
# class Settings:
# 	random_bool      :   bool
# 	seed_id          :   int         =   2907
# 	# seed              :   int         =   np.random.seed(seed_id)

# 	def get_keys(self):
# 		return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]

# 	def get_next_value(self):
# 		for key in self.get_keys():
# 			yield getattr(self, key)

# 	def get_all_settings(self):
# 		return {key: getattr(self, key) for key in self.get_keys()}

# 	def all_settings_to_yaml(self, filename):
# 		# print settings to yaml file
# 		yaml_prep = self.get_all_settings()      
# 		for key, value in yaml_prep.items():
# 			if value.__class__ == np.ndarray:
# 				yaml_prep[key] = value.tolist()
# 			if value.__class__ == tuple:
# 				yaml_prep[key] = list(value)
# 		with open(filename, "w") as f:
# 			yaml.dump(yaml_prep, f)

#	def all_settings_to_str(self):
#		# for putting them into a settings file
#		return_str = ""
#		for key in self.get_keys():
#			return_str += f"{key} : {getattr(self, key)} \n"
#		return return_str

#	def load_settings(category:str):
#		with open("settings.yaml") as settings_file:
#			data = yaml.load(settings_file, Loader=SafeLoader)
#		return data[category]


def load_settings(path:str, file_name="settings") -> Dict:
	with open(f"{path}/{file_name}.yaml", "r") as file:
		settings = yaml.load(file, Loader=yaml.SafeLoader)
	return settings

def save_settings(settings:Dict, path:str, name_file:str="settings"):
	with open(f"{path}/{name_file}.yaml", "w") as file:
		yaml.dump(settings, file)

def change_grid_domain_size(settings:Dict, case:str, grid_widths:List[int]=[100,750,80], number_cells:List[int]=[20,150,16], frequency:List[int]=[2,4,2]) -> Dict:
	# if you want to change the size of the domain:
	if case=="square":
		settings["grid"]["ncells"] = [150,150,16]
		settings["grid"]["size"] = [750,750,80]
		settings["permeability"]["frequency"] = [4,4,2]
	elif case=="large":
		settings["grid"]["ncells"] = [20,256,16]
		settings["grid"]["size"] = [100,1280,80]
		settings["permeability"]["frequency"] = [2,5,2]
	else:
		settings["grid"]["ncells"] = number_cells
		settings["grid"]["size"] = grid_widths
		settings["permeability"]["frequency"] = frequency

	bool_loc_inside = all(item is True for item in [settings["grid"]["loc_hp"][i] < settings["grid"]["size"][i] for i in [0,1,2]])
	assert bool_loc_inside, "The heat pump lies outside of the grid domain"

	return settings

def main_change_grid_size(path, case, name_file="settings", **grid_args) -> Dict:
	settings = load_settings(path)
	settings = change_grid_domain_size(settings, case=case, **grid_args)
	save_settings(settings, path, name_file)
	return settings

if __name__ == "__main__":

	main_change_grid_size(path="Phd_simulation_groundtruth/scripts/scripts_permeability", case="large")