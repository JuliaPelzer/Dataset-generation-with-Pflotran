from random import random, seed, sample
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from h5py import *
from scipy.interpolate import RegularGridInterpolator
import noise
from typing import Dict
from tqdm import tqdm
import logging
from scripts.make_general_settings import load_settings
from scripts.visualisation_self import _aligned_colorbar

def make_perm_grid(settings:Dict, base:float = 0, perm_min_max:np.array = None):
    length_cells = settings["grid"]["size"] / np.array(settings["grid"]["ncells"])
    icells = [np.linspace(1, settings["grid"]["ncells"][i], settings["grid"]["ncells"][i]) for i in (0,1,2)]
    idx, idy, idz = np.meshgrid(icells[0], icells[1], icells[2], indexing="ij")
    if perm_min_max is None:
        perm_min = settings["permeability"]["perm_min"]
        perm_max = settings["permeability"]["perm_max"]
    else:
        perm_min = np.min(perm_min_max)
        perm_max = np.max(perm_min_max)

    if settings["permeability"]["case"]=="trigonometric":
        # function exemplary
        def fct_sin(value):
            return (perm_max - perm_min)/2 * np.sin(value/settings["permeability"]["factor"]) + (perm_max + perm_min)/2
        def fct_cos(value):
            return (perm_max - perm_min)/2 * np.cos(value/settings["permeability"]["factor"]) + (perm_max + perm_min)/2
        values = (fct_cos(idx*length_cells[1])+fct_cos(idy*length_cells[0])+fct_cos(idz*length_cells[2]))/3  # ORDER X,Y,Z
    # TODO Überarbeiten mit neuer Settingsstruktur und testen
    # elif settings["permeability"]["case"]=="rand_interpolate":
    #     # Interpolation with RegularGridInterpolator from scipy (can do 3D, works on a regular grid)
    #     nbases = 5
    #     length_cells_base = settings.size / nbases
    #     icells_base = [np.linspace(1, settings.ncells[i], nbases) for i in (0,1,2)]
    #     idx_base, idy_base, idz_base = np.meshgrid(icells_base[0], icells_base[1], icells_base[2], indexing="ij") # ORDER X,Y,Z

    #     def fct_rand(shape=[nbases,nbases,nbases]):
    #         return np.random.uniform(settings.perm_min, settings.perm_max, size=shape)
    #     values_base = fct_rand()

    #     test_points = np.array([idx.ravel(), idy.ravel(), idz.ravel()]).T
    #     interpolator = RegularGridInterpolator(icells_base, values_base)
    #     method = "linear" # in ['linear', 'nearest', 'slinear', 'cubic', 'quintic']:
    #     values = interpolator(test_points, method=method).reshape(settings.ncells[0], settings.ncells[1], settings.ncells[2]).T
    elif settings["permeability"]["case"]=="perlin_noise":
        if settings["general"]["dimensions"]==2:
            def perlin_noise(x,y):
                return noise.pnoise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=base)
            values = np.zeros((settings["grid"]["ncells"][0], settings["grid"]["ncells"][1]))
            for i in range(0, settings["grid"]["ncells"][0]):
                for j in range(0, settings["grid"]["ncells"][1]):
                    freq = settings["permeability"]["frequency"] / np.array(settings["grid"]["ncells"])[0:2]
                    x,y = [i, j] * freq
                    values[i,j] = (perlin_noise(x,y)+1)/2 * (perm_max - perm_min) + perm_min
        else: #3D case
            def perlin_noise(x,y,z):
                return noise.pnoise3(x, y, z, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, repeatz=1024, base=base)
            values = np.zeros((settings["grid"]["ncells"][0], settings["grid"]["ncells"][1], settings["grid"]["ncells"][2]))
            for i in range(0, settings["grid"]["ncells"][0]):
                for j in range(0, settings["grid"]["ncells"][1]):
                    for k in range(0, settings["grid"]["ncells"][2]):
                        freq = settings["permeability"]["frequency"] / np.array(settings["grid"]["ncells"])
                        x,y,z = [i, j, k] * freq
                        values[i,j,k] = (perlin_noise(x,y,z)+1)/2 * (perm_max - perm_min) + perm_min
    
    return values, icells

def make_perm_grid_Manuel(settings:Dict, offset, base:float = 0):
    icells = [np.linspace(1, settings["grid"]["ncells"][i], settings["grid"]["ncells"][i]) for i in (0,1,2)]
    if settings["permeability"]["case"]=="perlin_noise":
        
        grid_dimensions = settings["grid"]["ncells"]
        simulation_area = settings["grid"]["size"]
        frequency = settings["permeability"]["frequency"]
        perm_max = settings["permeability"]["perm_max"]
        perm_min = settings["permeability"]["perm_min"]

        values = awesome_new_perlin_noise(grid_dimensions, simulation_area, frequency, perm_min, perm_max, offset)
    
    return values, icells

def awesome_new_perlin_noise(grid_dimensions, simulation_area, frequency, min_value, max_value, offset):

    # Scale the simulation area down into a unit cube
    simulation_area_max = max(simulation_area)
    scale_x = 100.0  / simulation_area_max; 
    scale_y = 1280.0 / simulation_area_max; 
    scale_z = 80.0   / simulation_area_max; 

    # Alternatively set scale factor to 1 for all dimensions.
    # This squishes the noise in tow dimensions. Was the old behaviour
    #scale_x = 1
    #scale_y = 1
    #scale_z = 1

    values = np.zeros((grid_dimensions[0], grid_dimensions[1], grid_dimensions[2]))

    for i in range(0, grid_dimensions[0]):
        for j in range(0, grid_dimensions[1]):
            for k in range(0, grid_dimensions[2]):

                x = i / grid_dimensions[0] * scale_x + offset[0]
                y = j / grid_dimensions[1] * scale_y + offset[1]

                x = x * frequency[0]
                y = y * frequency[1]

                if settings["general"]["dimensions"]==2:
                    noise_value  = (noise.pnoise2(x,y) + 1.0) / 2.0
                    values[i,j] = min_value + noise_value * (max_value - min_value)
                else:
                    z = k / grid_dimensions[2] * scale_y + offset[2]
                    z = z * frequency[2]
                    
                    # pnoise3 returns values in the range of [-1,1]. We want [0, 1].
                    noise_value  = (noise.pnoise3(x,y,z) + 1.0) / 2.0
                    # scale from [0,1] to our perm range
                    values[i,j,k] = min_value + noise_value * (max_value - min_value)

    return values

def save_perm(filename, ncells, cells, dimensionality:str="3D"):
    if dimensionality == "2D":
        n = ncells[0] * ncells[1]
    else:
        n = ncells[0] * ncells[1] * ncells[2]
    # create integer array for cell ids
    iarray = np.arange(n,dtype='u8')
    iarray[:] += 1 # convert to 1-based
    cells_array_flatten = cells.reshape(n, order='F')

    h5file = _edit_perm_file(filename,mode='w')

    dataset_name = 'Cell Ids'
    h5file.create_dataset(dataset_name, data=iarray)
    dataset_name = 'Permeability'
    h5file.create_dataset(dataset_name, data=cells_array_flatten)

    h5file.close()

# 2d plot of a permeability field
def plot_perm(cells, filename, case="trigonometric", **imshowargs):
    dimensionality = "2D"
    if dimensionality == "3D":
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        fig.suptitle(f"Permeability field [{case}]")
        axes = axes.ravel()
        axes[0].imshow(cells[:,:,0])
        axes[2].imshow(cells[:,0,:])
        axes[3].imshow(cells[0,:,:])
        axes[0].set_title("yz")
        axes[2].set_title("xz")
        axes[3].set_title("xy")
        for i in range(0,4):
            axes[i].axis("off")
        fig.tight_layout()
    else:
        fig, axis = plt.subplots(1, 1, figsize=(10, 6))
        fig.suptitle(f"Permeability field [{case}]")
        plt.imshow(cells, **imshowargs)
        plt.ylabel("x ")
        plt.xlabel("y")
        # fig.tight_layout()
        _aligned_colorbar()
        # fig.show()
    fig.savefig(f"{filename}.png")
    plt.close(fig)
    
def create_perm_fields(number_samples:int, folder:str, settings:Dict, plot_bool:bool=False, perms_min_max:np.ndarray=None, filename_extension:str=""):
    # TODO vary frequency
    # TODO vary offset?
    
    if not os.path.exists(folder):
        os.mkdir(folder)
    if not os.path.exists(f"{folder}/permeability_fields"):
        os.mkdir(f"{folder}/permeability_fields")

    if not settings["general"]["random_bool"]:
        np.random.seed(settings["general"]["seed_id"])

    # vary bases to get different fields
    try:
        bases = sample(range(0, 255), number_samples)
    except ValueError:
        print('Number of desired perm-field variations exceeds 255.')
    
    bases = tqdm(bases)
    for idx, base in enumerate(bases):
        cells, _ = make_perm_grid(settings, base, perms_min_max[idx])
        size = np.array(settings["grid"]["ncells"])
        filename = f"{folder}/permeability_fields/permeability_base_{base}{filename_extension}.h5"

        save_perm(filename, size, cells, settings["general"]["dimensions"])
        if plot_bool:
            plot_perm(cells, filename[:-3], case=settings["permeability"]["case"]) #, vmax=settings["permeability"]["perm_max"], vmin=settings["permeability"]["perm_min"])

    logging.info(f"Created {len(bases)} perm-field(s)")
    return cells # for pytest

def create_perm_field_Manuel(number_samples:int, folder:str, settings:Dict, plot_bool:bool=False, filename_extension:str=""):
    # TODO vary frequency
    
    if not os.path.exists(folder):
        os.mkdir(folder)
    if not os.path.exists(f"{folder}/permeability_fields"):
        os.mkdir(f"{folder}/permeability_fields")
    if not os.path.exists(f"{folder}/inputs"):
        os.mkdir(f"{folder}/inputs")

    if not settings["general"]["random_bool"]:
        np.random.seed(settings["general"]["seed_id"])

    # We sample the permeability from 3 dimensional perlin noise that extends indefinetly.
    # To introduce randomness the starting point of our sampling is drawn from a uniform
    # distribution. From there we are moving a multiple of our simulation area for every
    # sample to get non-overlapping fields. The simulation area is scaled to a unit cube so
    # conveniently we can move by 1 in x directon (in this direction the scaled area 
    # will be << 1)

    base_offset = np.random.rand(3) * 4242
    bases = range(number_samples)

    for base in tqdm(bases):
        cells, _ = make_perm_grid_Manuel(settings, offset=base_offset + [base,0,0])
        filename = f"{folder}/permeability_fields/permeability_base_{base}{filename_extension}.h5"
        save_perm(filename, settings["grid"]["ncells"], cells, settings["general"]["dimensions"])
        if plot_bool:
            plot_perm(cells, folder, case=settings["permeability"]["case"])
    
    logging.info("Created perm-field(s)")
    return cells # for pytest
    
def read_and_plot_perm_field(settings:Dict, filename:str):
    # read h5 perm file
    h5file = _edit_perm_file(filename,mode='r')

    # print header from h5 file
    if False:
        logging.info(h5file.keys())
        logging.info(h5file['Cell Ids'])
        logging.info(h5file['Cell Ids'][:])
        logging.info(h5file['Permeability'])
        logging.info(h5file['Permeability'][:])

    perm_field_orig = h5file['Permeability'][:]
    perm_field = perm_field_orig.reshape(settings["grid"]["ncells"], order="F")
    plot_perm(perm_field, filename[-10:-3], case=settings["permeability"]["case"])

    h5file.close()
    return perm_field # for pytest

def _edit_perm_file(filename:str, mode:str="r"):
    return File(filename, mode=mode)

def _random_exclude():
    """Returns a random number that is not in the excluded range."""
    exclude_min = 140000
    exclude_max = 260000

    while True:
        base = np.random.randint(1, 2**19)
        if base < exclude_min or base > exclude_max:
            return base

if __name__=="__main__":

    if True:
        # read input parameters
        cla_args = sys.argv
        logging.basicConfig(level=cla_args[1])
        number_samples = int(cla_args[2])
        folder_settings = "."

        output_folder = "."
        if len(cla_args) > 3:
            output_folder = cla_args[3]

        settings = load_settings(folder_settings)
        # get min and max perm value
        try:
            perms_min_max = np.loadtxt(f"{output_folder}/permeability_values.txt")
        except:
            print("No permeability_values.txt file found. Using default ones from settings.")


        plot_bool = False # if plot_bool then runs crash because try to load a png file as perm.h5 file
        # create_perm_field_Manuel(number_samples, folder, settings, plot_bool)
        create_perm_fields(number_samples, output_folder, settings, plot_bool, perms_min_max)

    else:    
        # just testing perm field creation
        output_folder = "/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/"
        output_folder += "try_perm"
        folder_settings = output_folder + "/inputs"
        settings = load_settings(folder_settings)
        for file in os.listdir(f"{output_folder}/permeability_fields"):
            if file.endswith(".h5"):
                read_and_plot_perm_field(settings, filename=f"{output_folder}/permeability_fields/{file}")
