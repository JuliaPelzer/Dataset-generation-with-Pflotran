# run pytest from unittests folder
import os
import subprocess

def test_create_grid():
    os.getcwd()
    try:
        os.mkdir("test_grid")
    except:
        pass
    subprocess.call(
        f"python3 /home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/scripts/create_grid_unstructured.py /home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/unittests/test_grid/",
        shell=True,
    )
    os.system("rm -r test_grid")
    os.system("rm -r __pycache__")


def test_create_grid_different_size():
    os.getcwd()
    try:
        os.mkdir("test_grid_small")
    except:
        pass
    grid_widths = [200, 200, 200]
    number_cells = [2, 3, 6]
    subprocess.call(
        f"python3 /home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/scripts/create_grid_unstructured.py /home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/unittests/test_grid_small/ 3D {grid_widths[0]} {grid_widths[1]} {grid_widths[2]} {number_cells[0]} {number_cells[1]} {number_cells[2]}",
        shell=True,
    )
    subprocess.call(
        "bash ../make_dataset.sh 1 1D 1 vary 3D test_grid_small", shell=True
    )
    # TODO actual ASSERT
    # TODO interaction with bash script
    os.system("rm -r test_grid_small")
    os.system("rm -r __pycache__")