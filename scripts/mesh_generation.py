import numpy as np
import h5py
import pathlib
from typing import Dict, Tuple
import logging

from scripts.mesh_generation_utils import create_regular_cell_centers, create_regular_cell_volumes, calc_n_faces, create_regular_face_areas, create_regular_faces_ids, create_regular_faces_centers, correct_face_ids, calc_n_cells_array
from scripts.mesh_generation_boundaries import create_SN_boundaries, create_WE_boundaries, create_TB_boundaries

# REGULAR GRID GENERATION
def create_regular_grid(settings:Dict, destination:pathlib) -> Tuple[h5py.File, np.array]:
    out = h5py.File(destination/"mesh.h5", "w")

    n_cells = calc_n_cells_array(settings)
    cell_centers = create_regular_cell_centers(settings["grid"]["resolution"], n_cells)
    logging.warning("ACHTUNG!! andere reihenfolge der zellen!!") 
    volumes = create_regular_cell_volumes(settings["grid"]["resolution"], n_cells)
    n_faces = calc_n_faces(n_cells)
    face_areas = create_regular_face_areas(settings["grid"]["resolution"], n_faces)
    face_cell_ids = create_regular_faces_ids(cell_centers, settings["grid"]["resolution"], n_cells, n_faces)
    face_centers = create_regular_faces_centers(face_cell_ids, cell_centers, n_faces)
    face_cell_ids = correct_face_ids(face_cell_ids)

    out.create_dataset("Domain/Cells/Centers", data=cell_centers, dtype="f8")
    out.create_dataset("Domain/Cells/Volumes", data=volumes, dtype="f8")
    out.create_dataset("Domain/Connections/Areas", data=face_areas, dtype="f8")
    out.create_dataset("Domain/Connections/Cell Ids", data=face_cell_ids, dtype="i")
    out.create_dataset("Domain/Connections/Centers", data=face_centers, dtype="f8")

    if False:
        print(f"{n_cells=}")
        print(f"{cell_centers[:10]=}")
        print(f"{volumes[:10]=}")
        print(f"{n_faces=}")
        print(f"{face_cell_ids[:10]=}")
        print(f"{face_centers[:10]=}")
        print(f"{out['Domain/Cells/Centers'].shape=}", f"{out['Domain/Cells/Centers'][0]=}")
        print(f"{out['Domain/Cells/Volumes'].shape=}", f"{out['Domain/Cells/Volumes'][0]=}")
        print(f"{out['Domain/Connections/Areas'].shape=}")
        print(f"{out['Domain/Connections/Cell Ids'].shape=}")
        print(f"{out['Domain/Connections/Centers'].shape=}")

    return out, n_cells

def create_mesh_files(path_to_output: pathlib.Path, settings: Dict):
    # cells_all = write_mesh_file(path_to_output, settings)
    dataset_grid, n_cells = create_regular_grid(settings, path_to_output)
    
    cells_N, cells_S = create_SN_boundaries(path_to_output, settings["grid"]["resolution"], n_cells, dataset_grid["Domain/Cells/Centers"], north_position = settings["grid"]["size [m]"][1], south_position = 0)
    cells_W, cells_E = create_WE_boundaries(path_to_output, settings["grid"]["resolution"], n_cells, dataset_grid["Domain/Cells/Centers"], west_position = 0, east_position = settings["grid"]["size [m]"][0])
    cells_T, cells_B = create_TB_boundaries(path_to_output, settings["grid"]["resolution"], n_cells, dataset_grid["Domain/Cells/Centers"], top_position = settings["grid"]["size [m]"][2], bottom_position = 0)

    return dataset_grid, {"north": cells_N, "south": cells_S, "west": cells_W, "east": cells_E, "top": cells_T, "bottom": cells_B}