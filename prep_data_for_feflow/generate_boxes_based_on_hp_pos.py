import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import pathlib
from tqdm.auto import tqdm
from shapely.geometry import Point
import pandas as pd

from generate_boxes_for_feflow import load_properties_after_aggregation, realistic_hydrogeological_params_boxes_and_hp_params, generate_box_geometries

def generate_wells_geometries(boxes_epsg, wells_epsg, valid_well_ids, desti_epsg, destination, box_len2D, store:bool=True):
    # make gpkg with extraction and injection well of same id; valid_well_id as global_id, i as box_id, and the box geometry in epsg
    geoms = []
    for box_id, well_id in zip(boxes_epsg.box_id, valid_well_ids):
        curr_wells = wells_epsg[wells_epsg.global_id == well_id].copy()
        curr_wells["box_id"] = box_id
    # print(curr_wells.head())
    # print(well_id, curr_wells.box_id)
        geoms.append(curr_wells)

    # Concatenate all wells
    geoms = gpd.GeoDataFrame(
    pd.concat(geoms, ignore_index=True),
    geometry="geometry",
    crs=desti_epsg
    )
    # geoms = gpd.GeoDataFrame(pd.concat(geoms), geometry="geometry", crs=desti_epsg)
    if store:
        geoms.to_file(destination / f"wells_in_boxes_{box_len2D}.gpkg", driver="GPKG")
    return geoms

def generate_wells_geometries_2hps(boxes_epsg, wells_epsg, valid_well_ids_1hp, valid_well_ids_2hp, desti_epsg, destination, box_len2D):
    # make gpkg with extraction and injection wells of same id; valid_well_id as global_id, i as box_id, and the box geometry in epsg
    geoms = []
    for box_id, well_id1, well_id2 in zip(boxes_epsg.box_id, valid_well_ids_1hp, valid_well_ids_2hp):
        curr_wells = wells_epsg[wells_epsg.global_id == well_id1].copy()
        curr_wells["box_id"] = box_id
        geoms.append(curr_wells)

        curr_wells = wells_epsg[wells_epsg.global_id == well_id2].copy()
        curr_wells["box_id"] = box_id
        geoms.append(curr_wells)

    # Concatenate all wells
    geoms = gpd.GeoDataFrame(
    pd.concat(geoms, ignore_index=True),
    geometry="geometry",
    crs=desti_epsg
    )
    # geoms = gpd.GeoDataFrame(pd.concat(geoms), geometry="geometry", crs=desti_epsg)
    geoms.to_file(destination / f"wells_in_boxes_{box_len2D}_2hp.gpkg", driver="GPKG")

    return geoms

def get_second_hp_in_box(box_id:int, boxes_epsg:gpd.GeoDataFrame, wells_epsg:gpd.GeoDataFrame, wells_inj:np.ndarray, wells_ext:np.ndarray, trafo_to_crs:rasterio.transform.Affine):
    # get window in crs
    polygon = boxes_epsg.geometry[box_id]

    # get 1hp-inj in crs
    well1hp_id = wells_epsg.global_id[wells_epsg.box_id == box_id].values[0]
    well1hp = wells_epsg[(wells_epsg.global_id == well1hp_id) & (wells_epsg.well_type == "injection")]
    # print(well1hp)

    # get 2nd hp-inj in crs
    for id2, pos2xi, pos2yi in wells_inj:
        if id2 != well1hp.global_id.iloc[0]: 
            pos2_crs = trafo_to_crs * (pos2xi, pos2yi)
            well2hp_inj = Point(pos2_crs[0], pos2_crs[1])
            # print(well2hp, well2hp.distance(well1hp.geometry.values[0]))
            if well2hp_inj.distance(well1hp.geometry.values[0]) > 10 and well2hp_inj.distance(well1hp.geometry.values[0]) < 320: #meters
                if well2hp_inj.within(polygon):
                    # return well2hp_inj, id2
                
                    # check extraction well #TODO
                    well2e_img = wells_ext[wells_ext[:,0] == id2][0]
                    pos2e_crs = trafo_to_crs * (well2e_img[1], well2e_img[2])
                    well2hp_ext = Point(pos2e_crs[0], pos2e_crs[1])
                    if well2hp_ext.within(polygon):
                        # print(f"Extraction and injection wells of id {id2}")
                        return id2 #well2hp_inj, well2hp_ext
    print("No second well found in box", box_id)
    return None


def preparation_for_box_generation():
    epsg_no = 25832
    desti_epsg = f"EPSG:{epsg_no}"
    reprojected_dir = pathlib.Path(f"aggregated_epsg{epsg_no}")
    properties_full, orig_resolution, trafo_to_crs = load_properties_after_aggregation(data_path=reprojected_dir) 
    trafo_to_img = ~trafo_to_crs

    wells_epsg = gpd.read_file("/home/pelzerja/pelzerja/test_nn/dataset_generation_laptop/Phd_simulation_groundtruth/prep_data_for_feflow/windows/wells_cnn.gpkg")
    wells_pos_img = trafo_to_img * (wells_epsg.geometry.x.values, wells_epsg.geometry.y.values)

    wells = np.array([wells_epsg.global_id.values, wells_epsg.well_type.values, wells_pos_img[0], wells_pos_img[1]]).T

    np.random.seed(1)
    np.random.shuffle(wells)

    wells_ext = wells[wells[:,1] == "extraction"] # since extraction well is the "upstream one" this one needs to be fitted
    wells_inj = wells[wells[:,1] == "injection"] 
    # TODO adapt - ensure both wells are in the box

    wells_ext = np.array([wells_ext[:,0], wells_ext[:,2].astype(float), wells_ext[:,3].astype(float)]).T
    wells_inj = np.array([wells_inj[:,0], wells_inj[:,2].astype(float), wells_inj[:,3].astype(float)]).T

    potential_start_positions_in_img = (wells_ext[:,1:3]).astype(int)
    # offset for start_positions in code

    return wells_epsg, wells_ext, wells_inj, potential_start_positions_in_img, properties_full, orig_resolution, trafo_to_crs, desti_epsg

def generate_boxes_with_single_hp(num_dp:int=1000):
    # settings
    destination = pathlib.Path("windows_1hp")
    destination.mkdir(exist_ok=True)
    box_len = np.array([320, 1280]) # in m

    wells_epsg, wells_ext, wells_inj, potential_start_positions_in_img, properties_full, orig_resolution, trafo_to_crs, desti_epsg = preparation_for_box_generation()

    # in img_space
    windows, _, box_len2D, valid_well_ids = realistic_hydrogeological_params_boxes_and_hp_params(properties_full, 20, box_len, num_dp = num_dp, start_positions_in_orig_cells=potential_start_positions_in_img, well_ids=wells_ext[:,0])
    boxes_epsg = generate_box_geometries(box_len2D, desti_epsg, trafo_to_crs, orig_resolution, windows, destination_dir=destination)
    # for i in [999, 998, 997]:
    #     well_img = wells_ext[wells_ext[:,0] == valid_well_ids[i]][0]
    #     well2_img = wells_inj[wells_inj[:,0] == valid_well_ids[i]][0]
    #     print(well_img)
    #     print(well2_img)
    #     print(windows[i]["start_pos"])
    #     print(windows[i]["rotation_angle"])
    #     polygon_img = trafo_to_img * np.array([boxes_epsg.geometry[i].exterior.coords.xy[0], boxes_epsg.geometry[i].exterior.coords.xy[1]])
    #     print(polygon_img)
    #     plt.figure(figsize=(5,5))
    #     plt.plot(polygon_img[0], polygon_img[1])
    #     # plt.scatter(windows[i]["start_pos"][0], windows[i]["start_pos"][1], color="red")
    #     plt.scatter(well_img[1], well_img[2], color="green")
    #     plt.scatter(well2_img[1], well2_img[2], color="blue")
    #     plt.xlim(300,400)
    #     plt.ylim(950,1050)
    #     plt.show()

    wells_epsg_small_1hp = generate_wells_geometries(boxes_epsg, wells_epsg, valid_well_ids, desti_epsg, destination, box_len2D)

    print("---------------Done---------------")
    print("Generated "f"{len(boxes_epsg)} boxes with 1 hp each.")
    print("first 5 boxes:\n", boxes_epsg.head())
    print("")
    print("first 5 wells:\n", wells_epsg_small_1hp.head())

def generate_boxes_with_two_hps(num_dp:int=1005):
    # settings
    destination = pathlib.Path("windows_2hp")
    destination.mkdir(exist_ok=True)

    box_len = np.array([1280, 1280]) # in m

    wells_epsg, wells_ext, wells_inj, potential_start_positions_in_img, properties_full, orig_resolution, trafo_to_crs, desti_epsg = preparation_for_box_generation()

    # in img_space
    windows_2hp, _, box_len2D_2hp, valid_well_ids_1hp = realistic_hydrogeological_params_boxes_and_hp_params(properties_full, 20, box_len, num_dp = num_dp, start_positions_in_orig_cells=potential_start_positions_in_img, well_ids=wells_ext[:,0])
    boxes_epsg_2hp = generate_box_geometries(box_len2D_2hp, desti_epsg, trafo_to_crs, orig_resolution, windows_2hp, store=False)
    wells_epsg_1hp = generate_wells_geometries(boxes_epsg_2hp, wells_epsg, valid_well_ids_1hp, desti_epsg, destination, box_len2D_2hp, store=False)

    # for box_id in range(10):
    #     plt.figure(figsize=(5,5))
    #     plt.plot(boxes_epsg_2hp.geometry[box_id].exterior.xy[0], boxes_epsg_2hp.geometry[box_id].exterior.xy[1])
    #     well1hp_id = wells_epsg_1hp.global_id[wells_epsg_1hp.box_id == box_id].values[0]
    #     well1hp = wells_epsg_1hp[wells_epsg_1hp.global_id == well1hp_id]
    #     plt.scatter(well1hp.geometry.x.values, well1hp.geometry.y.values, color="green")
    #     plt.show()

    # get set of second hp ids for all boxes
    valid_well_ids_2hp = []
    for box_id in tqdm(boxes_epsg_2hp.box_id):
        id2 = get_second_hp_in_box(box_id, boxes_epsg_2hp, wells_epsg_1hp, wells_inj, wells_ext, trafo_to_crs)
        valid_well_ids_2hp.append(id2)

    # for box_id, well2hp, well2hpe in wells_collect:
    #     plt.figure(figsize=(5,5))
    #     plt.plot(boxes_epsg_2hp.geometry[box_id].exterior.xy[0], boxes_epsg_2hp.geometry[box_id].exterior.xy[1])
    #     well1hp_id = wells_epsg_1hp.global_id[wells_epsg_1hp.box_id == box_id].values[0]
    #     well1hp = wells_epsg_1hp[wells_epsg_1hp.global_id == well1hp_id]
    #     plt.scatter(well1hp.geometry.x.values, well1hp.geometry.y.values, color="green")
    #     try:
    #         plt.scatter(well2hp.x, well2hp.y, color="red")
    #         plt.scatter(well2hpe.x, well2hpe.y, color="blue")
    #     except:
    #         pass
    #     plt.show()

    # exclude and store boxes(+wells) without valid 2nd hp from boxes_epsg_2hp and valid_wells_ids_1hp and valid_wells_ids_2hp
    boxes_epsg_2hp_valid = boxes_epsg_2hp[~pd.isna(valid_well_ids_2hp)].copy()
    valid_well_ids_1hp_valid = [id for id, id2 in zip(valid_well_ids_1hp, valid_well_ids_2hp) if id2 is not None]
    valid_well_ids_2hp_valid = [id2 for id2 in valid_well_ids_2hp if id2 is not None]

    # count how many NaNs in valid_well_ids_2hp
    print("Number of valid 2hp boxes:", sum([1 for id in valid_well_ids_2hp if id is not None]))
    # print(len(boxes_epsg_2hp_valid), len(valid_well_ids_1hp_valid), len(valid_well_ids_2hp_valid))

    wells_epsg_2hp = generate_wells_geometries_2hps(boxes_epsg_2hp_valid, wells_epsg, valid_well_ids_1hp_valid, valid_well_ids_2hp_valid, desti_epsg, destination, box_len2D_2hp)
    # store boxes:
    boxes_epsg_2hp_valid.to_file(f"windows_2hp/boxes_{box_len}_epgs_{desti_epsg.split(':')[1]}.gpkg", driver='GPKG', mode='w')

    print("---------------Done---------------")
    print("Generated "f"{len(boxes_epsg_2hp_valid)} boxes with 2 hps each.")
    print("first 5 boxes:\n", boxes_epsg_2hp_valid.head())
    print("")
    print("first 5 wells:\n", wells_epsg_2hp.head())

if __name__ == "__main__":
    generate_boxes_with_single_hp(num_dp=1000)
    generate_boxes_with_two_hps(num_dp=1005)