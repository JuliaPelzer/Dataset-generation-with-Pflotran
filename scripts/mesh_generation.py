import numpy as np
import h5py
import pathlib
from typing import Dict

# CELLS
def create_regular_cell_centers(resolution, n_cells):
    '''a 2D float dataset with center’s XYZ coordinates per cells)'''

    # Create 1D arrays for each dimension
    x = (np.arange(n_cells[0]) + 0.5) * resolution
    y = (np.arange(n_cells[1]) + 0.5) * resolution
    z = (np.arange(n_cells[2]) + 0.5) * resolution

    # Create a meshgrid and reshape to get the cell centers
    xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
    cells = np.vstack([xv.ravel(), yv.ravel(), zv.ravel()]).T
    return cells

def correct_cell_ids(cell_ids, offset=0):
    cell_ids[:, 0] += offset
    return cell_ids

def create_regular_cell_volumes(resolution, n_cells):
    ''' a 1D float dataset with the volume of each cell'''
    volume = resolution**3
    cell_volumes = np.ones(n_cells)*volume
    # flatten the array
    cell_volumes = cell_volumes.flatten()
    return cell_volumes

# FACES
def calc_n_faces(n_cells):
    return (n_cells[0] - 1) * n_cells[1] * n_cells[2] + n_cells[0] * (n_cells[1] - 1) * n_cells[2] + n_cells[0] * n_cells[1] * (n_cells[2] - 1)

def create_regular_face_areas(resolution, n_faces):
    '''a 1D float dataset with the area of each connection'''
    area = resolution**2
    face_areas = np.ones(n_faces)*area
    return face_areas

def create_3D_mesh_with_cell_ids(cell_centers, resolution, n_cells):
    cell_ids = np.zeros((n_cells[0], n_cells[1], n_cells[2]), dtype=int)
    for cell_id, cell in enumerate(cell_centers):
        cell = (cell / resolution - 0.5).astype(int)
        cell_ids[cell[0], cell[1], cell[2]] = cell_id
    return cell_ids

def create_regular_faces_ids(cell_centers, resolution, n_cells, n_faces):
    '''a 2D integer dataset with the two cell ids on either side of the connection'''
    mesh_ids = create_3D_mesh_with_cell_ids(cell_centers, resolution, n_cells)

    x_faces = np.array([mesh_ids[:-1].flatten(), mesh_ids[1:].flatten()])
    y_faces = np.array([mesh_ids[:, :-1].flatten(), mesh_ids[:, 1:].flatten()])
    z_faces = np.array([mesh_ids[:, :, :-1].flatten(), mesh_ids[:, :, 1:].flatten()])
    cell_ids = np.concatenate((x_faces, y_faces, z_faces), axis=1).T
    assert len(cell_ids) == n_faces, f"{len(cell_ids)=} != {n_faces=}"

    return cell_ids

def correct_face_ids(face_cell_ids, offset=0):
    '''a 2D integer dataset with the two cell ids on either side of the connection'''
    face_cell_ids += offset
    return face_cell_ids

def create_regular_faces_centers(face_cell_ids, cell_centers, n_faces):
    '''a 2D float dataset with the center’s XYZ coordinates per connection'''
    centers = np.zeros((n_faces, 3))
    for i, face in enumerate(face_cell_ids):
        centers[i] = 0.5 * (cell_centers[face[1]] + cell_centers[face[0]])
    return centers

# REGULAR GRID GENERATION
def create_regular_grid(settings:Dict, destination:pathlib, return_dataset:bool=False, printing:bool=False):
    offset = 1
    out = h5py.File(destination/"mesh.h5", "w")

    n_cells = (np.array(settings["grid"]["size [m]"]) / settings["grid"]["resolution"]).astype(int)
    cell_centers = create_regular_cell_centers(settings["grid"]["resolution"], n_cells)
    print("ACHTUNG!! andere reihenfolge der zellen!!") 
    volumes = create_regular_cell_volumes(settings["grid"]["resolution"], n_cells)
    n_faces = calc_n_faces(n_cells)
    face_areas = create_regular_face_areas(settings["grid"]["resolution"], n_faces)
    face_cell_ids = create_regular_faces_ids(cell_centers, settings["grid"]["resolution"], n_cells, n_faces)
    face_centers = create_regular_faces_centers(face_cell_ids, cell_centers, n_faces)
    face_cell_ids = correct_face_ids(face_cell_ids, offset)

    out.create_dataset("Domain/Cells/Centers", data=cell_centers, dtype="f8")
    out.create_dataset("Domain/Cells/Volumes", data=volumes, dtype="f8")
    out.create_dataset("Domain/Connections/Areas", data=face_areas, dtype="f8")
    out.create_dataset("Domain/Connections/Cell Ids", data=face_cell_ids, dtype="i")
    out.create_dataset("Domain/Connections/Centers", data=face_centers, dtype="i")

    if printing:
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

    if return_dataset:
        return out
    else:
        out.close()
        # append cell_centers by their index in 1st dimension
        cell_ids = np.arange(np.prod(n_cells))
        cell_centers = np.hstack([cell_ids.reshape(-1, 1), cell_centers])
        cell_centers = correct_cell_ids(cell_centers, offset)
        if printing:
            print(f"{cell_centers[:10]=}")

        return cell_centers