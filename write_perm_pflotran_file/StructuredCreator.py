# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:11:25 2020

@author: Fabian Böttcher
"""

import os
import numpy as np
from h5py import File
import matplotlib.pyplot as plt

def write_mesh_and_loc_hp_files(path_to_output:str, cell_widths, number_cells):
	cellXWidth, cellYWidth, cellZWidth = cell_widths
	xGrid, yGrid, zGrid = number_cells

	volume = 1
	output_string = []
	output_string.append("CELLS "+str(xGrid*yGrid*zGrid))
	cellID = 1

	for k in range(0,zGrid):
		zloc = (k + 0.5)*cellZWidth
		for j in range(0,yGrid):
			yloc = (j + 0.5)*cellYWidth
			for i in range(0,xGrid):
				xloc = (i + 0.5)*cellXWidth
				output_string.append("\n" + str(cellID)+"  "+str(xloc)+"  "+str(yloc)+"  "+str(zloc)+"  "+str(volume))
				# check for location of heat pump
				# if [52.5,122.5,52.5] == [xloc, yloc, zloc]:
				# 	print("CALC", cellID)
				cellID += 1

	with open(str(path_to_output)+"/mesh.uge", "w") as file:
		file.writelines(output_string)

def write_loc_well_file(path_to_output:str, cell_widths, number_cells, loc_well):
	i,j,k = loc_hp/cell_widths
	cellID = int(i+1 + j*number_cells[0] + k*number_cells[0]*number_cells[1])

	with open(str(path_to_output)+"/heatpump_inject1.vs", "w") as file:
		file.write(str(cellID))

def write_SN_files(path_to_output:str, cell_widths, number_cells, grid_witdhs, faceArea=1):
	cellXWidth, _, cellZWidth = cell_widths
	xGrid, yGrid, zGrid = number_cells
	_, yWidth, _ = grid_witdhs

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
	
def write_WE_files(path_to_output:str, cell_widths, number_cells, grid_witdhs, faceArea=1):
	_, cellYWidth, cellZWidth = cell_widths
	xGrid, yGrid, zGrid = number_cells
	xWidth, _, _ = grid_witdhs

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
		
if __name__ == "__main__":
	
	path_to_output = "."
	grid_widths=[100, 750, 80]	# Grid width in metres
	number_cells=[20, 150, 16]	# Number of grid cells
	cell_widths = grid_widths/np.array(number_cells)	# Cell width in metres
	loc_hp = [50, 120, 50]		# Location of the heatpump in metres
	write_mesh_and_loc_hp_files(path_to_output, cell_widths, number_cells)
	write_loc_well_file(path_to_output, cell_widths, number_cells, loc_hp)

	faceArea=1
	write_SN_files(path_to_output, cell_widths, number_cells, grid_widths, faceArea)
	write_WE_files(path_to_output, cell_widths, number_cells, grid_widths, faceArea)




# def initial_permeability_variation(x, y):
#     """calculate example permeability field for calibration testing"""
#     var_val = x*0 + 1e-9 + y*0
#     return var_val
    
# #perm_grid = initial_permeability_variation(coords[:,0], coords[:,1])

# #for i in range(0,xGrid*yGrid):
# 	#print(coords[i,0], coords[i,1], coords[i,2])



# # cell_centers_path = "grid_cell_centers.dat"
# # cell_center_coords = np.loadtxt(cell_centers_path)
# #perm_grid = initial_permeability_variation(cell_center_coords[:, 0], cell_center_coords[:, 1])
# scale_factor = 2
# #perm_grid_log = np.log(perm_grid)
# #perm_grid = np.exp(perm_grid_log.mean() + ((perm_grid_log - perm_grid_log.mean()) * scale_factor))

# #print(cell_center_coords)
# #plt.scatter(cell_center_coords[:, 0], cell_center_coords[:, 1], c=perm_grid)
# #plt.show()

# iarray = [] #np.arange(1, cell_center_coords.shape[0] + 1, 1)
# perm_grid = []
# for i in range(xGrid*yGrid):
# 	iarray.append(i+1)
# 	perm_grid.append(0.000000001)


# filename = 'permeability.h5'

# print(iarray)
# print(perm_grid)

# print('setting cell indices....')
# # add cell ids to file
# dataset_name = 'Cell Ids'
# h5file = File(filename, mode='w')
# h5dset = h5file.create_dataset(dataset_name, data=iarray)
# # add permeability to file
# dataset_name = 'Permeability'
# h5dset = h5file.create_dataset(dataset_name, data=iarray)
# h5file.close()

# # debug output
# print('min: %e' % np.max(perm_grid))
# print('max: %e' % np.min(perm_grid))
# print('ave: %e' % np.mean(perm_grid))
    

# '''	
# ###########################################
# # variables for setup #####################
# ###########################################

# #cell_centers_path = "../PFLOTRAN/test_model/grid_cell_centers.dat"

# # mean initial permeability
# const_permeability = 1e-8

# #scaling factor to increase permeability field differences
# scale_factor = 2
# plot=False

# # permeability dataset file name
# # has to match the link in the PFLOTRAN input file
# filename = '../PFLOTRAN/permeability.h5'
