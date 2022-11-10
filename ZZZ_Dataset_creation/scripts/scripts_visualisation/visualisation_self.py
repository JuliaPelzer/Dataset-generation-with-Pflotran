import os
import h5py
import numpy as np
from typing import Dict
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import logging
import sys

def plot_sim(path:str="try/RUN_0", plot_name:str="plot_simulation_results", case="side_hp", reshape=True):
    # master function: plots the data from the given path in given view, no need for reshaping if structured grid
    with h5py.File(path+"/pflotran.h5", "r") as file:
        list_to_plot = _make_plottable_and_2D(file, case, reshape)

    _plot_y(list_to_plot, path, name_pic=plot_name)
    try:
        logging.info(f"Temperature at HP: {np.round(list_to_plot[11]['data'][9,23],4)}")
    except:
        logging.info(f"Temperature at HP: {np.round(list_to_plot[11]['data'][23,9], 4)}")

def _make_plottable_and_2D(hdf5_file, case, reshape):
    # helper function to make the data plottable, i.e. put it into a dictionary
    list_to_plot = []
    for time in hdf5_file.keys():
        if not time in ["   0 Time  0.00000E+00 y", "Coordinates", "Provenance", "Time:  0.00000E+00 y"]:
            for property in hdf5_file[time].keys():
                data_dict = {"data" : np.array(hdf5_file[time][property]), "property" : str(property)} #+str(time)}
                if reshape:
                    data_dict["data"] = data_dict["data"] = data_dict["data"].reshape(20,150,16, order="F")
                if case=="side_hp":
                    data_dict["data"] = data_dict["data"][9,:,:].T
                elif case=="top_hp":
                    data_dict["data"] = data_dict["data"][:,:,9]
                else:
                    raise ValueError("Case not implemented")
                list_to_plot.append(data_dict)
    return list_to_plot

def _plot_y(data, path, name_pic="plot_y_exemplary"):
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
    
    pic_file_name = f"{path}/{name_pic}.jpg"
    logging.info(f"Resulting picture is at {pic_file_name}")  
    plt.savefig(pic_file_name)

def _aligned_colorbar(*args,**kwargs):
    # scales and positions the colorbar
    cax = make_axes_locatable(plt.gca()).append_axes("right",size=0.3,pad=0.05)
    plt.colorbar(*args,cax=cax,**kwargs)

def plot_perm(path="try_perm/RUN_0", case="top_hp"):
    # plots the permeability field with given view from given path
    for file in os.listdir(path):
        if file.startswith("permeability"):
            with h5py.File(path+"/"+file, "r") as f:
                data = np.array(f["Permeability"])
                data = data.reshape(20,150,16, order="F")
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

if __name__ == "__main__":

    cla = sys.argv
    if len(cla) > 1:
        path = cla[1]
        if len(cla) > 2:
            case = cla[2]
        else:
            case = "side_hp"
    else:
        path = "./RUN_1"
        case = "side_hp"

    plot_sim(path=path, case=case)
    # plot_perm(path="try_perm2/permeability_fields/", case="side_hp")