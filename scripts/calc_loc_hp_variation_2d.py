import numpy as np
import os
import sys

try:
    import scripts.make_general_settings as mgs
except:
    import make_general_settings as mgs

def calc_loc_hp_variation_2d(param_dataset_size: int, dataset_folder: str, number_of_hps: int, settings):

    assert number_of_hps in [1, 2], "number_of_hps must be 1 or 2"
    locs_hps = {}

    # get boundaries of domain
    grid_size = settings["grid"]["size"]
    cell_size = settings["grid"]["size"]/np.array(settings["grid"]["ncells"])

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
        
        locs_hps[i+1] = np.array([locs_x, locs_y]).T
    return locs_hps
    

if __name__ == "__main__":

    param_dataset_size = int(sys.argv[1])
    dataset_folder = sys.argv[2]
    number_of_hps = 1
    if sys.argv[3] != "false":
        number_of_hps = 2

    # get boundaries of domain
    settings = mgs.load_settings(dataset_folder, file_name="settings")
    grid_size = settings["grid"]["size"]
    cell_size = settings["grid"]["size"]/np.array(settings["grid"]["ncells"])

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