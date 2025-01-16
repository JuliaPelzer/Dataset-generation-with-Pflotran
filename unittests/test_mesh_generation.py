import numpy as np
import pathlib
import os
import matplotlib.pyplot as plt

from scripts.hp_variation_2d import calc_locs_hp_float
from scripts.mesh_generation_utils import loc_to_id, calc_face_cell_ids
from scripts.mesh_generation import create_regular_cell_centers, create_regular_cell_volumes, create_regular_grid
from scripts.mesh_refinement_utils import calc_inner_face_centers
from scripts.mesh_refinement import mesh_refinements_all_dps
    

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
    expected = np.array([[22.65625, 2.1875, 2.5, 0.3125, 1],
    [22.8125, 2.34375, 2.5, 0.3125, 0],
    [22.96875, 2.1875, 2.5, 0.3125, 1],
    [22.8125, 2.03125, 2.5, 0.3125, 0]])

    # Actual result
    actual = calc_inner_face_centers(centers)

    # Test
    assert np.allclose(actual, expected)

def test_mesh_refinement():
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [40, 30, 5], #100
            "loc_hp [m]": [1, 7, 7],
            "distance_to_border": [[0, 0], [0, 0], 0],
            "min resolution well (m)": 0.1,
            "min resolution plume (m)": 1,
        },
        "subsurface": {
            "hydraulic conductivity": 1e-5,
            "aquifer thickness": 5,
            "darcy velocity": 1,
        },
        "max pump": {
            "temperature": 5,
        }
    }
    goal_resolution = 0.1
    num_dp = 2
    num_hps = 4

    out, _  = create_regular_grid(settings, pathlib.Path.cwd())
    grids_global = np.array([out["Domain/Cells/Centers"],]*num_dp)
    face_areas = np.array([out["Domain/Connections/Areas"],]*num_dp)
    face_cell_ids_global = np.array([out["Domain/Connections/Cell Ids"],]*num_dp)
    face_centers_global = np.array([out["Domain/Connections/Centers"],]*num_dp)

    out.close()
    print(f"{grids_global.shape=}")
    print(f"{face_areas.shape=}")
    print(f"{face_cell_ids_global.shape=}")
    print(f"{face_centers_global.shape=}")

    dps_hps_locs_global = calc_locs_hp_float(True, num_dp, num_hps, settings)

    plt.subplot(211)
    plt.plot(grids_global[0][:, 0], grids_global[0][:, 1], "o")
    plt.plot(face_centers_global[0][:, 0], face_centers_global[0][:, 1], "x")
    plt.plot(dps_hps_locs_global[0,:,0], dps_hps_locs_global[0,:,1], "ro")
    plt.grid()
    plt.xlim(0, 40)
    plt.ylim(0, 30)

    print(f"{dps_hps_locs_global.shape=}")

    refined_cell_centers, refined_cell_volumes = mesh_refinements_all_dps(num_dp, settings, grids_global, face_centers_global, face_cell_ids_global, dps_hps_locs_global)
    print("#refined centers", len(refined_cell_centers), "refined center0-shape", refined_cell_centers[0].shape)
    print("#refined volumes", len(refined_cell_volumes), "refined volume0-shape", refined_cell_volumes[0].shape)
    assert len(refined_cell_centers) == len(refined_cell_volumes) == num_dp, "Different length of refined centers and volumes to num_dp"
    assert refined_cell_centers[0].shape[0] == refined_cell_volumes[0].shape[0], "Different number of refined centers and volumes"
    assert refined_cell_centers[0].shape[1] == 3, "Refined centers have wrong shape"

    plt.subplot(212)
    plt.plot(refined_cell_centers[0][:, 0], refined_cell_centers[0][:, 1], "o")
    plt.plot(dps_hps_locs_global[0,:,0], dps_hps_locs_global[0,:,1], "ro")
    plt.grid()
    plt.xlim(0, 40)
    plt.ylim(0, 30)
    plt.show()
    
if __name__ == "__main__":
    test_loc_to_id()