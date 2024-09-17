import numpy as np
from typing import Dict
from pathlib import Path


def cut_bcs_hh(tok:np.array, gwgl:np.array) -> Dict[str, np.ndarray]:
    tok_min = np.nanmin(tok)
    bcs = {}

    bcs["inflow"]   = np.median(gwgl[0,:] - tok_min)
    bcs["outflow"]  = np.median(gwgl[-1,:] - tok_min)
    bcs["left"]     = np.median(gwgl[:,-1] - tok_min)  # in stream direction
    bcs["right"]    = np.median(gwgl[:,0] - tok_min)  # in stream direction

    # # sample
    # hydraulic_head = gwgl[0,:] - gwgl[-1,:]
    return bcs #, hydraulic_head

def save_bcs(filename: Path, bcs:Dict):
    for name, value in bcs.items():
        with open(filename / f"bc_{name}.txt", "w") as file:
            file.writelines(f"0. 0. {value}")