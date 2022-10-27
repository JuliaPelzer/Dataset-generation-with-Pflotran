import numpy as np
import matplotlib.pyplot as plt
import os
from h5py import *
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
import noise
from typing import Tuple, Dict, Union
from dataclasses import dataclass
from tqdm import tqdm

@dataclass
class Settings:
    ncells      :   np.array    =   np.array([20,150,12])
    size        :   np.array    =   np.array([100,500,30])
    perm_max    :   float       =   6.65*10**-9
    perm_min    :   float       =   1.36*10**-12
    factor      :   float       =  40
    case        :   str         = "perlin_noise"
    frequency   :   Union[int, Tuple[int, int, int]]    =   (4,9,3)

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
    cells_array_flatten = cells.reshape(n, order='F')

    h5file = File(filename,mode='w')

    # create integer array for cell ids
    iarray = np.arange(n,dtype='u8')
    # convert to 1-based
    iarray[:] += 1
    dataset_name = 'Cell Ids'
    h5dset = h5file.create_dataset(dataset_name, data=iarray)

    # create double array for porosities
    # rarray = np.zeros(n,dtype='f8')
    # rarray[:] = 0.25
    # rarray[4:7] = 0.3
    dataset_name = 'Permeability'
    h5dset = h5file.create_dataset(dataset_name, data=cells_array_flatten)

    h5file.close()

# 2d plot of the permeability field
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

def create_perm_field(number_samples:int, filename_extension:str=None):
        # ncells:np.ndarray=np.ndarray([20,150,12]), 
        # size:np.ndarray=np.ndarray([100,500,30]), perm_max:float=6.65*10**-9,perm_min:float=1.36*10**-12,
        # factor:float=40, case:str="perlin_noise", frequency:Union[int, Tuple[int, int, int]]=10, base:int=0):
    
    # TODO dimensionen? Reihenfolge?
    # TODO vary frequency
    
    current_dir = os.getcwd()
    folder = os.path.join(current_dir, "vary_permeability/permeability_fields")
    if not os.path.exists(folder):
        os.mkdir(folder)

    settings = Settings() #ncells, size, perm_max, perm_min, factor, case, frequency)
    with open(f"{folder}/perm_field_parameters.txt", "w") as f:
        f.write(settings.all_settings_to_str())

    # vary bases to get different fields
    bases = np.random.randint(0, 2**25, size=number_samples) 

    for base in tqdm(bases):
        cells, _ = make_perm_grid(settings, base)
        filename = f"{folder}/permeability_base_{base}_{filename_extension}.h5"
        save_perm(filename, settings.ncells, cells)

if __name__=="__main__":
    create_perm_field(100, "test")

    # size = np.array([500, 1000, 30])
    # ncells = np.array([75, 150, 12])