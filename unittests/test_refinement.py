import pathlib
import h5py
import numpy as np

def test_refinement():
    path_run = pathlib.Path("unittests/data_test_refine/RUN_0")
    with h5py.File(path_run/"mesh.h5", "r") as mesh_file:
        print(mesh_file["Domain/Connections"].keys())
        cell_centers = np.array(mesh_file["Domain/Cells/Centers"])
        cell_volumes = np.array(mesh_file["Domain/Cells/Volumes"])
        face_cell_ids = np.array(mesh_file["Domain/Connections/Cell Ids"])
        face_centers = np.array(mesh_file["Domain/Connections/Centers"])
        face_areas = np.array(mesh_file["Domain/Connections/Areas"])

    n_neighbors = np.zeros([len(cell_centers)])
    for neighbors_ids, face_center in zip(face_cell_ids, face_centers):
        neighbor1 = cell_centers[neighbors_ids[0]-1]
        neighbor2 = cell_centers[neighbors_ids[1]-1]
        res1 = np.cbrt(cell_volumes[neighbors_ids[0]-1])
        res2 = np.cbrt(cell_volumes[neighbors_ids[1]-1])
        distance1 = np.linalg.norm(face_center - neighbor1)
        distance2 = np.linalg.norm(face_center - neighbor2)
        n_neighbors[neighbors_ids[0]-1] += 1
        n_neighbors[neighbors_ids[1]-1] += 1
        if distance1 > res1 or distance2 > res2:
            print(neighbors_ids, face_center, neighbor1, neighbor2, res1, res2, distance1, distance2)
            assert False, "face center not in cell"

    # assert if ther is any entry in n_neighbors < 2
    assert np.any(n_neighbors >= 2), "There is a cell with less than 2 neighbors"
    # assert if there is any entry in n_neighbors > 24
    assert np.any(n_neighbors <= 24), "There is a cell with more than 24 neighbors"

    # assert if a face is wrong
    for (neighbor1, neighbor2), face_center, face_area in zip(face_cell_ids, face_centers, face_areas):
        n1pos = cell_centers[neighbor1-1].copy()
        n2pos = cell_centers[neighbor2-1].copy()
        print(neighbor1, neighbor2, face_center, n1pos, n2pos)
        not_shared_axis = np.argmax(np.abs(n1pos - n2pos))
        res1 = np.cbrt(cell_volumes[neighbor1-1])
        res2 = np.cbrt(cell_volumes[neighbor2-1])
        poss = [n1pos, n2pos]
        ress = [res1, res2]
        # take all values from the nx_pos with smaller res
        smaller_res = np.min(ress)
        smaller_arg_res = np.argmin(ress)
        face_calc = poss[smaller_arg_res].copy()
        face_calc[not_shared_axis] += smaller_res/2 if poss[smaller_arg_res][not_shared_axis] < poss[1-smaller_arg_res][not_shared_axis] else -smaller_res/2
        if not np.allclose(face_center, face_calc):
            print(not_shared_axis, n1pos, n2pos)
            print("Face center not", neighbor1, neighbor2, face_center, face_calc)
            assert False, "Face center not in the middle of the two neighbors"
        
        if not np.allclose(face_area, smaller_res**2):
            print("Face area not", face_area, smaller_res**2)
            assert False, "Face area is wrong"

    # there should at most be 8 cells with only 2 neighbors
    assert np.sum(n_neighbors == 2) <= 8, "There are more than 8 cells with only 2 neighbors"