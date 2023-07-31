import yaml
from typing import List, Dict
import os


def load_yaml(path: str, file_name="settings") -> Dict:
    with open(os.path.join(path, f"{file_name}.yaml"), "r") as file:
        settings = yaml.safe_load(file)
    return settings


def save_yaml(settings: Dict, path: str, name_file: str = "settings"):
    with open(f"{path}/{name_file}.yaml", "w") as file:
        yaml.dump(settings, file)


def change_grid_domain_size(
    settings: Dict,
    case: str,
    grid_widths: List[int] = [100, 750, 80],
    number_cells: List[int] = [20, 150, 16],
    frequency: List[int] = [2, 4, 2],
) -> Dict:
    # if you want to change the size of the domain:
    if case == "square":
        settings["grid"]["ncells"] = [150, 150, 16]
        settings["grid"]["size"] = [750, 750, 80]
        settings["permeability"]["frequency"] = [4, 4, 2]
    elif case == "large":
        settings["grid"]["ncells"] = [20, 256, 16]
        settings["grid"]["size"] = [100, 1280, 80]
        settings["permeability"]["frequency"] = [2, 5, 2]
    else:
        settings["grid"]["ncells"] = number_cells
        settings["grid"]["size"] = grid_widths
        settings["permeability"]["frequency"] = frequency

    bool_loc_inside = all(
        item is True
        for item in [
            settings["grid"]["loc_hp"][i] < settings["grid"]["size"][i]
            for i in [0, 1, 2]
        ]
    )
    assert bool_loc_inside, "The heat pump lies outside of the grid domain"

    return settings


def main_change_grid_size(path, case, name_file="settings", **grid_args) -> Dict:
    settings = load_yaml(path)
    settings = change_grid_domain_size(settings, case=case, **grid_args)
    save_yaml(settings, path, name_file)
    return settings
