import numpy as np
from pathlib import Path

from scripts.mesh_generation_utils import loc_to_id


def get_boundary_cells_and_resolutions(mesh_refined, max_resolution:float, dim:int, offset:float, sign: int):
    # get boundary cell ids, calc their positions and get their resolution

    # get all cells with position = 1/2 their own resolution
    atol = 1e-5
    boundary = np.where(np.abs(mesh_refined["cell_centers"][:, dim] - (offset + sign * np.cbrt(mesh_refined["cell_volumes"])/2)) < atol)[0]
    
    cells = mesh_refined["cell_centers"][boundary]
    resolutions = np.cbrt(mesh_refined["cell_volumes"][boundary])

    cell_ids = np.zeros_like(cells[:, 0])
    for line, pos in enumerate(cells):
        centers_and_ress = np.column_stack([mesh_refined["cell_centers"], np.cbrt(mesh_refined["cell_volumes"])])
        cell_ids[line] = loc_to_id(centers_and_ress, pos)

    boundary_locs = cells.copy()
    boundary_locs[:, dim] = boundary_locs[:, dim] - sign*resolutions/2 # TODO NOW if east: + resolutions

    return np.concatenate([cell_ids[:, None], boundary_locs, resolutions[:, None]*max_resolution], axis=1)


def create_boundary_locs(mesh_refined, direction:str, max_resolution:float, window_shape: np.ndarray, orig_resolution: float, output_dir:Path=Path(".")):
    if direction in ["west", "east"]:
        dim = 1
    elif direction in ["north", "south"]:
        dim = 0
    elif direction in ["top", "bottom"]:
        dim = 2
        raise NotImplementedError("3D not implemented yet - produces false results")
    else:
        raise ValueError("Invalid direction")

    if direction in ["west", "north", "bottom"]:
        offset = 0
        sign = +1
    elif direction in ["east", "south", "top"]:
        offset = window_shape[dim] * orig_resolution
        sign = -1

    boundary = get_boundary_cells_and_resolutions(mesh_refined, max_resolution, dim, offset, sign)

    # generate boundary file
    output_str = f"CONNECTIONS {len(boundary)}\n"
    for line in boundary:
        output_str += f"{int(line[0])} {np.round(line[1],8)} {np.round(line[2],8)} {np.round(line[3],8)} {np.round(line[4],8)}\n"

    with open(output_dir / f"{direction}.ex", "w") as file:
        file.writelines(output_str)
        
    return boundary[:,0].astype(int)