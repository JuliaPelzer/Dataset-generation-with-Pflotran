import numpy as np
import os
import sys

try:
    import scripts.make_general_settings as mgs
except:
    import make_general_settings as mgs

def calc_loc_hp_variation_2d(param_dataset_size: int, dataset_folder: str, number_of_hps: int, settings, benchmark_bool:bool = False):

    assert number_of_hps > 0, "no clue what happens if number of hps is 0"
    with open("regions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"REGION heatpump_inject{hp}\n  FILE heatpump_inject{hp}.vs\nEND\n\n")
    with open("strata_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"STRATA\n  REGION heatpump_inject{hp}\n  MATERIAL gravel_inj\nEND\n\n")
    with open("conditions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(f"SOURCE_SINK heatpump_inject{hp}\n  FLOW_CONDITION injection\n  REGION heatpump_inject{hp}\nEND\n\n")

    locs_hps = np.ndarray((number_of_hps, param_dataset_size, 2))
    # get boundaries of domain
    grid_size = settings["grid"]["size"]
    cell_size = settings["grid"]["size"]/np.array(settings["grid"]["ncells"])

    if benchmark_bool:
        hps = mgs.load_yaml(dataset_folder, file_name="benchmark_locs_hps")
        for i in range(number_of_hps):
            locs_hps[i] = np.array(hps[i+1])

    else:
        try:
            distance_to_border_in_cells = settings["grid"]["distance_to_border_in_cells"]
        except:
            distance_to_border_in_cells = 5
        distance_to_border = distance_to_border_in_cells*cell_size

        for i in range(number_of_hps):
            # choose random position inside domain
            locs_x = np.random.randint(0+distance_to_border[0], grid_size[0]-distance_to_border[0], param_dataset_size)
            locs_y = np.random.randint(0+distance_to_border[1], grid_size[1]-distance_to_border[1], param_dataset_size)

            # save to file
            with open(os.path.join(dataset_folder, f"locs_hp_x_{i+1}.txt"), "w") as f:
                np.savetxt(f, locs_x)
            with open(os.path.join(dataset_folder, f"locs_hp_y_{i+1}.txt"), "w") as f:
                np.savetxt(f, locs_y)

            locs_hps[i] = np.array([locs_x, locs_y]).T
    locs_hps = np.swapaxes(locs_hps, 0, 1)
    return locs_hps