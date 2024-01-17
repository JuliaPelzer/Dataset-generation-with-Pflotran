import logging
import os
import sys
from random import random, sample, seed
from typing import Dict

import matplotlib.pyplot as plt
import noise
import numpy as np
from h5py import *
from scipy.interpolate import RegularGridInterpolator
from tqdm import tqdm

from scripts.make_general_settings import load_yaml
from scripts.visualisation import _aligned_colorbar


def make_grid(
    settings: Dict,
    perm_min: float,
    perm_max: float,
    base: float = 0,
    offset: float = None,
    freq: float = None,
    vary_property: str = "permeability",
):
    grid_dimensions = settings["grid"]["ncells"]  # [-]
    domain_size = settings["grid"]["size"]  # [m]

    if settings[vary_property]["case"] == "trigonometric":
        # function exemplary
        def fct_cos(value):
            return (perm_max - perm_min) / 2 * np.cos(
                value / settings[vary_property]["factor"]
            ) + (perm_max + perm_min) / 2

        icells = [
            np.linspace(1, grid_dimensions[i], grid_dimensions[i]) for i in (0, 1, 2)
        ]
        idx, idy, idz = np.meshgrid(icells[0], icells[1], icells[2], indexing="ij")
        length_cells = domain_size / grid_dimensions
        values = (
            fct_cos(idx * length_cells[1])
            + fct_cos(idy * length_cells[0])
            + fct_cos(idz * length_cells[2])
        ) / 3  # ORDER X,Y,Z
    elif settings[vary_property]["case"] == "rand_interpolate":
        print("rand_interpolate currently not implemented")
        """ TODO Überarbeiten mit neuer Settingsstruktur und testen
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
        """
    elif settings[vary_property]["case"] == "perlin_noise":
        if settings["general"]["dimensions"] == 2:

            def perlin_noise(x, y):
                return noise.pnoise2(
                    x,
                    y,
                    octaves=1,
                    persistence=0.5,
                    lacunarity=2.0,
                    repeatx=1024,
                    repeaty=1024,
                    base=base,
                )

            values = np.zeros((grid_dimensions[0], grid_dimensions[1]))
            for i in range(0, grid_dimensions[0]):
                for j in range(0, grid_dimensions[1]):
                    freq = np.array(freq) / domain_size[0:2]
                    x, y = [i, j] * freq
                    values[i, j] = (perlin_noise(x, y) + 1) / 2 * (
                        perm_max - perm_min
                    ) + perm_min
        else:  # 3D case

            def perlin_noise(x, y, z):
                return noise.pnoise3(
                    x,
                    y,
                    z,
                    octaves=1,
                    persistence=0.5,
                    lacunarity=2.0,
                    repeatx=1024,
                    repeaty=1024,
                    repeatz=1024,
                    base=base,
                )

            values = np.zeros(
                (grid_dimensions[0], grid_dimensions[1], grid_dimensions[2])
            )
            for i in range(0, grid_dimensions[0]):
                for j in range(0, grid_dimensions[1]):
                    for k in range(0, grid_dimensions[2]):
                        freq = np.array(freq) / domain_size
                        x, y, z = [i, j, k] * freq
                        values[i, j, k] = (perlin_noise(x, y, z) + 1) / 2 * (
                            perm_max - perm_min
                        ) + perm_min
    elif settings[vary_property]["case"] == "perlin_v2":
        # adapted by Manuel Hirche

        # We sample the permeability from 3 dimensional perlin noise that extends indefinetly.
        # To introduce randomness the starting point of our sampling is drawn from a uniform
        # distribution. From there we are moving a multiple of our simulation area for every
        # sample to get non-overlapping fields. The simulation area is scaled to a unit cube so
        # conveniently we can move by 1 in x directon (in this direction the scaled area
        # will be << 1)

        # Scale the simulation area down into a unit cube
        simulation_area_max = max(domain_size)
        scale_x = domain_size[0] / simulation_area_max
        scale_y = domain_size[1] / simulation_area_max
        scale_z = domain_size[2] / simulation_area_max

        values = np.zeros((grid_dimensions[0], grid_dimensions[1], grid_dimensions[2]))
        for i in range(0, grid_dimensions[0]):
            for j in range(0, grid_dimensions[1]):
                for k in range(0, grid_dimensions[2]):
                    x = i / grid_dimensions[0] * scale_x + offset[0]
                    y = j / grid_dimensions[1] * scale_y + offset[1]

                    x = x * freq[0]
                    y = y * freq[1]

                    if settings["general"]["dimensions"] == 2:
                        noise_value = (noise.pnoise2(x, y) + 1.0) / 2.0
                        values[i, j] = perm_min + noise_value * (perm_max - perm_min)
                    else:
                        z = k / grid_dimensions[2] * scale_z + offset[2]
                        z = z * freq[2]
                        # pnoise3 returns values in the range of [-1,1] -> move to [0, 1]
                        noise_value = (noise.pnoise3(x, y, z) + 1.0) / 2.0
                        values[i, j, k] = perm_min + noise_value * (
                            perm_max - perm_min
                        )  # scale to perm range

    return values


def save_vary_field(filename, ncells, cells, dimensionality: str = "3D", vary_property:str = "permeability"):
    if dimensionality == "2D":
        n = ncells[0] * ncells[1]
    else:
        n = ncells[0] * ncells[1] * ncells[2]
    # create integer array for cell ids
    iarray = np.arange(n, dtype="i4")
    iarray[:] += 1  # convert to 1-based
    cells_array_flatten = cells.reshape(n, order="F")

    h5file = _edit_vary_file(filename, mode="w")

    dataset_name = "Cell Ids"
    h5file.create_dataset(dataset_name, data=iarray)
    if vary_property == "permeability":
        dataset_name = "Permeability"
    elif vary_property == "pressure":
        dataset_name = "Pressure"
    h5file.create_dataset(dataset_name, data=cells_array_flatten)

    h5file.close()


def plot_vary_field(cells, filename, case="trigonometric", vary_property:str="permeability", **imshowargs):
    # 2d plot of a permeability field
    dimensionality = "2D"
    if dimensionality == "3D":
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        fig.suptitle(f"{vary_property} field [{case}]")
        axes = axes.ravel()
        axes[0].imshow(cells[:, :, 0])
        axes[2].imshow(cells[:, 0, :])
        axes[3].imshow(cells[0, :, :])
        axes[0].set_title("yz")
        axes[2].set_title("xz")
        axes[3].set_title("xy")
        for i in range(0, 4):
            axes[i].axis("off")
        fig.tight_layout()
    else:
        fig, axis = plt.subplots(1, 1, figsize=(10, 6))
        fig.suptitle(f"{vary_property} field [{case}]")
        plt.imshow(cells[:, :, 0], **imshowargs)
        plt.ylabel("x ")
        plt.xlabel("y")
        # fig.tight_layout()
        _aligned_colorbar()
        # fig.show()
    fig.savefig(f"{filename}.png")
    plt.close(fig)


def create_vary_fields(number_samples: int, folder: str, settings: Dict, plot_bool: bool = False, min_max: np.ndarray = None, filename_extension: str = "", vary_property: str = "permeability", ):
    # TODO vary frequency
    if not os.path.exists(folder):
        os.mkdir(folder)
    if not os.path.exists(f"{folder}/{vary_property}_fields"):
        os.mkdir(f"{folder}/{vary_property}_fields")

    # if not settings["general"]["random_bool"]:
    #     np.random.seed(settings["general"]["seed_id"])

    if settings[vary_property]["case"] == "perlin_noise":
        # vary bases to get different fields
        try:
            bases = sample(range(0, 255), number_samples)
        except ValueError:
            print("Number of desired perm-field variations exceeds 255.")
    elif settings[vary_property]["case"] == "perlin_v2":
        bases = range(number_samples)
    base_offset = np.random.rand(3) * 4242

    freq_factor = settings[vary_property]["frequency"]  # TODO vary like base

    for idx, base in enumerate(tqdm(bases)):
        if min_max is None:
            vary_min = settings[vary_property]["min"]
            vary_max = settings[vary_property]["max"]
        else:
            vary_min = np.min(min_max[idx])
            vary_max = np.max(min_max[idx])

        if vary_property == "permeability":
            vary_min = np.log10(vary_min)
            vary_max = np.log10(vary_max)

        cells = make_grid(
            settings,
            vary_min,
            vary_max,
            base=base,
            offset=base_offset + [base, 0, 0],
            freq=freq_factor,
            vary_property=vary_property,
        )

        if vary_property == "permeability":
            cells = 10 ** cells

        if vary_property == "pressure":
            cells = calc_pressure_from_gradient_field(cells, settings)

        filename = f"{folder}/{vary_property}_fields/{vary_property}_base_{base}{filename_extension}.h5"
        save_vary_field(filename, settings["grid"]["ncells"], cells, settings["general"]["dimensions"], vary_property=vary_property,)
        if plot_bool:
            plot_vary_field(cells, filename[:-3], case=settings[vary_property]["case"], vary_property=vary_property,)  # , vmax=settings["permeability"]["perm_max"], vmin=settings["permeability"]["perm_min"])
            
    # if vary_property == "pressure":
    #     cells = cells * 0
    #     filename = f"{folder}/{vary_property}_fields/empty_pressure_field.h5"
    #     save_vary_field(filename, settings["grid"]["ncells"], cells, settings["general"]["dimensions"], vary_property=vary_property,)


    logging.info(f"Created {len(bases)} {vary_property}-field(s)")
    return cells  # for pytest

def calc_pressure_from_gradient_field(gradient_field: np.array, settings: Dict):
    # calculate pressure field from gradient field

    # scale pressure field to -0.0035 and -0.0015
    current_min = np.min(gradient_field)
    current_max = np.max(gradient_field)
    new_min = settings["pressure"]["min"]
    new_max = settings["pressure"]["max"]
    gradient_field = (gradient_field - current_min) / (current_max - current_min) * (new_max - new_min) + new_min

    reference = 101325 # pressure
    len_cells = np.array(settings["grid"]["size"]) / np.array(settings["grid"]["ncells"])
    pressure_field = np.zeros_like(gradient_field)
    pressure_field[:,0] = reference
    for i in range(1, pressure_field.shape[1]):
        pressure_field[:,i] = pressure_field[:,i-1] + gradient_field[:,i] * len_cells[1] * 1000
    pressure_field = pressure_field[::-1]
    # for i in range(1, pressure_field.shape[0]):
    #     pressure_field[i,:] = (pressure_field[i-1,:] + gradient_field[i,:] * len_cells[0] + pressure_field[i,:])/2
    # pressure_field = gradient_field * len_cells[1] + reference
    import matplotlib.pyplot as plt
    plt.imshow(pressure_field)
    plt.colorbar()
    plt.show()
    return pressure_field


def read_and_plot_vary_field(settings: Dict, filename: str, vary_property: str = "permeability"):
    # read h5 perm file
    h5file = _edit_vary_file(filename, mode="r")

    # print header from h5 file
    if False:
        logging.info(h5file.keys())
        logging.info(h5file["Cell Ids"])
        logging.info(h5file["Cell Ids"][:])
        logging.info(h5file["Permeability"])
        logging.info(h5file["Permeability"][:])

    if vary_property == "permeability":
        vary_field_orig = h5file["Permeability"][:]
    elif vary_property == "pressure":
        vary_field_orig = h5file["Pressure"][:]
    vary_field = vary_field_orig.reshape(settings["grid"]["ncells"], order="F")
    plot_vary_field(vary_field, filename[-10:-3], case=settings[vary_property]["case"], vary_property=vary_property,)

    h5file.close()
    return vary_field  # for pytest


def _edit_vary_file(filename: str, mode: str = "r"):
    return File(filename, mode=mode)


if __name__ == "__main__":
    if True:
        # read input parameters
        cla_args = sys.argv
        logging.basicConfig(level=cla_args[1])
        number_samples = int(cla_args[2])
        folder_settings = "."

        output_folder = "."
        if len(cla_args) > 3:
            output_folder = cla_args[3]

        settings = load_yaml(folder_settings)
        # get min and max perm value
        try:
            perms_min_max = np.loadtxt(f"{output_folder}/permeability_values.txt")
        except:
            print("No permeability_values.txt file found. Using default ones from settings.")

        plot_bool = True  # if plot_bool then runs crash because try to load a png file as perm.h5 file
        create_vary_fields(
            number_samples, output_folder, settings, plot_bool, perms_min_max
        )
