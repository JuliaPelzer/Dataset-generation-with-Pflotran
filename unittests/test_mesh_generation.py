import numpy as np
import pathlib
import os
import matplotlib.pyplot as plt

from scripts.hp_variation_2d import calc_hps_locs_float
from scripts.mesh_generation_utils import loc_to_id, calc_face_cell_ids
from scripts.mesh_generation import create_regular_cell_centers, create_regular_cell_volumes, create_regular_grid, mesh_generation_all_dps
from scripts.mesh_refinement_utils import calc_inner_face_centers
from scripts.mesh_refinement import mesh_refinements_all_dps
from scripts.main_helpers import groundwater_temp
from scripts.utils import save_yaml

    

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
    out, _ = create_regular_grid(settings)

    # Expected result
    cell_id_expected = 10

    # Actual result
    cell_id_calc = loc_to_id(out['cell_centers'], np.array(settings['grid']['loc_hp [m]']))

    # Test
    assert cell_id_expected == cell_id_calc, f"Expected: {cell_id_expected}, Actual: {cell_id_calc}"

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
    # Fixture
    num_dp = 1
    num_hp = 1
    orig_resolution = 10
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [20, 10, 5],
            "distance_to_border": 1,
        },
        "subsurface": {
            "hydraulic conductivity": 1e-5,
            "aquifer thickness": 5,
            "darcy velocity": 1,
        },
    }

    output_dataset_dir = pathlib.Path.cwd() / "dataset_tmp"
    output_dataset_dir.mkdir(exist_ok=True)
    for dp_id in range(num_dp):
        output_run_dir = output_dataset_dir / f"RUN_{dp_id}"
        output_run_dir.mkdir(exist_ok=True)

        save_yaml(settings, output_run_dir)

    shape_inputs = (np.array(settings["grid"]["size [m]"][:2])/10).astype(int)
    windows = [{"properties": {"hydraulic_conductivity": np.ones(shape_inputs)*settings["subsurface"]["hydraulic conductivity"], "thickness": np.ones(shape_inputs)*settings["subsurface"]["aquifer thickness"], "darcy_velocity": np.ones(shape_inputs)*settings["subsurface"]["darcy velocity"]}, "shape":shape_inputs},]*num_dp

    meshs = mesh_generation_all_dps(settings, output_dataset_dir, windows, orig_resolution)
    assert meshs[0]["cell_centers"].shape == (8, 3), "Wrong shape of cell_centers"
    assert meshs[0]["face_cell_ids"].shape == (10, 2), "Wrong shape of face_cell_ids"
    assert meshs[0]["face_centers"].shape == (10, 3), "Wrong shape of face_centers"

    
    hps_locs = calc_hps_locs_float(True, num_dp, num_hp, settings)
    # TODO fix position of hps, then see actual number of cells and include assertions accordingly - for after refinement
    hps_temps = np.ones_like(hps_locs[:,:,0])*(5+groundwater_temp())
    hps_rates = np.ones_like(hps_locs[:,:,0])*0.00024

    plt.subplot(211)
    plt.plot(meshs[0]["cell_centers"][:, 0], meshs[0]["cell_centers"][:, 1], "o")
    plt.plot(meshs[0]["face_centers"][:, 0], meshs[0]["face_centers"][:, 1], "x")
    plt.plot(hps_locs[0,:,0], hps_locs[0,:,1], "ro")
    plt.grid()
    plt.xlim(0, 20)
    plt.ylim(0, 10)

    meshs_refined = mesh_refinements_all_dps(num_dp, settings, meshs, hps_locs, hps_temps, hps_rates, windows, orig_resolution, output_dataset_dir)

    assert len(meshs_refined) == num_dp, "Different length of refined meshes to num_dp"
    assert meshs_refined[0]["cell_centers"].shape[0] == meshs_refined[0]["cell_volumes"].shape[0], "Different number of refined centers and volumes"
    assert meshs_refined[0]["face_cell_ids"].shape[0] == meshs_refined[0]["face_centers"].shape[0], "Different number of refined face cell ids and centers"
    assert meshs_refined[0]["cell_centers"].shape[1] == 3, "Refined centers have wrong shape"

    plt.subplot(212)
    plt.plot(meshs_refined[0]["cell_centers"][:, 0], meshs_refined[0]["cell_centers"][:, 1], "o")
    plt.plot(hps_locs[0,:,0], hps_locs[0,:,1], "ro")
    plt.grid()
    plt.xlim(0, 20)
    plt.ylim(0, 10)
    plt.show()