from random import random, seed
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from h5py import *
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
import noise
from typing import Tuple, Dict, Union
from dataclasses import dataclass
from tqdm import tqdm
import logging

@dataclass
class Settings:
    random_bool      :   bool
    ncells      :   np.array    =   np.array([20,150,16])
    size        :   np.array    =   np.array([100,750,80])
    perm_max    :   float       =   6.65*10**-9
    perm_min    :   float       =   1.36*10**-12
    factor      :   float       =  40
    case        :   str         = "perlin_noise"
    frequency   :   Union[int, Tuple[int, int, int]]    =   (4,9,3)
    seed_id     :   int         =   0
    # seed        :   int         =   np.random.seed(seed_id)

    def get_keys(self):
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]

    def get_next_value(self):
        for key in self.get_keys():
            yield getattr(self, key)

    def get_all_settings(self):
        return {key: getattr(self, key) for key in self.get_keys()}

    def all_settings_to_str(self):
        # for putting them into a settings file
        return_str = ""
        for key in self.get_keys():
            return_str += f"{key} : {getattr(self, key)} \n"
        return return_str

def make_perm_grid(settings:Settings, base:float = 0):
    length_cells = settings.size / settings.ncells
    icells = [np.linspace(1, settings.ncells[i], settings.ncells[i]) for i in (0,1,2)]
    idx, idy, idz = np.meshgrid(icells[0], icells[1], icells[2], indexing="ij")
    if settings.case=="trigonometric":
        # function exemplary
        def fct_sin(value):
            return (settings.perm_max - settings.perm_min)/2 * np.sin(value/settings.factor) + (settings.perm_max + settings.perm_min)/2
        def fct_cos(value):
            return (settings.perm_max - settings.perm_min)/2 * np.cos(value/settings.factor) + (settings.perm_max + settings.perm_min)/2
        values = (fct_cos(idx*length_cells[1])+fct_cos(idy*length_cells[0])+fct_cos(idz*length_cells[2]))/3  # ORDER X,Y,Z
    elif settings.case=="rand_interpolate":
        # Interpolation with RegularGridInterpolator from scipy (can do 3D, works on a regular grid)
        nbases = 5
        length_cells_base = settings.size / nbases
        icells_base = [np.linspace(1, settings.ncells[i], nbases) for i in (0,1,2)]
        idx_base, idy_base, idz_base = np.meshgrid(icells_base[0], icells_base[1], icells_base[2], indexing="ij") # ORDER X,Y,Z

        def fct_rand(shape=[nbases,nbases,nbases]):
            return np.random.uniform(settings.perm_min, settings.perm_max, size=shape)
        values_base = fct_rand()

        test_points = np.array([idx.ravel(), idy.ravel(), idz.ravel()]).T
        interpolator = RegularGridInterpolator(icells_base, values_base)
        method = "linear" # in ['linear', 'nearest', 'slinear', 'cubic', 'quintic']:
        values = interpolator(test_points, method=method).reshape(settings.ncells[0], settings.ncells[1], settings.ncells[2]).T

    elif settings.case=="perlin_noise":
        def perlin_noise(x,y,z):
            return noise.pnoise3(x, y, z, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, repeatz=1024, base=base)
        values = np.zeros((settings.ncells[0], settings.ncells[1], settings.ncells[2]))
        for i in range(0, settings.ncells[0]):
            for j in range(0, settings.ncells[1]):
                for k in range(0, settings.ncells[2]):
                    freq = settings.frequency / settings.ncells
                    x,y,z = [i, j, k] * freq
                    values[i,j,k] = (perlin_noise(x,y,z)+1)/2 * (settings.perm_max - settings.perm_min) + settings.perm_min
    
    return values, icells

def save_perm(filename, ncells, cells):
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

    # create double array for porosities
    # rarray = np.zeros(n,dtype='f8')
    # rarray[:] = 0.25
    # rarray[4:7] = 0.3

# 2d plot of a permeability field
def plot_perm(cells, case="trigonometric"):
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
    # plt.colorbar()
    fig.show()
    
def create_perm_field(number_samples:int, filename_extension:str=None, random_bool:bool=False):
        # ncells:np.ndarray=np.ndarray([20,150,16]), 
        # size:np.ndarray=np.ndarray([100,750,80]), perm_max:float=6.65*10**-9,perm_min:float=1.36*10**-12,
        # factor:float=40, case:str="perlin_noise", frequency:Union[int, Tuple[int, int, int]]=10, base:int=0):
    
    # TODO dimensionen? Reihenfolge?
    # TODO vary frequency
    
    current_dir = os.getcwd()
    folder = os.path.join(current_dir, "permeability_fields")
    if not os.path.exists(folder):
        os.mkdir(folder)

    settings = Settings(random_bool) #ncells, size, perm_max, perm_min, factor, case, frequency)
    if not settings.random_bool:
        np.random.seed(settings.seed_id)
    with open(f"{folder}/perm_field_parameters.txt", "w") as f:
        f.write(settings.all_settings_to_str())

    # vary bases to get different fields
    bases = np.random.randint(0, 2**25, size=number_samples) 

    for base in tqdm(bases):
        cells, _ = make_perm_grid(settings, base)
        filename = f"{folder}/permeability_base_{base}_{filename_extension}.h5"
        save_perm(filename, settings.ncells, cells)
        plot_perm(cells, case=settings.case)
    
    logging.info("Created perm-field")
    return cells, settings # for pytest

def read_and_plot_perm_field(settings:Settings, filename:str="permeability_fields/permeability_base_8325804_test.h5"):
    # read h5 perm file
    h5file = _edit_perm_file(filename,mode='r')

    # print header in h5 file
    if False:
        logging.info(h5file.keys())
        logging.info(h5file['Cell Ids'])
        logging.info(h5file['Cell Ids'][:])
        logging.info(h5file['Permeability'])
        logging.info(h5file['Permeability'][:])
    perm_field_orig = h5file['Permeability'][:]
    perm_field = perm_field_orig.reshape((16,150,20)).T # TODO SETTINGSSIZE
    plot_perm(perm_field, case="perlin_noise")

    h5file.close()
    return perm_field # for pytest

def _edit_perm_file(filename:str, mode:str="r"):
    return File(filename, mode=mode)

if __name__=="__main__":

    # read input parameters
    cla_args = sys.argv
    logging.basicConfig(level=cla_args[1])
    number_samples = int(cla_args[2])
    filename_extension = cla_args[3]
    random_bool = bool(cla_args[4])
    create_perm_field(number_samples, filename_extension, random_bool)
    
    # _, settings = create_perm_field(number_samples, filename_extension, random_bool)
    # read_and_plot_perm_field(settings, "permeability_fields/permeability_base_8325804_test.h5")