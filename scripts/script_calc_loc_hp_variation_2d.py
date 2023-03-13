import numpy as np
import os
import sys
import make_general_settings as mgs

if __name__ == "__main__":

    param_dataset_size = int(sys.argv[1])
    dataset_folder = sys.argv[2] # "dummy_dataset" or "dummy_dataset_benchmark"
    filename = sys.argv[3] # "settings" or "settings_2D" or "settings_3D_fine"

    # get boundaries of domain
    settings = mgs.load_settings(os.path.join(dataset_folder,"inputs"), file_name=filename)
    grid_size = settings["grid"]["size"]

    # choose random position inside domain
    locs_x = np.random.uniform(0, grid_size[0], param_dataset_size)
    locs_y = np.random.uniform(0, grid_size[1], param_dataset_size)

    # save to file
    with open(dataset_folder+"/locs_hp.txt", "w") as f:
        f.writelines([f"{x} {y}\n" for x, y in zip(locs_x, locs_y)])