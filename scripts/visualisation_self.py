import os
import h5py
import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import logging
import sys
import yaml

def plot_sim(path_settings:str="try", path_run:str="try/RUN_0", plot_name:str="plot_simulation_results", case:str="side_hp", reshape_bool:bool=True):
    # master function: plots the data from the given path in given view, no need for reshaping if structured grid
    with h5py.File(path_run+"/pflotran.h5", "r") as file:
        list_to_plot = _make_plottable_and_2D(file, case, reshape_bool, path_settings)

    _plot_y(list_to_plot, path_run, name_pic=plot_name)
    try:
        logging.info(f"Temperature at HP: {np.round(list_to_plot[11]['data'][9,23],4)}")
    except:
        logging.info(f"Temperature at HP: {np.round(list_to_plot[11]['data'][23,9], 4)}")

def _make_plottable_and_2D(hdf5_file, case:str, reshape_bool:bool, path_settings:str) -> List:
    # helper function to make the data plottable, i.e. put it into a dictionary
    dimensions = _get_dimensions(path_settings)
    if dimensions != (20,150,16) and dimensions[2] != 1:
        logging.warning(f"Dimensions are {dimensions}, view is only optimized for dimensions 20x150x16 and size 100mx750mx80m")
    list_to_plot = []
    for time in hdf5_file.keys():
        if not time in ["Coordinates", "Provenance", "   0 Time  0.00000E+00 y", "Time:  0.00000E+00 y"]:
            for property in hdf5_file[time].keys():
                data_dict = {"data" : np.array(hdf5_file[time][property]), "property" : str(property)} #+str(time)}
                if reshape_bool:
                    data_dict["data"] = data_dict["data"] = data_dict["data"].reshape(dimensions, order="F")
                if case=="side_hp":
                    data_dict["data"] = data_dict["data"][9,:,:].T
                elif case=="top_hp":
                    data_dict["data"] = data_dict["data"][:,:,9]
                elif case=="2D":
                    data_dict["data"] = data_dict["data"][:,:]
                else:
                    raise ValueError("Case not implemented")
                list_to_plot.append(data_dict)
    return list_to_plot

def _plot_y(data, path:str, name_pic:str="plot_y_exemplary"):
    # helper function to plot the data
    n_subplots = len(data)
    _, axes = plt.subplots(n_subplots,1,sharex=True,figsize=(20,3*(n_subplots)))
    
    for index, data_point in enumerate(data):
        plt.sca(axes[index])
        plt.imshow(data_point["data"])
        plt.gca().invert_yaxis()

        plt.xlabel("y")
        plt.ylabel("x or z")
        _aligned_colorbar(label=data_point["property"])
    
    pic_file_name = f"{path}/{name_pic}_{case}.png"
    logging.info(f"Resulting picture is at {pic_file_name}")  
    plt.savefig(pic_file_name)

def _aligned_colorbar(*args,**kwargs):
    # scales and positions the colorbar
    cax = make_axes_locatable(plt.gca()).append_axes("right",size=0.3,pad=0.05)
    plt.colorbar(*args,cax=cax,**kwargs)

def plot_perm(path_settings:str="try_perm", path_run="try_perm/RUN_0", case="top_hp"):
    # plots the permeability field with given view from given path
    dimensions = _get_dimensions(path_settings)

    for file in os.listdir(path_run):
        if file.startswith("permeability"):
            with h5py.File(path_run+"/"+file, "r") as f:
                data = np.array(f["Permeability"])
                data = data.reshape(dimensions, order="F")
                if case=="side_hp":
                    data = data[9,:,:].T
                elif case=="top_hp":
                    data = data[:,:,9]
                else:
                    raise ValueError("Case not implemented")
                plt.imshow(data)
                plt.gca().invert_yaxis()
                plt.colorbar()
                plt.show()
                # break

def _get_dimensions(path:str) -> Tuple[int, int, int]:
    # read json file for dimensions
    with open(f"{path}/inputs/settings.yaml", "r") as f:
        perm_settings = yaml.safe_load(f)
    dimensions_of_datapoint = perm_settings["grid"]["ncells"]
    return dimensions_of_datapoint

if __name__ == "__main__":

    path_settings = "."
    path_run = "./RUN_0"
    case = "side_hp"

    cla = sys.argv
    if len(cla) > 1:
        path_settings = cla[1]
        if len(cla) > 2:
            path_run = cla[2]
            if len(cla) > 3:
                case = cla[3]

    plot_sim(path_settings=path_settings, path_run=path_run, case=case)
    # plot_perm(path="try_perm2/permeability_fields/", case="side_hp")