import numpy as np
from typing import Dict
import logging

# n_cells
def calc_n_cells_array(settings:Dict):
    n_cells = (np.array(settings["grid"]["size [m]"]) / settings["grid"]["resolution"]).astype(int)
    return n_cells

# CELLS
def create_regular_cell_centers(resolution:int, n_cells:np.array):
    '''a 2D float dataset with center’s XYZ coordinates per cells)'''

    # Create 1D arrays for each dimension
    x = (np.arange(n_cells[0]) + 0.5) * resolution
    y = (np.arange(n_cells[1]) + 0.5) * resolution
    z = (np.arange(n_cells[2]) + 0.5) * resolution

    # Create a meshgrid and reshape to get the cell centers
    xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
    cells = np.vstack([xv.ravel(), yv.ravel(), zv.ravel()]).T
    return cells

def correct_cell_ids(cell_ids:np.array, offset:int=1):
    cell_ids[:, 0] += offset
    return cell_ids

def create_regular_cell_volumes(resolution:int, n_cells:np.array):
    ''' a 1D float dataset with the volume of each cell'''
    volume = resolution**3
    cell_volumes = np.ones(n_cells)*volume
    # flatten the array
    cell_volumes = cell_volumes.flatten()
    return cell_volumes

def loc_to_id(cell_centers:np.array, position:np.array):
    '''find the cell id of a location'''
    if (position > cell_centers).any() or (position < 0).any():
        logging.info("loc_hp is outside/on boundary of domain")
    return np.argmin(np.linalg.norm(cell_centers - position, axis=1))+1

def id_to_loc(cell_centers:np.array, cell_id:int):
    '''find the location of a cell id'''
    return cell_centers[cell_id-1]

# FACES
def calc_n_faces(n_cells:np.array):
    return (n_cells[0] - 1) * n_cells[1] * n_cells[2] + n_cells[0] * (n_cells[1] - 1) * n_cells[2] + n_cells[0] * n_cells[1] * (n_cells[2] - 1)

def create_regular_face_areas(resolution:int, n_faces:int):
    '''a 1D float dataset with the area of each connection'''
    area = resolution**2
    face_areas = np.ones(n_faces)*area
    return face_areas

def create_3D_mesh_with_cell_ids(cell_centers:np.array, resolution:int, n_cells:np.array):
    cell_ids = np.zeros((n_cells[0], n_cells[1], n_cells[2]), dtype=int)
    for cell_id, cell in enumerate(cell_centers):
        cell = (cell / resolution - 0.5).astype(int)
        cell_ids[cell[0], cell[1], cell[2]] = cell_id
    return cell_ids

def create_regular_faces_ids(cell_centers:np.array, resolution:int, n_cells:np.array, n_faces:int):
    '''a 2D integer dataset with the two cell ids on either side of the connection'''
    mesh_ids = create_3D_mesh_with_cell_ids(cell_centers, resolution, n_cells)

    x_faces = np.array([mesh_ids[:-1].flatten(), mesh_ids[1:].flatten()])
    y_faces = np.array([mesh_ids[:, :-1].flatten(), mesh_ids[:, 1:].flatten()])
    z_faces = np.array([mesh_ids[:, :, :-1].flatten(), mesh_ids[:, :, 1:].flatten()])
    cell_ids = np.concatenate((x_faces, y_faces, z_faces), axis=1).T
    assert len(cell_ids) == n_faces, f"{len(cell_ids)=} != {n_faces=}"

    return cell_ids

def correct_face_ids(face_cell_ids:np.array, offset:int=1):
    '''a 2D integer dataset with the two cell ids on either side of the connection'''
    face_cell_ids += offset
    return face_cell_ids

def create_regular_faces_centers(face_cell_ids:np.array, cell_centers:np.array, n_faces:int):
    '''a 2D float dataset with the center’s XYZ coordinates per connection'''
    centers = np.zeros((n_faces, 3))
    for i, face in enumerate(face_cell_ids):
        centers[i] = 0.5 * (cell_centers[face[1]] + cell_centers[face[0]])
    return centers