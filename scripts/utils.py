import os
from time import time
from functools import wraps
import pathlib
from typing import Dict
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

def beep(case: str = "end"):
    duration = 0.05  # seconds
    freq = 440  # Hz
    os.system(f"play -nq -t alsa synth {duration} sine {freq}")
    if case == "end":
        freq = 640  # Hz
        os.system(f"play -nq -t alsa synth {duration} sine {freq}")

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' % \
          (f.__name__, te-ts))
        return result
    return wrap