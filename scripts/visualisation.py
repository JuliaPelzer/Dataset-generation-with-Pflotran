import logging
import os
import sys
from typing import List, Dict

import h5py
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

import scripts.cmap_jp

def plot_results(path_run: str, settings: Dict, plot_name: str = "plot_simulation_results", case: str = "2D", reshape_bool: bool = True):
    # master function: plots the data from the given path in given view, no need for reshaping if structured grid
    with h5py.File(path_run + "/pflotran.h5", "r") as file:
        list_to_plot = make_plottable_and_2D(file, case, reshape_bool, settings)

    plot_data(list_to_plot, path_run, name_pic=plot_name, case=case)


def make_plottable_and_2D(hdf5_file: h5py.File, case: str, reshape_bool: bool, settings: Dict) -> List:
    # helper function to make the data plottable, i.e. put it into a dictionary
    dimensions = np.array(settings["grid"]["size [m]"]) // settings["grid"]["resolution"]
    list_to_plot = []
    for time in hdf5_file.keys():
        if not time in ["   0 Time  0.00000E+00 y"]:
            for property in hdf5_file[time].keys():
                data_dict = {
                    "data": np.array(hdf5_file[time][property]),
                    "property": str(property),
                    "time": str(time),
                }
                if reshape_bool:
                    data_dict["data"] = data_dict["data"].reshape(dimensions)
                if case == "side_hp":
                    data_dict["data"] = data_dict["data"][9, :, :].T
                elif case == "top_hp":
                    data_dict["data"] = data_dict["data"][:, :, 9]
                elif case == "2D":
                    data_dict["data"] = data_dict["data"][:, :, 0]
                elif case == "3D":
                    data_dict["data"] = data_dict["data"][:, :, 2]
                else:
                    raise ValueError("Case not implemented")
                list_to_plot.append(data_dict)
    return list_to_plot


def plot_data(data: List, path: str, name_pic: str = "plot_y_exemplary", case: str = "side_hp"):
    # helper function to plot the data
    n_subplots = len(data)
    _, axes = plt.subplots(n_subplots, 1, sharex=True, figsize=(20, 3 * (n_subplots)))

    for index, data_point in enumerate(data):
        plt.sca(axes[index])
        plt.imshow(data_point["data"], origin="lower", cmap="jp")
        plt.xlabel("y")
        plt.ylabel("x")
        _aligned_colorbar(label=data_point["property"])

    pic_file_name = f"{path}/{name_pic}_{case}.png"
    logging.info(f"Resulting picture is at {pic_file_name}")
    plt.savefig(pic_file_name, dpi=400)


def _aligned_colorbar(*args, **kwargs):
    # scales and positions the colorbar
    cax = make_axes_locatable(plt.gca()).append_axes("right", size=0.3, pad=0.05)
    plt.colorbar(*args, cax=cax, **kwargs)

