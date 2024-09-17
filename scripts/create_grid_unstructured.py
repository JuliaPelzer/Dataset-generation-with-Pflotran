import logging
import os
import sys
from typing import Dict, List
import pathlib
import argparse
import numpy as np

from scripts.calc_loc_hp_variation_2d import write_hp_additional_files


def write_mesh_file(path_to_output: pathlib.Path, settings: Dict):
    resolution = settings["grid"]["resolution"] # Cell width in metres
    xGrid, yGrid, zGrid = (np.array(settings["grid"]["size [m]"]) / resolution).astype(int)

    faceArea = resolution**2
    volume = faceArea * resolution

    output_string = [f"CELLS {xGrid * yGrid * zGrid}"]
    cells = np.ndarray((xGrid*yGrid*zGrid, 4))
    cellID_1 = 1
    for k in range(0, zGrid):
        zloc = (k + 0.5) * resolution
        for j in range(0, yGrid):
            yloc = (j + 0.5) * resolution
            for i in range(0, xGrid):
                xloc = (i + 0.5) * resolution
                output_string.append(f"\n{cellID_1}  {xloc}  {yloc}  {zloc}  {volume}")
                cells[cellID_1-1] = [cellID_1, xloc, yloc, zloc]
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

    with open(path_to_output / "mesh.uge", "w") as file:
        file.writelines(output_string)

    return cells

def write_loc_well_file(path_to_output: pathlib.Path, settings: Dict, loc_hp: np.array = None, idx: int = 0):
    resolution = settings["grid"]["resolution"] # Cell width in metres
    xGrid, yGrid, zGrid = (np.array(settings["grid"]["size [m]"]) / resolution).astype(int)
    
    if loc_hp is None:
        loc_hp = settings["grid"]["loc_hp"]
    i, j, k = np.array(loc_hp / resolution, int)
    if k == 0:
        k = 1
        if j == 0:
            j = 1
            if i == 0:
                i = 1
    cellID = int(i + (j - 1) * xGrid + (k - 1) * xGrid * yGrid)
    assert cellID > 0, "CellID is negative"

    with open(path_to_output / f"heatpump_inject{idx}.vs", "w") as file:
        file.write(str(cellID))
    return cellID  # for pytest


def write_SN_files(path_to_output: pathlib.Path, settings: Dict):
    resolution = settings["grid"]["resolution"] # Cell width in metres
    xGrid, yGrid, zGrid = (np.array(settings["grid"]["size [m]"]) / resolution).astype(int)

    yWidth = settings["grid"]["size [m]"][1]
    faceArea = resolution**2

    output_string_north = [f"CONNECTIONS {xGrid * zGrid}"]
    output_string_south = [f"CONNECTIONS {xGrid * zGrid}"]
    yloc_north = yWidth
    yloc_south = 0
    for k in range(0, zGrid):
        zloc = 0.5 * resolution + k * resolution
        for i in range(0, xGrid):
            xloc = (i + 0.5) * resolution
            cellID_north = (xGrid * (yGrid - 1)) + i + 1 + k * xGrid * yGrid
            cellID_south = i + 1 + k * xGrid * yGrid
            output_string_north.append(f"\n{cellID_north}  {xloc}  {yloc_north}  {zloc}  {faceArea}")
            output_string_south.append(f"\n{cellID_south}  {xloc}  {yloc_south}  {zloc}  {faceArea}")

    with open(path_to_output / "north.ex", "w") as file:
        file.writelines(output_string_north)
    with open(path_to_output / "south.ex", "w") as file:
        file.writelines(output_string_south)


def write_WE_files(path_to_output: pathlib.Path, settings: Dict):
    resolution = settings["grid"]["resolution"] # Cell width in metres
    xGrid, yGrid, zGrid = (np.array(settings["grid"]["size [m]"]) / resolution).astype(int)

    xWidth = settings["grid"]["size [m]"][0]
    faceArea = resolution**2

    output_string_east = ["CONNECTIONS " + str(yGrid * zGrid)]
    output_string_west = ["CONNECTIONS " + str(yGrid * zGrid)]
    xloc_east = xWidth
    xloc_west = 0
    for k in range(0, zGrid):
        zloc = 0.5 * resolution + k * resolution
        for j in range(0, yGrid):
            yloc = (j + 0.5) * resolution
            cellID_east = (j + 1) * xGrid + k * xGrid * yGrid
            cellID_west = j * xGrid + 1 + k * xGrid * yGrid
            output_string_east.append("\n"+ str(cellID_east)+ "  "+ str(xloc_east)+ "  "+ str(yloc)+ "  "+ str(zloc)+ "  "+ str(faceArea))
            output_string_west.append("\n"+ str(cellID_west)+ "  "+ str(xloc_west)+ "  "+ str(yloc)+ "  "+ str(zloc)+ "  "+ str(faceArea))

    with open(path_to_output / "east.ex", "w") as file:
        file.writelines(output_string_east)
    with open(path_to_output / "west.ex", "w") as file:
        file.writelines(output_string_west)


def write_TB_files(path_to_output: pathlib.Path, settings: Dict):
    resolution = settings["grid"]["resolution"] # Cell width in metres
    xGrid, yGrid, zGrid = (np.array(settings["grid"]["size [m]"]) / resolution).astype(int)

    zWidth = settings["grid"]["size [m]"][2]
    faceArea = resolution**2

    output_string_top = ["CONNECTIONS " + str(xGrid * yGrid)]
    output_string_bottom = ["CONNECTIONS " + str(xGrid * yGrid)]
    zloc_top = zWidth # TODO so rum richtig?
    zloc_bottom = 0 # TODO so rum richtig?

    for k in range(0, yGrid):
        # TODO
        yloc = ...
        for j in range(0, xGrid):
            xloc = ...
            cellID_top = ...
            cellID_bottom = ...
            output_string_top.append(f"\n{cellID_top}  {xloc}  {yloc}  {zloc_top}  {faceArea}")
            output_string_bottom.append(f"\n{cellID_bottom}  {xloc}  {yloc}  {zloc_bottom}  {faceArea}")

    with open(path_to_output / "top.ex", "w") as file:
        file.writelines(output_string_top)
    with open(path_to_output / "bottom.ex", "w") as file:
        file.writelines(output_string_bottom)


def create_mesh_files(path_to_output: pathlib.Path, settings: Dict):
    cells = write_mesh_file(path_to_output, settings)
    write_SN_files(path_to_output, settings)
    write_WE_files(path_to_output, settings)
    # write_TB_files(path_to_output, settings)

    return cells