import numpy as np
import pathlib
import os

from scripts.mesh_generation_utils import loc_to_id, calc_face_cell_ids
from scripts.mesh_generation import create_regular_cell_centers, create_regular_cell_volumes, create_regular_grid
from scripts.mesh_refinement_utils import calc_inner_face_centers

def test_create_regular_cell_centers():
    # Fixture
    resolution = 5.
    n_cells = (4, 3, 7)

    # Expected result
    def v1(resolution, n_cells):
        xGrid, yGrid, zGrid = n_cells
        
        cells = np.ndarray((np.prod(n_cells), 3))
        cellID_1 = 0
        for i in range(0, xGrid):
            xloc = (i + 0.5) * resolution
            for j in range(0, yGrid):
                yloc = (j + 0.5) * resolution
                for k in range(0, zGrid):
                    zloc = (k + 0.5) * resolution
                    cells[cellID_1] = [xloc, yloc, zloc]
                    cellID_1 += 1
        return cells
    
    expected = v1(resolution, n_cells)
    # print(expected[:10])

    # Actual result
    actual = create_regular_cell_centers(resolution, n_cells)
    # print(actual[:10])

    # Test
    assert np.allclose(actual, expected)

def test_create_regular_cell_volumes():
    # Fixture
    resolution = 5.
    n_cells = (4, 3, 2)

    # Expected result
    expected_volume = 125*np.ones(np.prod(n_cells))

    # Actual result
    actual = create_regular_cell_volumes(resolution, n_cells)

    # Test
    assert np.allclose(actual, expected_volume)

def test_loc_to_id():
    # Fixture
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [20, 15, 10], #100
            "loc_hp [m]": [10, 7, 10],
        }
    }
    out, _ = create_regular_grid(settings, pathlib.Path.cwd())

    # Expected result
    cell_id_expected = 10

    # Actual result
    cell_id_calc = loc_to_id(out['Domain/Cells/Centers'], np.array(settings['grid']['loc_hp [m]']))

    # Test
    assert cell_id_expected == cell_id_calc, f"Expected: {cell_id_expected}, Actual: {cell_id_calc}"

    # Clean up
    out.close()
    os.remove(pathlib.Path.cwd() / "mesh.h5")

def test_calc_face_cell_ids():
    # Fixture
    faces_res_orient = [
        [10, 2.5, 2.5, 5, 0], 
        [15, 2.5, 2.5, 5, 0]
    ]
    centers = np.array([[5, 5, 2.5], [12.5, 2.5, 2.5], [12.5, 7.5, 2.5], [17.5, 2.5, 2.5], [17.5, 7.5, 2.5]])

    # Expected result
    expected = np.array([[1, 2], [2, 4]])

    # Actual result
    actual = calc_face_cell_ids(faces_res_orient, centers)

    # Test
    assert np.allclose(actual, expected)

def test_calc_inner_face_centers():
    # Fixture
    centers = np.array([[22.65625,  2.03125,  2.5,      0.3125 ],
    [22.65625,  2.34375,  2.5,      0.3125 ],
    [22.96875,  2.03125,  2.5,      0.3125 ],
    [22.96875,  2.34375,  2.5,      0.3125 ]])

    # Expected result
    expected = np.array([[22.65625, 2.1875, 2.5, 0.3125],
    [22.8125, 2.34375, 2.5, 0.3125],
    [22.96875, 2.1875, 2.5, 0.3125],
    [22.8125, 2.03125, 2.5, 0.3125]])

    # Actual result
    actual = calc_inner_face_centers(centers)

    # Test
    assert np.allclose(actual, expected)

if __name__ == "__main__":
    test_loc_to_id()