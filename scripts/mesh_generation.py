import numpy as np
import pathlib
from typing import Dict, Tuple
import logging

from scripts.utils import save_yaml
from scripts.mesh_generation_utils import create_regular_cell_centers, create_regular_cell_volumes, calc_n_faces, create_regular_face_areas, create_regular_faces_ids, create_regular_faces_centers, correct_face_ids, calc_n_cells_array
from scripts.mesh_generation_utils import store_mesh

# REGULAR GRID GENERATION
def create_regular_grid(settings:Dict) -> Tuple[Dict[str, np.ndarray], np.array]:

    n_cells = calc_n_cells_array(settings)
    cell_centers = create_regular_cell_centers(settings["grid"]["resolution"], n_cells)
    logging.warning("ACHTUNG!! andere reihenfolge der zellen!!") 
    volumes = create_regular_cell_volumes(settings["grid"]["resolution"], n_cells)
    n_faces = calc_n_faces(n_cells)
    face_areas = create_regular_face_areas(settings["grid"]["resolution"], n_faces)
    face_cell_ids = create_regular_faces_ids(cell_centers, settings["grid"]["resolution"], n_cells, n_faces)
    face_centers = create_regular_faces_centers(face_cell_ids, cell_centers, n_faces)
    face_cell_ids = correct_face_ids(face_cell_ids)

    return {"cell_centers": cell_centers, "cell_volumes": volumes, "face_areas": face_areas, "face_cell_ids": face_cell_ids, "face_centers": face_centers}, n_cells

def mesh_generation_all_dps(settings:Dict, output_dir:pathlib.Path, windows_collected:list[dict], orig_resolution:float) -> list[Dict[str, np.ndarray]]:
    meshs = []
    for id, window in enumerate(windows_collected):
        output_run_dir = output_dir / f"RUN_{id}"
        desti_resolution = settings["grid"]["resolution"]
        assert desti_resolution >=1, "not implemented for resolution <1 yet"

        # 9. generate mesh (height added to ncells, NOT to window_shape)
        # TODO include height
        ncells = window["shape"][...] * orig_resolution / desti_resolution

        if False:
            ncells = np.append(ncells, np.ceil(window_height_in_meters / desti_resolution))
        else:
            ncells = np.append(ncells, 1)
        ncells = ncells.astype(int)
        if len(settings["grid"]["size [m]"]) == 2:
            settings["grid"]["size [m]"].append(int(ncells[2] * desti_resolution))
        else:
            settings["grid"]["size [m]"][2] = int(ncells[2] * desti_resolution)
        save_yaml(settings, output_run_dir)
        mesh, _ = create_regular_grid(settings)

        # store mesh
        store_mesh(output_run_dir, mesh)

        meshs.append(mesh)

    return meshs