import numpy as np
from typing import List, Tuple

def get_start_positions(data, info:dict) -> List[Tuple[int,int]]:
    ids = [(i,j) for i in range(data.shape[0]) for j in range(data.shape[1])]
    not_nan_ids = [id for id in ids if not np.isnan(data[id])]

    if info["random_bool"]:
        print("Randomizing order of windows")
        np.random.seed(info["seed_id"])
        np.random.shuffle(not_nan_ids)
    else:
        print("Not randomizing order of windows")

    return not_nan_ids

def random_delta_t() -> int:
    # random Anlageparameter: [2-6K]
    return np.random.randint(2, 7)

def sample_median(field: np.array, start_pos: np.array, field_size: np.array = np.array([100,100])):
    # general direction of flow is from south to north, hence to get as realistic median values as possible, we have to align this box in the same direction (relative to the start-position), hence the minus in front of the field_size[1]
    field = slice_box(field, start_pos, field_size)
    median = np.nanmedian(field)
    return median

def random_thresholded_v_tech(v_dd:float):
    # v_tech = random, with upper threshold (0.5l/s? - max-drawdown)
    lower_limit = 0.5 * 1E-3 # m^3/s
    assert v_dd >= lower_limit, f"max-drawdown with {v_dd} too low for v_tech formula"
    return np.random.uniform(lower_limit, v_dd * 1E-3)

def slice_box(field: np.array, start_pos: np.array, field_size: np.array = np.array([100,100])):
    field = field[start_pos[0]:start_pos[0]+field_size[0], start_pos[1]-field_size[1]:start_pos[1]]

    # falls alle Werte in der Box nan sind - dann jump einfahc zu nöchsten potentiellen Startpunkt ausprobieren
    if np.isnan(field).all():
        raise ValueError()
    return field