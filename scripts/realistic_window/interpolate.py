import numpy as np
from scipy.interpolate import RegularGridInterpolator
from typing import Dict

def interpolate_properties(property_fields:Dict[str,np.array]) -> Dict[str, RegularGridInterpolator]:
    # make property continuous through interpolation
    interpolators = {}
    for key in property_fields.keys():
        x,y = np.arange(property_fields[key].shape[0]), np.arange(property_fields[key].shape[1]) # accelerate: rausziehen aus for-loop
        interpolators[key] = RegularGridInterpolator((x,y), property_fields[key], bounds_error=False, fill_value=None)
    return interpolators


def interpolate_windows(orig_resolution:int, window_shape, window_properties, desti_resolution:int):
    # TODO where? pixel ist orientiert an lower left -> korrektur notwendig: +0.5 resolution in beide richtungen 
    # TODO achtung, wenn orig_res NOT div-able by desti_reso
    window_desti_cells = tuple(np.meshgrid(np.arange(0, window_shape[0],
                                                       step=desti_resolution/orig_resolution),
                                             np.arange(0, window_shape[1],
                                                       step=desti_resolution/orig_resolution)))
    # alternative: load mesh.uge and somehow evaluate at those positions: mesh.uge entsprocht pflotran.h5, nutze DomainYC/XC von mesh.uge für interpolator
    # window_orig_cells = tuple(np.meshgrid(np.arange(0, window_shape[0]),
    #                                  np.arange(0, window_shape[1])))
    interpolators = interpolate_properties(window_properties)
    window_desti_values = {}
            # orig_values = {}
    for key in interpolators.keys():
        window_desti_values[key] = interpolators[key](window_desti_cells)

        # plt.figure()
        # plt.title(key)
        # plt.imshow(window_desti_values[key], origin="lower")
        # plt.savefig("test_interpo.png")

        # plt.figure()
        # orig_values[key] = interpolators[key](window_orig_cells)
        # plt.title(key)
        # plt.imshow(orig_values[key], origin="lower")
        # plt.savefig("test_.png")

        # plt.figure()
        # plt.title(key)
        # plt.scatter(window_rotated_cells[1], window_rotated_cells[0], c=window_properties[key])
        # plt.savefig("test_orig.png")
        # exit()

    return window_desti_values
