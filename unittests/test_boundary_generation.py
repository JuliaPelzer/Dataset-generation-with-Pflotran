import numpy as np
import pathlib
import os

from scripts.mesh_generation import create_regular_grid
from scripts.mesh_generation_boundaries import create_SN_boundaries, create_WE_boundaries, create_TB_boundaries

def test_SN():
    # Fixture
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [20, 15, 10],
            "loc_hp [m]": [10, 7, 7],
        }
    }
    out, n_cells = create_regular_grid(settings, pathlib.Path.cwd(), printing=False)

    # Expected result
    cells_N_expected = np.array([[ 2.5, 15., 2.5],
                                [ 7.5, 15., 2.5],
                                [12.5, 15., 2.5],
                                [17.5, 15., 2.5],
                                [ 2.5, 15., 7.5],
                                [ 7.5, 15., 7.5],
                                [12.5, 15., 7.5],
                                [17.5, 15., 7.5]])
    cells_S_expected = np.array([[ 2.5, 0., 2.5],
                                [ 7.5, 0., 2.5],
                                [12.5, 0., 2.5],
                                [17.5, 0., 2.5],
                                [ 2.5, 0., 7.5],
                                [ 7.5, 0., 7.5],
                                [12.5, 0., 7.5],
                                [17.5, 0., 7.5]])
    cell_ids_north_expected = np.array([5, 11, 17, 23, 6, 12, 18, 24])
    cell_ids_south_expected = np.array([1, 7, 13, 19, 2, 8, 14, 20])

    # Actual result
    cells_N, cells_S = create_SN_boundaries(pathlib.Path.cwd(), settings["grid"]["resolution"], n_cells, out["Domain/Cells/Centers"], north_position = settings["grid"]["size [m]"][1], south_position = 0)
    out.close()
    # load the files again
    with open(pathlib.Path.cwd() / "north.ex", "r") as file:
        lines = file.readlines()
        cell_ids_north = np.array([int(line.split()[0]) for line in lines[1:]])
    with open(pathlib.Path.cwd() / "south.ex", "r") as file:
        lines = file.readlines()
        cell_ids_south = np.array([int(line.split()[0]) for line in lines[1:]])

    # Assertion
    np.testing.assert_allclose(cells_N, cells_N_expected)
    np.testing.assert_allclose(cells_S, cells_S_expected)
    np.testing.assert_allclose(cell_ids_north, cell_ids_north_expected)
    np.testing.assert_allclose(cell_ids_south, cell_ids_south_expected)

    # Clean up
    os.remove(pathlib.Path.cwd() / "mesh.h5")
    os.remove(pathlib.Path.cwd() / "north.ex")
    os.remove(pathlib.Path.cwd() / "south.ex")

def test_WE():
    # Fixture
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [20, 15, 10],
            "loc_hp [m]": [10, 7, 7],
        }
    }
    out, n_cells = create_regular_grid(settings, pathlib.Path.cwd(), printing=False)

    # Expected result
    cells_W_expected = np.array([[ 0.,   2.5,  2.5],
                                [ 0.,   7.5,  2.5],
                                [ 0.,  12.5,  2.5],
                                [ 0.,   2.5,  7.5],
                                [ 0.,   7.5,  7.5],
                                [ 0.,  12.5,  7.5]])
    cells_E_expected = np.array([[20.,   2.5,  2.5],
                                [20.,   7.5,  2.5],
                                [20.,  12.5,  2.5],
                                [20.,   2.5,  7.5],
                                [20.,   7.5,  7.5],
                                [20.,  12.5,  7.5]])
    cell_ids_west_expected = np.array([1, 3, 5, 2, 4, 6])
    cell_ids_east_expected = np.array([19, 21, 23, 20, 22, 24])

    # Actual result
    cells_W, cells_E = create_WE_boundaries(pathlib.Path.cwd(), settings["grid"]["resolution"], n_cells, out["Domain/Cells/Centers"], west_position = 0, east_position = settings["grid"]["size [m]"][0])
    out.close()
    # load the files again
    with open(pathlib.Path.cwd() / "west.ex", "r") as file:
        lines = file.readlines()
        cell_ids_west = np.array([int(line.split()[0]) for line in lines[1:]])
    with open(pathlib.Path.cwd() / "east.ex", "r") as file:
        lines = file.readlines()
        cell_ids_east = np.array([int(line.split()[0]) for line in lines[1:]])

    # Assertion
    np.testing.assert_allclose(cells_W, cells_W_expected)
    np.testing.assert_allclose(cells_E, cells_E_expected)
    np.testing.assert_allclose(cell_ids_west, cell_ids_west_expected)
    np.testing.assert_allclose(cell_ids_east, cell_ids_east_expected)

def test_TB():
    # Fixture
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [20, 15, 10],
            "loc_hp [m]": [10, 7, 7],
        }
    }
    out, n_cells = create_regular_grid(settings, pathlib.Path.cwd(), printing=False)

    # Expected result
    cells_T_expected = np.array([[ 2.5,  2.5, 10.],
                                [ 7.5,  2.5, 10.],
                                [12.5,  2.5, 10.],
                                [17.5,  2.5, 10.],
                                [ 2.5,  7.5, 10.],
                                [ 7.5,  7.5, 10.],
                                [12.5,  7.5, 10.],
                                [17.5,  7.5, 10.],
                                [ 2.5, 12.5, 10.],
                                [ 7.5, 12.5, 10.],
                                [12.5, 12.5, 10.],
                                [17.5, 12.5, 10.]])
    cells_B_expected = np.array([[ 2.5,  2.5, 0.],
                                [ 7.5,  2.5, 0.],
                                [12.5,  2.5, 0.],
                                [17.5,  2.5, 0.],
                                [ 2.5,  7.5, 0.],
                                [ 7.5,  7.5, 0.],
                                [12.5,  7.5, 0.],
                                [17.5,  7.5, 0.],
                                [ 2.5, 12.5, 0.],
                                [ 7.5, 12.5, 0.],
                                [12.5, 12.5, 0.],
                                [17.5, 12.5, 0.]])
    cell_ids_top_expected = np.array([2, 8, 14, 20, 4, 10, 16, 22, 6, 12, 18, 24])
    cell_ids_bottom_expected = np.array([1, 7, 13, 19, 3, 9, 15, 21, 5, 11, 17, 23])

    # Actual result
    cells_T, cells_B = create_TB_boundaries(pathlib.Path.cwd(), settings["grid"]["resolution"], n_cells, out["Domain/Cells/Centers"], top_position = settings["grid"]["size [m]"][2], bottom_position = 0)
    out.close()
    # load the files again
    with open(pathlib.Path.cwd() / "top.ex", "r") as file:
        lines = file.readlines()
        cell_ids_top = np.array([int(line.split()[0]) for line in lines[1:]])
    with open(pathlib.Path.cwd() / "bottom.ex", "r") as file:
        lines = file.readlines()
        cell_ids_bottom = np.array([int(line.split()[0]) for line in lines[1:]])

    # Assertion
    np.testing.assert_allclose(cells_T, cells_T_expected)
    np.testing.assert_allclose(cells_B, cells_B_expected)
    np.testing.assert_allclose(cell_ids_top, cell_ids_top_expected)
    np.testing.assert_allclose(cell_ids_bottom, cell_ids_bottom_expected)

if __name__ == "__main__":
    test_SN()
    test_WE()
    test_TB()