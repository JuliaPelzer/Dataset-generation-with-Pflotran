import os
from typing import Dict, List
import pathlib

import yaml


def load_yaml(path: pathlib.Path, file_name="settings") -> Dict:
    with open(path / f"{file_name}.yaml", "r") as file:
        settings = yaml.safe_load(file)
    return settings


def save_yaml(settings: Dict, path: pathlib.Path, name_file: str = "settings", kwargs = None):
    with open(f"{path}/{name_file}.yaml", "w") as file:
        if kwargs:
            yaml.dump(settings, file, **kwargs)
        else:
            yaml.dump(settings, file)