import numpy as np

def write_mesh_file(path_to_output:str, cell_widths, number_cells, faceArea=1):
	cellXWidth, cellYWidth, cellZWidth = cell_widths
	xGrid, yGrid, zGrid = number_cells

	volume = 1
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



	with open(str(path_to_output)+"/mesh.uge", "w") as file:
		file.writelines(output_string)

def write_loc_well_file(path_to_output:str, cell_widths, number_cells, loc_hp):
	i,j,k = loc_hp/cell_widths
	cellID = int(i + (j-1)*number_cells[0] + (k-1)*number_cells[0]*number_cells[1])

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
	
	grid_widths=[100, 750, 80]	# Grid width in metres
	number_cells=[20, 150, 16]	# Number of grid cells
	loc_hp = [50, 120, 50]		# Location of the heatpump in metres
	path_to_output = "."

	faceArea=1
	cell_widths = grid_widths/np.array(number_cells)	# Cell width in metres
	write_mesh_file(path_to_output, cell_widths, number_cells, faceArea)
	write_loc_well_file(path_to_output, cell_widths, number_cells, loc_hp)
	write_SN_files(path_to_output, cell_widths, number_cells, grid_widths, faceArea)
	write_WE_files(path_to_output, cell_widths, number_cells, grid_widths, faceArea)