import rasterio
import numpy as np
import yaml
from pathlib import Path
from scipy.interpolate import RegularGridInterpolator
from typing import Dict

# load geoTIFF files
def load_geotiff(file_path):
    with rasterio.open(file_path) as src:
        img = src.read()
        img = img.squeeze()
    return np.array(img)

def load_properties_after_R_prep(data_path: Path) -> dict:
    properties = {"dtw": "Depth_to_water_20m_resolution.tif",
                  "drawdown": "Drawdown_20m_resolution.tif", # max. Pumprate des Förderbrunnens an der Stelle #TODO Einheit
                  "hydraulic_conductivity": "Hydraulic_conductivity_20m_resolution.tif",# [m/s]
                  "hydraulic_gradient": "Hydraulic_gradient_20m_resolution.tif", # [m/m]
                  "thickness": "Aquifer_thickness_20m_resolution.tif", # [m]
                  "darcy_dir": "Direction_of_flow_South_Zero_20m_resolution.tif", # [°]
                  "gwgl": "Gwgl_20m_resolution.tif", # [m]
                  "tok": "Tok_20m_resolution.tif"} # [m]
    # load data
    data = {}
    for key, value in properties.items():
        data[key] = load_geotiff(data_path / value)
        
    data = align_holes(data)
    
    data["darcy_velocity"] = data["hydraulic_conductivity"] * data["hydraulic_gradient"] * 60*60*24# [m/s]
    data["darcy_velocity"][np.isnan(data["hydraulic_conductivity"])] = np.nan
    
    resolution = yaml.safe_load(open(data_path / "resolution.yaml", "r"))
    return data, resolution

def align_holes(data:dict) -> dict:
    mask = data["gwgl"] < 0
    for key in data.keys():
        mask = mask | np.isnan(data[key]) | (data[key] < -1e35)

    for key in data.keys():
        data[key][mask] = np.nan
    return data

def interpolate_properties(property_fields:Dict[str,np.array]) -> Dict[str, RegularGridInterpolator]:
    # make property continuous through interpolation
    interpolators = {}
    for key in property_fields.keys():
        x,y = np.arange(property_fields[key].shape[0]), np.arange(property_fields[key].shape[1])
        interpolators[key] = RegularGridInterpolator((x,y), property_fields[key], bounds_error=False, fill_value=None)
    return interpolators