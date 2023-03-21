import numpy as np
import sys
import os
import logging
from typing import Dict
from scripts.make_general_settings import load_settings, change_grid_domain_size, save_settings

def write_mesh_file(path_to_output:str, settings:Dict):
	xGrid, yGrid, zGrid = settings["grid"]["ncells"]
	cell_widths = settings["grid"]["size"]/np.array(settings["grid"]["ncells"])	# Cell width in metres
	cellXWidth, cellYWidth, cellZWidth = cell_widths

	volume = cellXWidth*cellYWidth*cellZWidth
	if cellXWidth == cellYWidth and cellXWidth == cellZWidth:
		faceArea = cellXWidth**2
	else:
		logging.error("The grid is not cubic - look at create_grid_unstructured.py OR 2D case and settings.yaml depth for z is not adapted")

	output_string = []
	output_string.append("CELLS "+str(xGrid*yGrid*zGrid))
	cellID_1 = 1
	for k in range(0,zGrid):
		zloc = (k + 0.5)*cellZWidth
		for j in range(0,yGrid):
			yloc = (j + 0.5)*cellYWidth
			for i in range(0,xGrid):
				xloc = (i + 0.5)*cellXWidth
				output_string.append("\n" + str(cellID_1)+"  "+str(xloc)+"  "+str(yloc)+"  "+str(zloc)+"  "+str(volume))
				# check for location of heat pump
				# if [52.5,122.5,52.5] == [xloc, yloc, zloc]:
				# 	print("CALC", cellID)
				cellID_1 += 1

	output_string.append("\nCONNECTIONS " + str((xGrid-1)*yGrid*zGrid + xGrid*(yGrid-1)*zGrid + xGrid*yGrid*(zGrid-1)))
	for k in range(0,zGrid):
		zloc = (k + 0.5)*cellZWidth
		for j in range(0,yGrid):
			yloc = (j + 0.5)*cellYWidth
			for i in range(0,xGrid):
				xloc = (i + 0.5)*cellXWidth
				cellID_1 = i+1 + j*xGrid + k*xGrid*yGrid
				if i < xGrid-1:
					xloc_local = (i + 1)*cellXWidth
					cellID_2 = cellID_1+1
					output_string.append("\n" + str(cellID_1)+"  "+str(cellID_2)+"  "+str(xloc_local)+"  "+str(yloc)+"  "+str(zloc)+"  "+str(faceArea))
				if j < yGrid-1:
					yloc_local = (j + 1)*cellYWidth
					cellID_2 = cellID_1+xGrid
					output_string.append("\n" + str(cellID_1)+"  "+str(cellID_2)+"  "+str(xloc)+"  "+str(yloc_local)+"  "+str(zloc)+"  "+str(faceArea))
				if k < zGrid-1:
					zloc_local = (k + 1)*cellZWidth
					cellID_2 = cellID_1+xGrid*yGrid
					output_string.append("\n" + str(cellID_1)+"  "+str(cellID_2)+"  "+str(xloc)+"  "+str(yloc)+"  "+str(zloc_local)+"  "+str(faceArea))

	if not os.path.exists(path_to_output):
		os.makedirs(path_to_output)
		
	with open(str(path_to_output)+"/mesh.uge", "w") as file:
		file.writelines(output_string)

def write_loc_well_file(path_to_output:str, settings:Dict, loc_hp:np.array=None, idx:int=1):
	if loc_hp is None:
		loc_hp = settings["grid"]["loc_hp"]
	number_cells = settings["grid"]["ncells"]
	cell_widths = settings["grid"]["size"]/np.array(number_cells)	# Cell width in metres

	i,j,k = np.array(loc_hp/cell_widths, int)
	if k == 0:
		k = 1
	cellID = int(i + (j-1)*number_cells[0])
	if k != 0:
		cellID += (k-1)*number_cells[0]*number_cells[1]
	assert cellID > 0, "CellID is negative"

	with open(os.path.join(path_to_output, f"heatpump_inject{idx}.vs"), "w") as file:
		file.write(str(cellID))

def write_SN_files(path_to_output:str, settings:Dict):

	xGrid, yGrid, zGrid = settings["grid"]["ncells"]
	cell_widths = settings["grid"]["size"]/np.array(settings["grid"]["ncells"])	# Cell width in metres
	cellXWidth, cellYWidth, cellZWidth = cell_widths
	_, yWidth, _ = settings["grid"]["size"]

	if not cellXWidth == cellZWidth:
		logging.error("Something with create_grid_unstructured.py is wrong")
	else:
		faceArea = cellXWidth*cellZWidth

	output_string_north = []
	output_string_north.append("CONNECTIONS " + str(xGrid*zGrid))
	output_string_south = []
	output_string_south.append("CONNECTIONS " + str(xGrid*zGrid))
	yloc_north = yWidth
	yloc_south = 0
	for k in range(0, zGrid):
		zloc = 0.5*cellZWidth + k*cellZWidth
		for i in range(0,xGrid):
			xloc = (i+0.5)*cellXWidth
			cellID_north = (xGrid*(yGrid-1)) + i+1 + k*xGrid*yGrid
			cellID_south = i+1 + k*xGrid*yGrid
			output_string_north.append("\n" + str(cellID_north)+"  "+str(xloc)+"  "+str(yloc_north)+"  "+str(zloc)+"  "+str(faceArea))
			output_string_south.append("\n" + str(cellID_south)+"  "+str(xloc)+"  "+str(yloc_south)+"  "+str(zloc)+"  "+str(faceArea))
	
	with open(str(path_to_output)+"/north.ex", "w") as file:
		file.writelines(output_string_north)
	with open(str(path_to_output)+"/south.ex", "w") as file:
		file.writelines(output_string_south)

def write_WE_files(path_to_output:str, settings:Dict):
	xGrid, yGrid, zGrid = settings["grid"]["ncells"]
	cell_widths = settings["grid"]["size"]/np.array(settings["grid"]["ncells"])	# Cell width in metres
	cellXWidth, cellYWidth, cellZWidth = cell_widths
	xWidth, _, _ = settings["grid"]["size"]

	if not cellYWidth == cellZWidth:
		logging.error("Something with create_grid_unstructured.py is wrong")
	else:
		faceArea = cellYWidth*cellZWidth

	output_string_east = []
	output_string_east.append("CONNECTIONS " + str(yGrid*zGrid))
	output_string_west = []
	output_string_west.append("CONNECTIONS " + str(yGrid*zGrid))
	xloc_east = xWidth
	xloc_west = 0
	for k in range(0, zGrid):
		zloc = 0.5*cellZWidth + k*cellZWidth
		for j in range(0,yGrid):
			yloc = (j+0.5)*cellYWidth
			cellID_east = (j+1)*xGrid + k*xGrid*yGrid
			cellID_west = j*xGrid + 1 + k*xGrid*yGrid
			output_string_east.append("\n" + str(cellID_east)+"  "+str(xloc_east)+"  "+str(yloc)+"  "+str(zloc)+"  "+str(faceArea))
			output_string_west.append("\n" + str(cellID_west)+"  "+str(xloc_west)+"  "+str(yloc)+"  "+str(zloc)+"  "+str(faceArea))
	
	with open(str(path_to_output)+"/east.ex", "w") as file:
		file.writelines(output_string_east)
	with open(str(path_to_output)+"/west.ex", "w") as file:
		file.writelines(output_string_west)

def _set_z_width_in_2d_case(settings:Dict):
	# If 2D case: set z-width to average of x and y width
	cellXWidth = settings["grid"]["size"][0]/np.array(settings["grid"]["ncells"][0])	# Cell width in metres
	cellYWidth = settings["grid"]["size"][1]/np.array(settings["grid"]["ncells"][1])
	cellZWidth = (cellXWidth+cellYWidth)/2 
	settings["grid"]["size"][2] = float(cellZWidth)

if __name__ == "__main__":
	cla = sys.argv
	assert len(cla) >= 2, "Please provide a path to the input folder"
	path_to_input = cla[1]
	path_to_output = "."

	settings = load_settings(path_to_input)
	if len(cla) > 3:
		path_to_output = cla[2]
		assert len(cla) >= 9, "Please provide a path to the output folder and the grid widths and number of cells per direction"
		grid_widths = [float(cla[3]), float(cla[4]), float(cla[5])]
		number_cells = [int(cla[6]), int(cla[7]), int(cla[8])]
		settings = change_grid_domain_size(settings, case="", grid_widths=grid_widths, number_cells=number_cells)

	if settings["general"]["dimensions"] == 2:
		_set_z_width_in_2d_case(settings)
	save_settings(settings, path_to_output)
	write_mesh_file(path_to_output, settings)
	write_SN_files(path_to_output, settings)
	write_WE_files(path_to_output, settings)
	write_loc_well_file(path_to_output, settings)