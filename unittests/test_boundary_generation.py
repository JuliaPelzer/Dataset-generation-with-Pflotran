import numpy as np
import pathlib
import os
import filecmp

from scripts.mesh_generation import create_regular_grid
from scripts.mesh_generation_boundaries import create_boundary_locs
from scripts.mesh_refinement import mesh_refinements_all_dps

def test_refined_BCs():
    # Fixture
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
    num_dp = 1
    dps_hps_locs_global = np.array([[[ 4.68187768,  0.83783127,  1.        ],
        [35.97385269,  4.77132156,  1.        ],
        [ 1.44393715, 13.66984525,  1.        ],
        [18.02092972, 16.91220293,  1.        ]]])
    windows = [{"properties": {"hydraulic_conductivity": np.ones(settings["grid"]["size [m]"][:2])*settings["subsurface"]["hydraulic conductivity"], "thickness": np.ones(settings["grid"]["size [m]"][:2])*settings["subsurface"]["aquifer thickness"], "darcy_velocity": np.ones(settings["grid"]["size [m]"][:2])*settings["subsurface"]["darcy velocity"]}}]
    
    out, _  = create_regular_grid(settings)
    out = [out,]
    meshs_refined = mesh_refinements_all_dps(num_dp, settings, meshs_regular=out, dps_hps_locs=dps_hps_locs_global, dps_hps_temps=np.ones_like(dps_hps_locs_global[:,:,0])*5, windows_properties_collected=windows, orig_resolution=20)

    # Expected result
    path_expected = pathlib.Path.cwd() / "unittests"

    # Actual result
    for direction in ["west", "east", "north", "south"]:
        create_boundary_locs(meshs_refined[0], direction, settings["grid"]["resolution"], np.array(settings["grid"]["size [m]"])/settings["grid"]["resolution"], orig_resolution=settings["grid"]["resolution"], output_dir=pathlib.Path.cwd())

    # Assertion
    for direction in ["west", "east", "north", "south"]:
        assert filecmp.cmp(path_expected / f"{direction}.ex", pathlib.Path.cwd() / f"{direction}.ex"), f"{direction} not equal to reference file in ./unittests"
    

    # Clean up
    os.remove(pathlib.Path.cwd() / "west.ex")
    os.remove(pathlib.Path.cwd() / "east.ex")
    os.remove(pathlib.Path.cwd() / "north.ex")
    os.remove(pathlib.Path.cwd() / "south.ex")
    try:
        os.remove(pathlib.Path.cwd() / "top.ex")
        os.remove(pathlib.Path.cwd() / "bottom.ex")
    except:
        pass