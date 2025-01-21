import numpy as np
from pathlib import Path

from scripts.mesh_generation_utils import loc_to_id


def get_boundary_cells_and_resolutions(mesh_refined, max_resolution:float, dim:int, offset:float, sign: int):
    # get boundary cell ids, calc their positions and get their resolution

    # get all cells with position = 1/2 their own resolution
    # boundary = np.where(meshs_refined[0]["cell_centers"][:, 0] == np.cbrt(meshs_refined[0]["cell_volumes"])/2)
    boundary = np.where(mesh_refined["cell_centers"][:, dim] == offset + sign * np.sqrt(mesh_refined["cell_volumes"]/max_resolution)/2) # TODO anpassen, sobald 3D refinement implementiert
    
    cells = mesh_refined["cell_centers"][boundary]
    resolutions = np.sqrt(mesh_refined["cell_volumes"][boundary]/max_resolution) # TODO anpassen, sobald 3D refinement implementiert auf np.cbrt ...

    cell_ids = np.zeros_like(cells[:, 0])
    for line, pos in enumerate(cells):
        cell_ids[line] = loc_to_id(mesh_refined["cell_centers"], pos)

    boundary_locs = cells.copy()
    boundary_locs[:, dim] = boundary_locs[:, dim] - sign*resolutions/2 # TODO NOW if east: + resolutions

    return np.concatenate([cell_ids[:, None], boundary_locs, resolutions[:, None]*max_resolution], axis=1)#


def create_boundary_locs(mesh_refined, direction:str, max_resolution:float, window_shape: np.ndarray, orig_resolution: float, output_dir:Path=Path(".")):
    
    if direction in ["west", "east"]:
        dim = 0
    elif direction in ["north", "south"]:
        dim = 1
    elif direction in ["top", "bottom"]:
        dim = 2
        raise NotImplementedError("3D not implemented yet - produces false results")
    else:
        raise ValueError("Invalid direction")

    if direction in ["west", "south", "bottom"]:
        offset = 0
        sign = +1
    elif direction in ["east", "north", "top"]:
        offset = window_shape[dim] * orig_resolution
        sign = -1

    boundary = get_boundary_cells_and_resolutions(mesh_refined, max_resolution, dim, offset, sign)

    # generate boundary file
    output_str = f"CONNECTIONS {len(boundary)}\n"
    for line in boundary:
        output_str += f"{int(line[0])} {line[1]} {line[2]} {line[3]} {line[4]}\n"

    with open(output_dir / f"{direction}.ex", "w") as file:
        file.writelines(output_str)

    return boundary[:,0].astype(int)