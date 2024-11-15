import numpy as np

from scripts.mesh_generation import create_regular_cell_centers, create_regular_cell_volumes

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

if __name__=="__main__":
    test_create_regular_cell_centers()
    test_create_regular_cell_volumes()