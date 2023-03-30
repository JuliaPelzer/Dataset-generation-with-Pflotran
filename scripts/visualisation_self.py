import os
import h5py
import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import logging
import sys
try:
    from scripts.make_general_settings import load_settings
except:
    from make_general_settings import load_settings

def plot_sim(path_run:str, settings, plot_name:str="plot_simulation_results", case:str="side_hp", reshape_bool:bool=True, confined:bool=False):
    # master function: plots the data from the given path in given view, no need for reshaping if structured grid
    with h5py.File(path_run+"/pflotran.h5", "r") as file:
        list_to_plot = _make_plottable_and_2D(file, case, reshape_bool, settings, confined=confined)

    _plot_y(list_to_plot, path_run, name_pic=plot_name, case=case)
    _plot_isolines(list_to_plot, path_run, settings, name_pic=plot_name, case=case,)
    try:
        logging.info(f"Temperature at HP: {np.round(list_to_plot[11]['data'][9,23],4)}")
    except:
        logging.info(f"Temperature at HP: {np.round(list_to_plot[11]['data'][23,9], 4)}")

def _make_plottable_and_2D(hdf5_file, case:str, reshape_bool:bool, settings, confined:bool=False) -> List:
    # helper function to make the data plottable, i.e. put it into a dictionary
    dimensions = settings["grid"]["ncells"]
    if confined:
        dimensions = (dimensions[0], dimensions[1], dimensions[2]+2)
    # if dimensions != (20,150,16) and dimensions[2] != 1:
    #     logging.warning(f"Dimensions are {dimensions}, view is only optimized for dimensions 20x150x16 and size 100mx750mx80m")
    list_to_plot = []
    for time in hdf5_file.keys():
        if not time in ["Coordinates", "Provenance", "   0 Time  0.00000E+00 y", "Time:  0.00000E+00 y"]:
            for property in hdf5_file[time].keys():
                data_dict = {"data" : np.array(hdf5_file[time][property]), "property" : str(property), "time" : str(time)} #+str(time)}
                if reshape_bool:
                    data_dict["data"] = data_dict["data"] = data_dict["data"].reshape(dimensions, order="F")
                if case=="side_hp":
                    data_dict["data"] = data_dict["data"][9,:,:].T
                elif case=="top_hp":
                    data_dict["data"] = data_dict["data"][:,:,9]
                elif case=="2D" and confined:
                    data_dict["data"] = data_dict["data"][:,:,1]
                elif case=="2D" and not confined:
                    data_dict["data"] = data_dict["data"][:,:,0]
                elif case=="3D":
                    data_dict["data"] = data_dict["data"][:,:,2]
                else:
                    raise ValueError("Case not implemented")
                list_to_plot.append(data_dict)
    return list_to_plot

def _plot_y(data, path:str, name_pic:str="plot_y_exemplary", case:str="side_hp"):
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

def _plot_isolines(data, path:str, settings, name_pic:str="plot_isolines_exemplary", case:str="side_hp"):
    # helper function to plot the data
    n_subplots = int(len(data)/4)-1 #7)
    _, axes = plt.subplots(n_subplots,1,sharex=True,figsize=(20,3*(n_subplots)))
    
    index = 0
    levels = np.arange(10.6, 15.6, 0.25)
    grid_size = settings["grid"]["size"]
    for data_point in data:
        if data_point["property"] == "Temperature [C]" and data_point["time"] != "   1 Time  1.00000E-01 y":
            plt.sca(axes[index])
            plt.contourf(data_point["data"], levels=levels, cmap='RdBu_r',  extent=(0, grid_size[1], grid_size[0], 0))
            plt.gca().invert_yaxis()
            plottable_time = float(data_point["time"].split(" ")[-2])
            plt.title(f"{plottable_time} years")
            plt.xlabel("y [m]")
            plt.ylabel("x [m]")
            _aligned_colorbar(label="Temperature [°C]")
            index += 1
    
    pic_file_name = f"{path}/{name_pic}_{case}_isolines"
    logging.info(f"Resulting picture is at {pic_file_name}") 
    plt.suptitle(f"Isolines of Temperature [°C]")
    # plt.savefig(f"{pic_file_name}.svg")
    plt.savefig(f"{pic_file_name}.png")

def _aligned_colorbar(*args,**kwargs):
    # scales and positions the colorbar
    cax = make_axes_locatable(plt.gca()).append_axes("right",size=0.3,pad=0.05)
    plt.colorbar(*args,cax=cax,**kwargs)

def plot_perm(path_settings:str="try_perm", path_run="try_perm/RUN_0", case="top_hp"):
    # plots the permeability field with given view from given path
    dimensions = load_settings(path_settings)["grid"]["ncells"]

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