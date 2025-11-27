import numpy as np
from typing import Tuple
import logging
import yaml
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pathlib import Path
import csv
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, Point
from skimage.draw import polygon

from aggregate import main as aggregate_main


# helper functions
def load_geotiff(file_path):
    # load geoTIFF files
    with rasterio.open(file_path) as src:
        img = src.read()
        img = img.squeeze()
    return np.array(img)

def load_properties_after_aggregation(data_path: Path) -> tuple[dict[str, np.ndarray], int]:
    properties = {"dtw": "Flur_20.tif",
                  "drawdown": "Drawdown_20.tif", # max. Pumprate des Förderbrunnens an der Stelle , [l/s]
                  "hydraulic_conductivity": "Cond_20.tif",# [m/s]
                  "hydraulic_gradient": "Grad_20.tif", # [m/m]
                  "thickness": "Thick_20.tif", # [m]
                  "darcy_dir": "darcydir_south_zero.tif", # [°]
                  "darcy_dir2": "Direc_20.tif", # [°]
                  "gwgl": "Gwgl_20.tif", # [m]
                  "tok": "Tok_20.tif"} # [m]
    
    data = {}
    for key, value in properties.items(): # load data
        data[key] = load_geotiff(data_path / value)
        print(f"Loaded {key} from {value} with shape {data[key].shape} and dtype {data[key].dtype}")
        
    data = align_holes(data)
    data["darcy_velocity"] = data["hydraulic_conductivity"] * data["hydraulic_gradient"] * 60*60*24# [m/s]
    data["darcy_velocity"][np.isnan(data["hydraulic_conductivity"])] = np.nan
    
    resolution = yaml.safe_load(open(data_path / "resolution.yaml", "r"))[0]  # in meters
    return data, resolution

def align_holes(data:dict) -> dict:
    mask = data["gwgl"] < 0
    for key in data.keys():
        mask = mask | np.isnan(data[key]) | (data[key] < -1e35)

    for key in data.keys():
        data[key][mask] = np.nan
    return data

def get_start_positions(data: np.ndarray, info:dict):
    '''calculates + shuffles all positions in data, returns [(id1x, id1y), (id2x,id2y), ...]'''
    ids = np.array([(j,i) for i in range(data.shape[0]) for j in range(data.shape[1])])
    not_nan_ids = ids[~np.isnan(data).flatten()]

    if info["random_bool"]:
        print("Randomizing order of windows")
        # np.random.seed(info["seed_id"])
        np.random.shuffle(not_nan_ids)
    else:
        print("Not randomizing order of windows")

    return not_nan_ids

def sample_median(field: np.ndarray, start_pos, field_size: np.ndarray[int, int] = np.array([100,100])) -> float:
    # general direction of flow is from south to north, hence to get as realistic median values as possible, we have to align this box in the same direction (relative to the start-position), hence the minus in front of the field_size[1]

    field = field[start_pos[1]-int(field_size[1]/2):start_pos[1]+int(field_size[1]/2), start_pos[0]-int(field_size[0]/2):start_pos[0]+int(field_size[0]/2)]
    # falls alle Werte in der Box nan sind - dann jump einfach zu nächsten potentiellen Startpunkt ausprobieren
    if np.isnan(field).all():
        raise ValueError("All values in box are nan")

    median = np.nanmedian(field)
    return median

def rot_matrix(angle_in_rad):
    return np.array([
        [np.cos(angle_in_rad), -np.sin(angle_in_rad)],
        [np.sin(angle_in_rad), np.cos(angle_in_rad)]
    ])

def local_to_global(window_shape, angle_in_deg, start_pos):
    corners = np.array([
    [- window_shape[0]/2, - window_shape[1]/2],
    [- window_shape[0]/2, + window_shape[1]/2],
    [+ window_shape[0]/2, + window_shape[1]/2],
    [+ window_shape[0]/2, - window_shape[1]/2],
    ])
    angle_in_rad = np.deg2rad(angle_in_deg)
    return np.dot(corners, rot_matrix(angle_in_rad)) + start_pos

def cut_out_values(data:np.ndarray, rotated_box_cells: Tuple[np.ndarray, np.ndarray]) -> np.ndarray:  
    cells_x = rotated_box_cells[0].flatten()
    cells_y = rotated_box_cells[1].flatten()
    # extract data on meshgrid coordinates "rotated box coords"
    rotated_box_values = data[cells_y.astype(int), cells_x.astype(int)]
    rotated_box_values = rotated_box_values.reshape(rotated_box_cells[0].shape)

    return rotated_box_values

def check_validity_window(data:np.ndarray, window:Tuple[np.ndarray,np.ndarray]) -> bool: #Tuple[bool, np.ndarray]:
    """ window is still in cell "coords" of original data """
    # check that window within data range
    if np.any(window[0] < 0) or np.any(window[1] < 0) or np.any(window[0] >= data.shape[1]) or np.any(window[1] >= data.shape[0]):
        return False
    # check window for nan values
    box = cut_out_values(data, window)
    if np.any(np.isnan(box)):
        print("Window contains NaN values")
        return False
    else:
        print("Window is valid")
        return True
    
def check_box_validity_fast(data: np.ndarray, corners: np.ndarray) -> bool:
    # corners: (2, 4) array of (x, y)
    # polygon expects (row, col) -> (y, x)
    if np.any(corners[0] < 0) or np.any(corners[1] < 0) or np.any(corners[0] >= data.shape[1]) or np.any(corners[1] >= data.shape[0]):
        return False
    rr, cc = polygon(corners[1], corners[0], shape=data.shape)
    values = data[rr, cc]
    return not np.isnan(values).any()

# extract windows (start positions + rotations)
def realistic_hydrogeological_params_boxes_and_hp_params(properties_full, orig_resolution, box_len, num_dp:int):

    # 2. get all start points, randomized (NOT checked for validity yet) or manual start point, e.g.  # start_positions = [[2100, 2300]]
    start_positions_in_orig_cells = get_start_positions(properties_full["dtw"], {"random_bool": True})

    windows_collected = []
    n_valid_windows = 0
    not_valid_windows_collected = []
    # while not enough windows:
    for i, start_pos in enumerate(start_positions_in_orig_cells):
        try:
            window_shape_in_orig_cells = np.array([box_len/orig_resolution, box_len/orig_resolution]).astype(int) # get window shape in original cells
            rotation_angle_degree = - sample_median(properties_full["darcy_dir"], start_pos, window_shape_in_orig_cells) # extract median direction in window
            window_rotated_cells = local_to_global(window_shape_in_orig_cells, rotation_angle_degree, start_pos).T # coords of rotated window # TODO wieso .T??
        except Exception as e:
            print(e)
            continue

        # 6. check window for nans
        valid = check_box_validity_fast(properties_full["dtw"], window_rotated_cells)

        if valid:
            windows_collected.append({"start_pos": start_pos, "rotation_angle": rotation_angle_degree})
            print("valid", i, start_pos, rotation_angle_degree)
            n_valid_windows += 1
        else:
            not_valid_windows_collected.append({"start_pos": start_pos, "rotation_angle": rotation_angle_degree})
            continue

        if n_valid_windows >= num_dp:
            print(n_valid_windows, " valid windows found within", i+1, "tries")
            return windows_collected, not_valid_windows_collected

    logging.warning(n_valid_windows, " valid windows found within", i+1, "tries")
    if n_valid_windows < num_dp:
        logging.error(f"Not enough windows found. Only {n_valid_windows} found.")

    return windows_collected, not_valid_windows_collected

def export_windows_to_csv(windows_collected, not_valid_windows_collected, box_len, window_dir):
    for case in ["valid", "not_valid"]:
        if case == "valid":
            windows = windows_collected
            file_path = window_dir / f"windows_{box_len}_collected.csv"
        else:
            windows = not_valid_windows_collected
            file_path = window_dir / f"windows_not_valid_{box_len}_collected.csv"

        with open(file_path, "w", newline='') as csvfile:
            fieldnames = ["run_id", "start_pos_x", "start_pos_y", "rotation_angle"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for run_id, window in enumerate(windows):
                writer.writerow({
                    "run_id": run_id,
                    "start_pos_x": window["start_pos"][0],
                    "start_pos_y": window["start_pos"][1],
                    "rotation_angle": window["rotation_angle"] # TODO *-1?
                })

def check_windows():
    with open("windows/windows_collected.csv", "r", newline='') as csvfile:
        start_positions_in_orig_cells = []
        boxes_angle = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_positions_in_orig_cells.append((int(row["start_pos_x"]), int(row["start_pos_y"])) ) # passt
            boxes_angle.append(float(row["rotation_angle"]) ) # passt

            print(int(row["start_pos_x"]), int(row["start_pos_y"]), float(row["rotation_angle"]) )

    with open("windows/windows_not_valid_collected.csv", "r", newline='') as csvfile:
        not_valid_start_positions_in_orig_cells = []
        not_valid_boxes_angle = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            not_valid_start_positions_in_orig_cells.append((int(row["start_pos_x"]), int(row["start_pos_y"])) ) # passt
            not_valid_boxes_angle.append(float(row["rotation_angle"]) ) # passt

    # plot windows on map
    plt.figure(figsize=(10,10))
    plt.imshow(properties_full["gwgl"],cmap="tab20")
    plt.colorbar()
    for i, (pos, angle) in enumerate(zip(start_positions_in_orig_cells, boxes_angle)):
        plt.scatter(pos[0], pos[1], color="red")
        window_rotated_cells = local_to_global([256,256], angle, pos).T # coords of rotated window
        plt.scatter(window_rotated_cells[0], window_rotated_cells[1], color="black")
        # break
    plt.title("Start Positions and Boxes")
    plt.show()

def reproject_tiff(src_path, dst_path, dst_crs):
    # reproject tiffs to epsg:25832
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    transform_check = None
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
        # print(src.crs, dst_crs, src.width, src.height, src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        if transform_check is not None:
            assert np.allclose(transform_check, transform), "transforms do not match!"
        transform_check = transform

        with rasterio.open(dst_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
    
    return transform_check
               

def generate_box_geometries(local_to_global, box_len, desti_epsg, trafo_epsg, orig_resolution, windows_collected):
    start_positions_in_orig_cells = []
    boxes_angle = []

    for window in windows_collected:
            start_positions_in_orig_cells.append((window["start_pos"]))
            boxes_angle.append(window["rotation_angle"] ) 

    # transform windows to new coordinate system
    box_length = box_len /orig_resolution

    # prepare box minx, miny, maxx, maxy for every box in list
    collected_corners = []
    collected_centers = []
    n_boxes = len(start_positions_in_orig_cells)
            
    for i in range(n_boxes):
        # rotate corners around start position
        rotated_corners = local_to_global([box_length, box_length], boxes_angle[i], start_positions_in_orig_cells[i])
        collected_corners.append(np.array([trafo_epsg * (corner[0], corner[1]) for corner in rotated_corners]))

        collected_centers.append(trafo_epsg * (start_positions_in_orig_cells[i][0], start_positions_in_orig_cells[i][1]))

    geoms = []
    for corners, center in zip(collected_corners, collected_centers):
        geoms.append(Polygon(corners))
        geoms.append(Point(center))

    box_geoms = gpd.GeoDataFrame(geometry=geoms, crs=f'epsg:{desti_epsg.split(":")[1]}')

    box_geoms.to_file(f"windows/boxes_{box_len}_epgs_{desti_epsg.split(':')[1]}.gpkg", driver='GPKG', mode='w')
    print("boxes extracted for epsg:", desti_epsg)

if __name__ == "__main__":
    box_len = 4000
    desti_epsg = "EPSG:31468" #31468 5678
    num_dp = 100
    orig_res = 20

    ORIG_dir = Path("shared_data_Fabian")
    aggregated_dir = Path("aggregated")
    reprojected_dir = Path(f"aggregated_epsg{desti_epsg.split(':')[1]}")
    windows_dir = Path("windows")
    windows_dir.mkdir(parents=True, exist_ok=True)

    # # aggregate with python
    aggregate_main(ORIG_dir, aggregated_dir, orig_res)

    # put into different epsg
    for src_path in aggregated_dir.glob("*.tif"):
        trafo_epsg = reproject_tiff(src_path, reprojected_dir / src_path.name, dst_crs=desti_epsg)
    print(trafo_epsg)

    # 1. load full maps # properties_full: 1px (=1cell) = 20m (=orig_resolution)
    properties_full, orig_resolution = load_properties_after_aggregation(data_path=aggregated_dir) 

    windows_collected, not_valid_windows_collected = realistic_hydrogeological_params_boxes_and_hp_params(properties_full, orig_resolution, box_len, num_dp=num_dp)
    export_windows_to_csv(windows_collected, not_valid_windows_collected, box_len, windows_dir)

    generate_box_geometries(local_to_global, box_len, desti_epsg, trafo_epsg, orig_resolution, windows_collected)