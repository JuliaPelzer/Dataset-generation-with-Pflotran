import numpy as np
from typing import Dict
from pathlib import Path


def cut_bcs_hh_v1(tok:np.array, gwgl:np.array) -> Dict[str, np.ndarray]:
    
    tok_min = np.nanmin(tok)
    bcs = {}

    bcs["inflow"]   = np.median(gwgl[0,:] - tok_min)
    bcs["outflow"]  = np.median(gwgl[-1,:] - tok_min)
    bcs["left"]     = np.median(gwgl[:,-1] - tok_min)  # in stream direction
    bcs["right"]    = np.median(gwgl[:,0] - tok_min)  # in stream direction

    # # sample
    # hydraulic_head = gwgl[0,:] - gwgl[-1,:]
    return bcs #, hydraulic_head

def cut_bcs_hh(tok:np.array, gwgl:np.array, cells: Dict[str, np.ndarray], desti_resolution:int, box_length_in_m: float) -> Dict[str, np.ndarray]:
    # only [1:3] in case of 2D
    bc_locs = {}
    for direction in ["north", "south", "west", "east"]:
        bc_locs[direction] = (cells[direction][:,1:3]//desti_resolution).astype(int)
        # print(bc_locs[direction][:10], gwgl.shape)

    tok_min = np.nanmin(tok)

    bcs = {}
    bcs["inflow"]   = - np.median(gwgl[bc_locs["north"]] - tok_min)/box_length_in_m
    bcs["outflow"]  = - np.median(gwgl[bc_locs["south"]] - tok_min)/box_length_in_m
    bcs["left"]     = - np.median(gwgl[bc_locs["east"]] - tok_min)/box_length_in_m  # in stream direction
    bcs["right"]    = - np.median(gwgl[bc_locs["west"]] - tok_min)/box_length_in_m  # in stream direction
    bcs["initial"]  = (bcs["outflow"] - bcs["inflow"])
    return bcs

def save_bcs(filename: Path, bcs:Dict):
    for name, value in bcs.items():
        with open(filename / f"bc_{name}.txt", "w") as file:
            file.write(f"LIQUID_PRESSURE 0. {format(value, 'f')} 0.")
            # file.write(f"""! <time> <valueX, valueY, valueZ>\n0. 0. 0. {value}""")
            