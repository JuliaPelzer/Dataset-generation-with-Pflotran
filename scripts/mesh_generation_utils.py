import numpy as np
from typing import Dict
import logging
from pathlib import Path
import h5py

# n_cells
def calc_n_cells_array(settings:Dict):
    n_cells = (np.array(settings["grid"]["size [m]"]) / settings["grid"]["resolution"]).astype(int)
    return n_cells

# CELLS
def create_regular_cell_centers(resolution:int, n_cells:np.ndarray):
    '''a 2D float dataset with center’s XYZ coordinates per cells)'''

    # Create 1D arrays for each dimension
    x = (np.arange(n_cells[0]) + 0.5) * resolution
    y = (np.arange(n_cells[1]) + 0.5) * resolution
    z = (np.arange(n_cells[2]) + 0.5) * resolution

    # Create a meshgrid and reshape to get the cell centers
    xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
    cells = np.vstack([xv.ravel(), yv.ravel(), zv.ravel()]).T
    return cells

def correct_cell_ids(cell_ids:np.ndarray, offset:int=1):
    cell_ids[:, 0] += offset
    return cell_ids

def create_regular_cell_volumes(resolution:int, n_cells:np.ndarray):
    ''' a 1D float dataset with the volume of each cell'''
    volume = resolution**3
    cell_volumes = np.ones(n_cells)*volume
    # flatten the array
    cell_volumes = cell_volumes.flatten()
    return cell_volumes

def loc_to_id(cell_centers:np.ndarray, position:np.ndarray):
    '''find the cell id of a location'''
    # WARNING! this only works if no cells of 2 different resolutions are connected
    # if (position > cell_centers).any() or (position < 0).any():
    #     logging.info("loc_hp is outside/on boundary of domain")
    
    return int(np.argmin(np.sum((cell_centers - position)**2, axis=1))+1)

def id_to_loc(cell_centers:np.ndarray, cell_id:int):
    '''find the location of a cell id'''
    return cell_centers[int(cell_id)-1]

# FACES
def calc_n_faces(n_cells:np.ndarray):
    return (n_cells[0] - 1) * n_cells[1] * n_cells[2] + n_cells[0] * (n_cells[1] - 1) * n_cells[2] + n_cells[0] * n_cells[1] * (n_cells[2] - 1)

def create_regular_face_areas(resolution:int, n_faces:int):
    '''a 1D float dataset with the area of each connection'''
    area = resolution**2
    face_areas = np.ones(n_faces)*area
    return face_areas

def create_3D_mesh_with_cell_ids(cell_centers:np.ndarray, resolution:int, n_cells:np.ndarray):
    cell_ids = np.zeros((n_cells[0], n_cells[1], n_cells[2]), dtype=int)
    for cell_id, cell in enumerate(cell_centers):
        cell = (cell / resolution - 0.5).astype(int)
        cell_ids[cell[0], cell[1], cell[2]] = cell_id
    return cell_ids

def create_regular_faces_ids(cell_centers:np.ndarray, resolution:int, n_cells:np.ndarray, n_faces:int):
    '''a 2D integer dataset with the two cell ids on either side of the connection'''
    mesh_ids = create_3D_mesh_with_cell_ids(cell_centers, resolution, n_cells)

    x_faces = np.array([mesh_ids[:-1].flatten(), mesh_ids[1:].flatten()])
    y_faces = np.array([mesh_ids[:, :-1].flatten(), mesh_ids[:, 1:].flatten()])
    z_faces = np.array([mesh_ids[:, :, :-1].flatten(), mesh_ids[:, :, 1:].flatten()])
    cell_ids = np.concatenate((x_faces, y_faces, z_faces), axis=1).T
    assert len(cell_ids) == n_faces, f"{len(cell_ids)=} != {n_faces=}"

    return cell_ids

def correct_face_ids(face_cell_ids:np.ndarray, offset:int=1):
    '''a 2D integer dataset with the two cell ids on either side of the connection'''
    face_cell_ids += offset
    return face_cell_ids

def create_regular_faces_centers(face_cell_ids:np.ndarray, cell_centers:np.ndarray, n_faces:int):
    '''a 2D float dataset with the centers XYZ coordinates per connection'''
    centers = np.zeros((n_faces, 3), dtype=float)
    for i, face in enumerate(face_cell_ids):
        centers[i] = 0.5 * (cell_centers[face[1]] + cell_centers[face[0]])
    return centers

def get_neighboring_2cells_ids_of_face_pos(face_center, resolution, orientation, cell_centers_and_res):
    neighbors = np.array([face_center.copy()]*2)
    sign = np.array([-1, 1])
    offset = 0.75 * resolution
    neighbors[0,int(orientation)] += sign[0] * offset
    neighbors[1,int(orientation)] += sign[1] * offset
    neighbor_ids = np.zeros(2)
    for id in range(2):
        neighbor_ids[id] = loc_to_id(cell_centers_and_res[:,:3], neighbors[id])
    if neighbor_ids[0] == neighbor_ids[1]:
        logging.info(f"neighbors should be different, but are {neighbor_ids}")
        for id in range(2):
            found_neighbor_and_res = id_to_loc(cell_centers_and_res, neighbor_ids[id])
            if np.abs(found_neighbor_and_res[int(orientation)] - neighbors[id, int(orientation)]) > found_neighbor_and_res[3]:
                logging.info(f"this neighbor is wrong: {found_neighbor_and_res} != {neighbors[id]}, {id}")
                neighbors[id, int(orientation)] 
                neighbors[id, int(orientation)] -= sign[id] * offset
                neighbors[id, int(orientation)] += sign[id] * 0.75 * 4* resolution
                neighbor_ids[id] = loc_to_id(cell_centers_and_res[:,:3], neighbors[id])
                logging.info(f"corrected to {neighbors[id]}")
        assert neighbor_ids[0] != neighbor_ids[1], f"neighbors should be different, but are {neighbor_ids}"

    return neighbor_ids

def calc_face_cell_ids(faces_and_res_and_orient, cell_centers):
    face_cell_ids = []
    for x,y,z, res, orientation in faces_and_res_and_orient:
        neighbors = get_neighboring_2cells_ids_of_face_pos([x,y,z], res, orientation, cell_centers)
        face_cell_ids.append(neighbors)
    return np.array(face_cell_ids)

def face_loc_to_line(face_centers:np.ndarray, position:np.ndarray):
    '''find the cell id of a location'''
    if (position > face_centers).any() or (position < 0).any():
        logging.info("position is not a valid face")
    return np.argmin(np.linalg.norm(face_centers - position, axis=1))

def store_mesh(destination_path:Path, mesh:Dict[str, np.ndarray]):
    '''store the mesh in a file'''
    out = h5py.File(destination_path/"mesh.h5", "w")

    out.create_dataset("Domain/Cells/Centers", data=mesh["cell_centers"], dtype="f8")
    out.create_dataset("Domain/Cells/Volumes", data=mesh["cell_volumes"], dtype="f8")
    out.create_dataset("Domain/Connections/Areas", data=mesh["face_areas"], dtype="f8")
    out.create_dataset("Domain/Connections/Cell Ids", data=mesh["face_cell_ids"], dtype="i")
    out.create_dataset("Domain/Connections/Centers", data=mesh["face_centers"], dtype="f8")

    out.close()