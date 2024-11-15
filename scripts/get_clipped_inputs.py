import pathlib
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import yaml
from typing import Dict, List

# load geoTIFF files
def load_geotiff(file_path):
    with rasterio.open(file_path) as src:
        img = src.read()
        img = img.squeeze()
    return np.array(img)

# plot 
def plot_img(img, title, resolution, start = [0,0]):
    plt.imshow(img, cmap='hot', extent=[start[1]*resolution/1000, start[1]*resolution/1000+img.shape[1]*resolution/1000, start[0]*resolution/1000+img.shape[0]*resolution/1000, start[0]*resolution/1000])
    plt.colorbar()
    plt.title(title)
    plt.ylabel("y [km]")
    plt.xlabel("x [km]")
    plt.show()

def overlay_tif(start, window_shape, data, none_value=None):
    # TODO wie kommunizier ich den startpunkt? ko-vergleich von der 1.pos mit wert > 0?!
    end = start[0] + window_shape[0], start[1] + window_shape[1]
    data_windowed = data[start[0]:end[0], start[1]:end[1]]

    if none_value is not None:
        if (data_windowed == none_value).any():
            raise ValueError("Window outside of domain")

    return data_windowed

def load_params(inputs_path:pathlib.Path, dest_path:pathlib.Path):
    resolution = yaml.safe_load(open(inputs_path / "resolution.yaml"))
    params = yaml.safe_load(open(dest_path / "settings.yaml"))
    window_shape = params["window shape [m]"] #(256*20,16*20) # meters
    number_of_simulations = params["number of simulations"] #10000

    window_shape_cells = int(window_shape[0]/resolution), int(window_shape[1]/resolution)

    # start_point = (40000, 40000) #in meters
    # start_cells = int(start_point[0]/resolution), int(start_point[1]/resolution)

    return params, resolution, window_shape, window_shape_cells, number_of_simulations

def prepare_data_ids(data, randomize: Dict):
    ids = [(i,j) for i in range(data.shape[0]) for j in range(data.shape[1])]
    if randomize["random_bool"]:
        print("Randomizing input windows")
        np.random.seed(randomize["seed_id"])
        np.random.shuffle(ids)
    else:
        print("Not randomizing input windows")

    return ids

def get_all_clipped_inputs(inputs_path:pathlib.Path, number_of_simulations:int, window_shape_cells:List[int], randomize:Dict):

    # load data
    cond = load_geotiff(inputs_path / "Hydraulic_conductivity_20m_resolution.tif")
    drawdown = load_geotiff(inputs_path / "Drawdown_20m_resolution.tif")
    # plot_img(cond, "Hydraulic conductivity", resolution=20)

    # prepare data
    dummy_values = {"cond": -0.005, "drawdown": -100}
    cond[cond < 0] = dummy_values["cond"]
    drawdown[drawdown < 0] = dummy_values["drawdown"]

    ids_cells = prepare_data_ids(cond, randomize)

    # random start-point version
    start_positions = []
    windows_cond = []
    windows_drawdown = []

    for i, position_cells in enumerate(ids_cells):
        cond_windowed = overlay_tif(position_cells, window_shape_cells, cond)
        if dummy_values["cond"] not in cond_windowed:
            windows_cond.append(cond_windowed)
            start_positions.append(position_cells)
            windows_drawdown.append(overlay_tif(position_cells, window_shape_cells, drawdown, none_value=dummy_values["drawdown"]))

            if len(windows_cond) == number_of_simulations:
                break

    print("Number of windows found:", len(windows_cond), "within", i, "tries")
    if len(windows_cond) < number_of_simulations:
        print("Not enough windows found. Only", len(windows_cond), "found.")
    
    # ATTENTION currently resolution-dependent: entries=cell-wise, not meter-wise
    return np.array(start_positions), np.array(windows_cond), np.array(windows_drawdown)

if __name__ == "__main__":
    # load params
    inputs_path = pathlib.Path("input_files/real_Munich_input_fields/epsg_25832/")
    dest_path = pathlib.Path("outputs/test_dataset")
    params, resolution, window_shape, window_shape_cells, number_of_simulations = load_params(inputs_path, dest_path)
    print(params)

    start_positions, windows_cond, windows_drawdown = get_all_clipped_inputs(inputs_path, number_of_simulations, window_shape_cells, randomize=params["random"])

    for position_cells, cond_windowed in zip(start_positions, windows_cond):
        plot_img(cond_windowed, "Hydraulic conductivity", resolution, start=position_cells)
        break