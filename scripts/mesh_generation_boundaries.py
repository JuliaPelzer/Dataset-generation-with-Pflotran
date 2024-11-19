import numpy as np
import pathlib

from scripts.mesh_generation_utils import loc_to_id

def create_SN_boundaries(path_to_output: pathlib.Path, resolution:int, n_cells:np.array, cell_centers:np.ndarray, north_position:float, south_position:float):

    face_area = resolution**2

    output_string_north = [f"CONNECTIONS {n_cells[0] * n_cells[2]}"]
    output_string_south = [f"CONNECTIONS {n_cells[0] * n_cells[2]}"]
    locs_north = np.ndarray((n_cells[0]*n_cells[2], 3))
    locs_south = np.ndarray((n_cells[0]*n_cells[2], 3))
    id = 0
    for k in range(0, n_cells[2]):
        loc_z = 0.5 * resolution + k * resolution
        for i in range(0, n_cells[0]):
            loc_x = (i + 0.5) * resolution
            locs_north[id] = [loc_x, north_position, loc_z]
            locs_south[id] = [loc_x, south_position, loc_z]
            cell_id_north = loc_to_id(cell_centers, locs_north[id])
            cell_id_south = loc_to_id(cell_centers, locs_south[id])
            output_string_north.append(f"\n{cell_id_north}  {locs_north[id][0]}  {locs_north[id][1]}  {locs_north[id][2]}  {face_area}")
            output_string_south.append(f"\n{cell_id_south}  {locs_south[id][0]}  {locs_south[id][1]}  {locs_south[id][2]}  {face_area}")
            id += 1

    with open(path_to_output / "north.ex", "w") as file:
        file.writelines(output_string_north)
    with open(path_to_output / "south.ex", "w") as file:
        file.writelines(output_string_south)

    return locs_north, locs_south

def create_WE_boundaries(path_to_output: pathlib.Path, resolution:int, n_cells:np.array, cell_centers:np.ndarray, west_position:float, east_position:float):

    face_area = resolution**2

    output_string_west = [f"CONNECTIONS {n_cells[1] * n_cells[2]}"]
    output_string_east = [f"CONNECTIONS {n_cells[1] * n_cells[2]}"]
    locs_west = np.ndarray((n_cells[1]*n_cells[2], 3))
    locs_east = np.ndarray((n_cells[1]*n_cells[2], 3))
    id = 0
    for k in range(0, n_cells[2]):
        loc_z = 0.5 * resolution + k * resolution
        for j in range(0, n_cells[1]):
            loc_y = (j + 0.5) * resolution
            locs_west[id] = [west_position, loc_y, loc_z]
            locs_east[id] = [east_position, loc_y, loc_z]
            cell_id_west = loc_to_id(cell_centers, locs_west[id])
            cell_id_east = loc_to_id(cell_centers, locs_east[id])
            output_string_west.append(f"\n{cell_id_west}  {locs_west[id][0]}  {locs_west[id][1]}  {locs_west[id][2]}  {face_area}")
            output_string_east.append(f"\n{cell_id_east}  {locs_east[id][0]}  {locs_east[id][1]}  {locs_east[id][2]}  {face_area}")
            id += 1

    with open(path_to_output / "west.ex", "w") as file:
        file.writelines(output_string_west)
    with open(path_to_output / "east.ex", "w") as file:
        file.writelines(output_string_east)

    return locs_west, locs_east


def create_TB_boundaries(path_to_output: pathlib.Path, resolution:int, n_cells:np.array, cell_centers: np.ndarray, top_position:float, bottom_position:float):
    
        face_area = resolution**2
    
        output_string_top = [f"CONNECTIONS {n_cells[0] * n_cells[1]}"]
        output_string_bottom = [f"CONNECTIONS {n_cells[0] * n_cells[1]}"]
        locs_top = np.ndarray((n_cells[0]*n_cells[1], 3))
        locs_bottom = np.ndarray((n_cells[0]*n_cells[1], 3))
        id = 0
        for j in range(0, n_cells[1]):
            loc_y = (j + 0.5) * resolution
            for i in range(0, n_cells[0]):
                loc_x = (i + 0.5) * resolution
                locs_top[id] = [loc_x, loc_y, top_position]
                locs_bottom[id] = [loc_x, loc_y, bottom_position]
                cell_id_top = loc_to_id(cell_centers, locs_top[id]) # WRONG
                cell_id_bottom = loc_to_id(cell_centers, locs_bottom[id]) # WRONG
                output_string_top.append(f"\n{cell_id_top}  {locs_top[id][0]}  {locs_top[id][1]}  {locs_top[id][2]}  {face_area}")
                output_string_bottom.append(f"\n{cell_id_bottom}  {locs_bottom[id][0]}  {locs_bottom[id][1]}  {locs_bottom[id][2]}  {face_area}")
                id += 1
    
        with open(path_to_output / "top.ex", "w") as file:
            file.writelines(output_string_top)
        with open(path_to_output / "bottom.ex", "w") as file:
            file.writelines(output_string_bottom)
    
        return locs_top, locs_bottom