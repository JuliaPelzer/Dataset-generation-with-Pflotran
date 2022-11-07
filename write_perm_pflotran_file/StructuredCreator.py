# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:11:25 2020

@author: Fabian Böttcher
"""

import os
import numpy as np
from h5py import File
import matplotlib.pyplot as plt

def write_mesh_file(path_to_output:str, cell_widths, number_cells):
	# Cell width in metres
	cellXWidth, cellYWidth, cellZWidth = cell_widths
	# Number of grid cells
	xGrid, yGrid, zGrid = number_cells


	coords = np.zeros((xGrid*yGrid*zGrid,3))
	cellID = 0
	output_string = []
	output_string.append("CELLS "+str(xGrid*yGrid*zGrid))
	index = 0
	for k in range(0,zGrid):
		zloc = (k + 0.5)*cellZWidth
		for j in range(0,yGrid):
			yloc = (j + 0.5)*cellYWidth
			for i in range(0,xGrid):
				xloc = (i + 0.5)*cellXWidth
				# index = i + j*xGrid + k*yGrid*xGrid
				coords[index] = [xloc,yloc,zloc]
				volume = 1
				# cellID = (i+1) + j*xGrid + k*yGrid*xGrid
				cellID = index+1
				output_string.append("\n" + str(cellID)+"  "+str(xloc)+"  "+str(yloc)+"  "+str(zloc)+"  "+str(volume))
				index += 1

	with open(str(path_to_output)+"/mesh.uge", "w") as file:
		file.writelines(output_string)

def calc_connections(cell_widths, number_cells):
	# Cell width in metres
	cellXWidth, cellYWidth, cellZWidth = cell_widths
	# Number of grid cells
	xGrid, yGrid, zGrid = number_cells

	print("CONNECTIONS")
	# for k in range(0,zGrid):
	for j in range(0,yGrid):
		for i in range(0,xGrid):
			if (i < (xGrid - 1)):
				cellID_1 = (i+1) + j*yGrid
				cellID_2 = (i+1) + j*yGrid + 1
				xloc = cellXWidth + i*cellXWidth
				yloc = 0.5*cellYWidth + j*cellYWidth
				zloc = 0.5*cellZWidth
				faceArea = 1
				print(cellID_1, "  ", cellID_2, "  ", xloc, "  ", yloc, "  ", zloc, "  ",  faceArea)
			
			if (j < (yGrid - 1)):
				cellID_1 = (i+1) + j*yGrid
				cellID_2 = (i+1) + j*yGrid + xGrid
				xloc = 0.5*cellXWidth + i*cellXWidth
				yloc = cellYWidth + j*cellYWidth
				zloc = 0.5*cellZWidth
				faceArea = 1
				print(cellID_1, "  ", cellID_2, "  ", xloc, "  ", yloc, "  ", zloc, "  ",  faceArea)
	
	print("NorthBC")
	for i in range(0,xGrid):
		cellID = (xGrid*(yGrid-1)) + i + 1
		xloc = 0.5*cellXWidth + i*cellXWidth
		yloc = yWidth
		zloc = 0.5*cellZWidth
		faceArea = 1
		print(cellID, "  ", xloc, "  ", yloc, "  ", zloc, "  ",  faceArea)
		
	print("SouthBC")
	for i in range(0,xGrid):
		cellID = i + 1
		xloc = 0.5*cellXWidth + i*cellXWidth
		yloc = 0
		zloc = 0.5*cellZWidth
		faceArea = 1
		print(cellID, "  ", xloc, "  ", yloc, "  ", zloc, "  ",  faceArea)
		
	print("WestBC")
	for i in range(0,yGrid):
		cellID = 1 + i*xGrid
		xloc = 0
		yloc = 0.5*cellYWidth + i*cellYWidth
		zloc = 0.5*cellZWidth
		faceArea = 1
		print(cellID, "  ", xloc, "  ", yloc, "  ", zloc, "  ",  faceArea)
		
	print("EastBC")
	for i in range(0,yGrid):
		cellID = i*xGrid +xGrid
		xloc = xWidth
		yloc = 0.5*cellYWidth + i*cellYWidth
		zloc = 0.5*cellZWidth
		faceArea = 1
		print(cellID, "  ", xloc, "  ", yloc, "  ", zloc, "  ",  faceArea)


if __name__ == "__main__":
	grid_widths=[100, 750, 80]
	number_cells=[20, 150, 16]
	cell_widths = grid_widths/np.array(number_cells)
	path_to_output = "."

	write_mesh_file(path_to_output=path_to_output, cell_widths=cell_widths, number_cells=number_cells)
	calc_connections(cell_widths=cell_widths, number_cells=number_cells)




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
