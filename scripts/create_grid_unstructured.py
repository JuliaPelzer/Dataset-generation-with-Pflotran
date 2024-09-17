import logging
import os
import sys
from typing import Dict, List
import pathlib
import argparse

import numpy as np

from scripts.calc_loc_hp_variation_2d import write_hp_additional_files
from scripts.make_general_settings import load_yaml, save_yaml


def write_mesh_file(path_to_output: str, settings: Dict):
    xGrid, yGrid, zGrid = settings["grid"]["ncells"]
    resolution = settings["grid"]["resulution"] # Cell width in metres

    faceArea = resolution**2
    volume = faceArea * resolution

    output_string = ["CELLS " + str(xGrid * yGrid * zGrid)]
    cellID_1 = 1
    for k in range(0, zGrid):
        zloc = (k + 0.5) * resolution
        for j in range(0, yGrid):
            yloc = (j + 0.5) * resolution
            for i in range(0, xGrid):
                xloc = (i + 0.5) * resolution
                output_string.append(f"\n{cellID_1}  {xloc}  {yloc}  {zloc}  {volume}")
                cellID_1 += 1

    output_string.append(f"\nCONNECTIONS {(xGrid - 1) * yGrid * zGrid+ xGrid * (yGrid - 1) * zGrid+ xGrid * yGrid * (zGrid - 1)}")
    for k in range(0, zGrid):
        zloc = (k + 0.5) * resolution
        for j in range(0, yGrid):
            yloc = (j + 0.5) * resolution
            for i in range(0, xGrid):
                xloc = (i + 0.5) * resolution
                cellID_1 = i + 1 + j * xGrid + k * xGrid * yGrid
                if i < xGrid - 1:
                    xloc_local = (i + 1) * resolution
                    cellID_2 = cellID_1 + 1
                    output_string.append(f"\n{cellID_1}  {cellID_2}  {xloc_local}  {yloc}  {zloc}  {faceArea}")
                if j < yGrid - 1:
                    yloc_local = (j + 1) * resolution
                    cellID_2 = cellID_1 + xGrid
                    output_string.append("\n"+ str(cellID_1)+ "  "+ str(cellID_2)+ "  "+ str(xloc)+ "  "+ str(yloc_local)+ "  "+ str(zloc)+ "  "+ str(faceArea))
                if k < zGrid - 1:
                    zloc_local = (k + 1) * resolution
                    cellID_2 = cellID_1 + xGrid * yGrid
                    output_string.append("\n"+ str(cellID_1)+ "  "+ str(cellID_2)+ "  "+ str(xloc)+ "  "+ str(yloc)+ "  "+ str(zloc_local)+ "  "+ str(faceArea))

    if not os.path.exists(path_to_output):
        os.makedirs(path_to_output)

    with open(str(path_to_output) + "/mesh.uge", "w") as file:
        file.writelines(output_string)

def write_loc_well_file(
    path_to_output: str, settings: Dict, loc_hp: np.array = None, idx: int = 0
):
    if loc_hp is None:
        loc_hp = settings["grid"]["loc_hp"]
    number_cells = settings["grid"]["ncells"]
    cell_widths = settings["grid"]["size [m]"] / np.array(
        number_cells
    )  # Cell width in metres

    i, j, k = np.array(loc_hp / cell_widths, int)
    if k == 0:
        k = 1
        if j == 0:
            j = 1
            if i == 0:
                i = 1
    cellID = int(
        i + (j - 1) * number_cells[0] + (k - 1) * number_cells[0] * number_cells[1]
    )
    assert cellID > 0, "CellID is negative"
    assert type(cellID) == int, "CellID is not an integer"

    with open(os.path.join(path_to_output, f"heatpump_inject{idx}.vs"), "w") as file:
        file.write(str(cellID))
    return cellID  # for pytest


def write_SN_files(path_to_output: str, settings: Dict):
    xGrid, yGrid, zGrid = settings["grid"]["ncells"]
    cell_widths = settings["grid"]["size [m]"] / np.array(
        settings["grid"]["ncells"]
    )  # Cell width in metres
    cellXWidth, _, cellZWidth = cell_widths
    _, yWidth, _ = settings["grid"]["size [m]"]

    if not cellXWidth == cellZWidth:
        logging.error("Something with create_grid_unstructured.py is wrong")
    else:
        faceArea = cellXWidth * cellZWidth

    output_string_north = ["CONNECTIONS " + str(xGrid * zGrid)]
    output_string_south = ["CONNECTIONS " + str(xGrid * zGrid)]
    yloc_north = yWidth
    yloc_south = 0
    for k in range(0, zGrid):
        zloc = 0.5 * cellZWidth + k * cellZWidth
        for i in range(0, xGrid):
            xloc = (i + 0.5) * cellXWidth
            cellID_north = (xGrid * (yGrid - 1)) + i + 1 + k * xGrid * yGrid
            cellID_south = i + 1 + k * xGrid * yGrid
            output_string_north.append("\n"+ str(cellID_north)+ "  "+ str(xloc)+ "  "+ str(yloc_north)+ "  "+ str(zloc)+ "  "+ str(faceArea))
            output_string_south.append("\n"+ str(cellID_south)+ "  "+ str(xloc)+ "  "+ str(yloc_south)+ "  "+ str(zloc)+ "  "+ str(faceArea))

    with open(str(path_to_output) + "/north.ex", "w") as file:
        file.writelines(output_string_north)
    with open(str(path_to_output) + "/south.ex", "w") as file:
        file.writelines(output_string_south)


def write_WE_files(path_to_output: str, settings: Dict):
    xGrid, yGrid, zGrid = settings["grid"]["ncells"]
    cell_widths = settings["grid"]["size [m]"] / np.array(
        settings["grid"]["ncells"]
    )  # Cell width in metres
    _, cellYWidth, cellZWidth = cell_widths
    xWidth, _, _ = settings["grid"]["size [m]"]

    if not cellYWidth == cellZWidth:
        logging.error("Something with create_grid_unstructured.py is wrong")
    else:
        faceArea = cellYWidth * cellZWidth

    output_string_east = ["CONNECTIONS " + str(yGrid * zGrid)]
    output_string_west = ["CONNECTIONS " + str(yGrid * zGrid)]
    xloc_east = xWidth
    xloc_west = 0
    for k in range(0, zGrid):
        zloc = 0.5 * cellZWidth + k * cellZWidth
        for j in range(0, yGrid):
            yloc = (j + 0.5) * cellYWidth
            cellID_east = (j + 1) * xGrid + k * xGrid * yGrid
            cellID_west = j * xGrid + 1 + k * xGrid * yGrid
            output_string_east.append("\n"+ str(cellID_east)+ "  "+ str(xloc_east)+ "  "+ str(yloc)+ "  "+ str(zloc)+ "  "+ str(faceArea))
            output_string_west.append("\n"+ str(cellID_west)+ "  "+ str(xloc_west)+ "  "+ str(yloc)+ "  "+ str(zloc)+ "  "+ str(faceArea))

    with open(str(path_to_output) + "/east.ex", "w") as file:
        file.writelines(output_string_east)
    with open(str(path_to_output) + "/west.ex", "w") as file:
        file.writelines(output_string_west)


def create_all_grid_files(settings, path_to_output: str = "."):
    write_mesh_file(path_to_output, settings)
    write_SN_files(path_to_output, settings)
    write_WE_files(path_to_output, settings)
    write_loc_well_file(path_to_output, settings)

    return settings

def make_mesh_files(args:argparse.Namespace, output_dataset_dir:pathlib.Path, settings: Dict, grid_size: np.array = None, ncells:np.array = None):
    # make grid files
    output_dataset_dir.mkdir(parents=True, exist_ok=True)
    settings = create_all_grid_files(settings, output_dataset_dir, grid_size, ncells)

    write_hp_additional_files(output_dataset_dir, args.num_hps) # region_hps, strata_hps, condition_hps.txt

    return settings