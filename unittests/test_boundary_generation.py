import pathlib
import numpy as np
import os
import filecmp

from scripts.mesh_generation_boundaries import create_boundary_locs
from scripts.main_helpers import groundwater_temp
from scripts.hp_variation_2d import calc_hps_locs_float
from scripts.mesh_generation import mesh_generation_all_dps
from scripts.mesh_refinement import mesh_refinements_all_dps
from scripts.utils import save_yaml

def test_refined_BCs():
    # Fixture
    # settings = {
    #     "grid": {
    #         "resolution": 1,
    #         "size [m]": [4, 3, 2], #100
    #         "loc_hp [m]": [1, 2, 2],
    #         "distance_to_border": [[0, 0], [0, 0], 0],
    #         "min resolution well (m)": 0.1,
    #         "min resolution plume (m)": 1,
    #     },
    #     "subsurface": {
    #         "hydraulic conductivity": 1e-5,
    #         "aquifer thickness": 5,
    #         "darcy velocity": 1,
    #     },
    #     "max pump": {
    #         "temperature": 5,
    #     }
    # }
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

    hps_locs = calc_hps_locs_float(True, num_dp, num_hp, settings)
    hps_temps = np.ones_like(hps_locs[:,:,0])*(5+groundwater_temp())
    hps_rates = np.ones_like(hps_locs[:,:,0])*0.00024
    meshs_refined = mesh_refinements_all_dps(num_dp, settings, meshs, hps_locs, hps_temps, hps_rates, windows, orig_resolution, output_dataset_dir)

    # Expected result
    path_expected = pathlib.Path.cwd() / "unittests"

    # Actual result
    for direction in ["west", "east", "north", "south"]:
        create_boundary_locs(meshs_refined[0], direction, settings["grid"]["resolution"], np.array(settings["grid"]["size [m]"])/settings["grid"]["resolution"], orig_resolution=settings["grid"]["resolution"], output_dir=pathlib.Path.cwd())

    # # Assertion
    # for direction in ["west", "east", "north", "south"]:
    #     assert filecmp.cmp(path_expected / f"{direction}.ex", pathlib.Path.cwd() / f"{direction}.ex"), f"{direction} not equal to reference file in ./unittests"
    

    # # Clean up
    # os.remove(pathlib.Path.cwd() / "west.ex")
    # os.remove(pathlib.Path.cwd() / "east.ex")
    # os.remove(pathlib.Path.cwd() / "north.ex")
    # os.remove(pathlib.Path.cwd() / "south.ex")
    # try:
    #     os.remove(pathlib.Path.cwd() / "top.ex")
    #     os.remove(pathlib.Path.cwd() / "bottom.ex")
    # except:
    #     pass