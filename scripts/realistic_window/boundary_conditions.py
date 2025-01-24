import numpy as np
from typing import Dict
from pathlib import Path

def get_bcs_values(tok:np.array, gwgl:np.array, bcs_cell_ids: Dict[str, np.ndarray], box_shape_in_m: float) -> Dict[str, np.ndarray]:
    # only [1:3] in case of 2D
    
    tok_min = np.nanmin(tok)

    bcs = {}
    bcs["west"]   = - np.median(gwgl[bcs_cell_ids["west"]-1] - tok_min)/box_shape_in_m[0]
    bcs["east"]  = - np.median(gwgl[bcs_cell_ids["east"]-1] - tok_min)/box_shape_in_m[0]
    bcs["north"]     = - np.median(gwgl[bcs_cell_ids["north"]-1] - tok_min)/box_shape_in_m[1]  # in stream direction
    bcs["south"]    = - np.median(gwgl[bcs_cell_ids["south"]-1] - tok_min)/box_shape_in_m[1]  # in stream direction
    # TODO top, bottom
    bcs["initial"]  = (bcs["west"] + bcs["east"])/2
    print("bcs", bcs)
    return bcs

def save_bcs(filename: Path, bcs:Dict):
    for name, value in bcs.items():
        with open(filename / f"bc_{name}.txt", "w") as file:
            file.write(f"LIQUID_PRESSURE 0. {format(value, 'f')} 0.")
            # file.write(f"""! <time> <valueX, valueY, valueZ>\n0. 0. 0. {value}""")
            