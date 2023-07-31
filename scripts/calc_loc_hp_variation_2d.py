import numpy as np
import os
import sys

try:
    import scripts.make_general_settings as mgs
except:
    import make_general_settings as mgs


def write_hp_additional_files(
    dataset_folder_interim: str, number_of_hps: int, num_hps_to_vary: int = 0
):
    assert number_of_hps > 0, "no clue what happens if number of hps is 0"
    assert (
        num_hps_to_vary <= number_of_hps
    ), "number of hps to vary must be smaller than number of hps"

    # write input lines for pflotran for number of hps
    with open(f"{dataset_folder_interim}/regions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(
                f"REGION heatpump_inject{hp}\n  FILE heatpump_inject{hp}.vs\nEND\n\n"
            )
    with open(f"{dataset_folder_interim}/strata_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(
                f"STRATA\n  REGION heatpump_inject{hp}\n  MATERIAL gravel_inj\nEND\n\n"
            )
    with open(f"{dataset_folder_interim}/conditions_hps.txt", "w") as f:
        for hp in range(number_of_hps):
            f.write(
                f"SOURCE_SINK heatpump_inject{hp}\n  FLOW_CONDITION injection\n  REGION heatpump_inject{hp}\nEND\n\n"
            )


def calc_loc_hp_variation_2d(
    param_dataset_size: int,
    dataset_folder_inputs: str,
    number_of_hps: int,
    settings,
    benchmark_bool: bool = False,
    num_hps_to_vary: int = 0,
):
    locs_hps = np.ndarray((number_of_hps, param_dataset_size, 2))
    # get boundaries of domain
    grid_size = settings["grid"]["size"]

    if benchmark_bool or (number_of_hps - num_hps_to_vary > 0):
        hps = mgs.load_yaml(dataset_folder_inputs, file_name="benchmark_locs_hps")
        for i in range(number_of_hps - num_hps_to_vary):
            locs_hps[i] = np.array(hps[i + 1])

            # if not benchmark_bool:
            # save to file
            with open(
                os.path.join(dataset_folder_inputs, f"locs_hp_{i+1}_fixed.txt"), "w"
            ) as f:
                np.savetxt(f, locs_hps[i])

    if not benchmark_bool:
        try:
            distance_to_border = settings["grid"]["distance_to_border"]
        except:
            distance_to_border = 5
        print(
            f"distance to border: {distance_to_border} m, {len(distance_to_border[1])} values"
        )

        for i in range(number_of_hps - num_hps_to_vary, number_of_hps):
            # choose random position inside domain
            try:
                locs_x = np.random.randint(
                    0 + distance_to_border[0][0],
                    grid_size[0] - distance_to_border[0][1],
                    param_dataset_size,
                )
            except:
                locs_x = np.random.randint(
                    0 + distance_to_border[0][0],
                    grid_size[0] - distance_to_border[0][0],
                    param_dataset_size,
                )

            if len(distance_to_border[1]) == 1:
                locs_y = np.random.randint(
                    0 + distance_to_border[1],
                    grid_size[1] - distance_to_border[1],
                    param_dataset_size,
                )
            elif len(distance_to_border[1]) == 2:
                locs_y = np.random.randint(
                    distance_to_border[1][0],
                    grid_size[1] - distance_to_border[1][1],
                    param_dataset_size,
                )
            else:
                print(
                    "distance to border in y direction must be either one value or two values"
                )
                sys.exit()

            # save to file
            with open(
                os.path.join(dataset_folder_inputs, f"locs_hp_x_{i+1}.txt"), "w"
            ) as f:
                np.savetxt(f, locs_x)
            with open(
                os.path.join(dataset_folder_inputs, f"locs_hp_y_{i+1}.txt"), "w"
            ) as f:
                np.savetxt(f, locs_y)

            locs_hps[i] = np.array([locs_x, locs_y]).T
    locs_hps = np.swapaxes(locs_hps, 0, 1)
    return locs_hps
