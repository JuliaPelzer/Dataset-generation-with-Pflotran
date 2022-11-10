from xlrd import open_workbook
import os
import matplotlib.pyplot as plt
import random 

class Region(object):
    def __init__(self, id, Point, X1, Y1, Z1, X2, Y2, Z2, nTemps):
        self.id = id
        self.Point = Point
        self.X1 = X1
        self.Y1 = Y1
        self.Z1 = Z1
        self.X2 = X2
        self.Y2 = Y2
        self.Z2 = Z2
        self.nTemps = nTemps

    def __str__(self):
        return("Region object:\n"
               "  Well_Number = {0}\n"
               "  Point = {1}\n"
               "  X1 = {2}\n"
               "  Y1 = {3}\n"
               "  Z1 = {4}\n"
               "  X2 = {5}\n"
               "  Y2 = {6}\n"
               "  Z2 = {7}\n"
               "  n_Temps = {8}"
               .format(self.id, self.Point, self.X1,
                       self.Y1, self.Z1, self.X2, self.Y2, self.Z2, self.nTemps))
                       
SetwordsFirst = '''
#Description: 3D toy problem for richards equation

SIMULATION
  SIMULATION_TYPE SUBSURFACE
  PROCESS_MODELS
    SUBSURFACE_FLOW flow
      MODE TH
    /
  /
END

SUBSURFACE

#=========================== solver options ===================================

#NEWTON_SOLVER FLOW
#  ITOL_UPDATE 1.d0     ! Convergences with max change in pressure is 1 Pa.
#END
NUMERICAL_METHODS FLOW 
  NEWTON_SOLVER 
    ANALYTICAL_JACOBIAN 
    ITOL_UPDATE 1.d0 
    RTOL 1.d-3 
  / 
  LINEAR_SOLVER 
    SOLVER ITERATIVE 
  / 
END

#=========================== flow mode ========================================

#=========================== discretization ===================================
GRID
TYPE UNSTRUCTURED_EXPLICIT mesh.uge
MAX_CELLS_SHARING_A_VERTEX 70
END


#=========================== fluid properties =================================
FLUID_PROPERTY
  DIFFUSION_COEFFICIENT 1.d-9
/

DATASET perm
  HDF5_DATASET_NAME Permeability
  FILENAME permeability.h5
END


#==================== material properties =====================

MATERIAL_PROPERTY gravel
  ID 1
  POROSITY 0.25d0
  TORTUOSITY 0.5d0
  ROCK_DENSITY 2.8E3
  SPECIFIC_HEAT 1E3
  THERMAL_CONDUCTIVITY_DRY 0.5
  THERMAL_CONDUCTIVITY_WET 0.5
  LONGITUDINAL_DISPERSIVITY 3.1536d0
  PERMEABILITY
    DATASET perm
    #PERM_ISO 1.d-9
  /
  CHARACTERISTIC_CURVES cc1
/

#==================== characteristic curves ===================

CHARACTERISTIC_CURVES cc1
  SATURATION_FUNCTION VAN_GENUCHTEN
    ALPHA  1.d-4
    M 0.5d0
    LIQUID_RESIDUAL_SATURATION 0.1d0
  /
  PERMEABILITY_FUNCTION MUALEM_VG_LIQ
    M 0.5d0
    LIQUID_RESIDUAL_SATURATION 0.1d0
  /
END

#=========================== output options ===================================
OUTPUT
  SNAPSHOT_FILE
    #PERIODIC TIME 40. d BETWEEN 0. d AND 400. d
    PERIODIC TIME 180. d BETWEEN 0. d AND 1000. d
    #FORMAT TECPLOT BLOCK
    FORMAT VTK
    PRINT_COLUMN_IDS
    VARIABLES
      LIQUID_PRESSURE
      TEMPERATURE
      LIQUID_ENERGY
      PERMEABILITY
    /
  VELOCITY_AT_CENTER
  /
  OBSERVATION_FILE
    PERIODIC TIME 180. d
    VARIABLES
      TEMPERATURE
      LIQUID_ENERGY
    /
  /
END

#=========================== times ============================================
TIME
  FINAL_TIME 720.d0 d
  MAXIMUM_TIMESTEP_SIZE 40.d3 d
  #FINAL_TIME 8760.d0 d
  #INITIAL_TIMESTEP_SIZE 10.d1 d
  #MAXIMUM_TIMESTEP_SIZE 10.d1 d
  #MINIMUM_TIMESTEP_SIZE 10.d1 d
/

REFERENCE_PRESSURE 101325.

#=========================== regions ==========================================

REGION all
  COORDINATES
    0.d0 0.d0 0.d0
    64.d0 64.d0 1.d0
  /
/

REGION south
FILE south.ex
END

REGION north
FILE north.ex
END

REGION east
FILE east.ex
END

REGION west
FILE west.ex
END

REGION well
FILE well.vs
END

REGION obs
FILE observationPoints.txt
END


#=========================== observation points ===============================

OBSERVATION
  REGION obs
/


#=========================== flow conditions ==================================
FLOW_CONDITION initial
  TYPE
    PRESSURE HYDROSTATIC
    TEMPERATURE DIRICHLET
  /
  DATUM 0.d0 0.d0 10.d0
  GRADIENT
'''

SetwordsSecond = '''  
  /
  PRESSURE 101325.d0
  TEMPERATURE 10.d0
END

FLOW_CONDITION injection_1 
  TYPE 
    RATE SCALED_MASS_RATE VOLUME
    TEMPERATURE dirichlet 
    #ENERGY_RATE ENERGY_RATE NEIGHBOR_PERM
  / 
  RATE LIST 
    TIME_UNITS d 
    DATA_UNITS kg/s
    INTERPOLATION LINEAR
    #time  #massrate
'''
#    0.d0 0.01d0 
#    40.d0 0.01d0
#    80.d0 0.01d0
#    120.d0 0.01d0
#    320.d0 0.01d0

SetwordsThird = '''
/
#ENERGY_RATE 200 W
  TEMPERATURE LIST 
    TIME_UNITS d 
    DATA_UNITS C 
    INTERPOLATION LINEAR
    #time  #temperature  
    0.d0 15.0
    40.d0 15
    80.d0 15
    120.d0 15
    160.d0 15
/
END


#=========================== condition couplers ===============================
# initial condition
INITIAL_CONDITION all
  FLOW_CONDITION initial
  REGION all
END

BOUNDARY_CONDITION inflow
  FLOW_CONDITION initial
  REGION west
END

BOUNDARY_CONDITION outflow
  FLOW_CONDITION initial
  REGION east
END

BOUNDARY_CONDITION outflow
  FLOW_CONDITION initial
  REGION north
END

BOUNDARY_CONDITION outflow
  FLOW_CONDITION initial
  REGION south
END

SOURCE_SINK 
  FLOW_CONDITION injection_1
  REGION well
END


#=========================== stratigraphy couplers ============================
STRATA
  REGION all
  MATERIAL gravel
END

HDF5_READ_GROUP_SIZE 1
END_SUBSURFACE

#=========================== Debug ============================
DEBUG
  PRINT_SOLUTION
  PRINT_RESIDUAL
  PRINT_JACOBIAN
  FORMAT ASCII
  PRINT_WAYPOINTS
  PRINT_COUPLERS
END
'''

wb = open_workbook('testing.xls')
i = 0
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols

    items = []

    rows = []
    for row in range(0, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                values.append(value)
        item = Region(*values)
        items.append(item)


p1 = []
p2 = []
p3 = []

skip = 1

nRunsStart = 150
nRunsEnd = 175

for i in range(nRunsStart,nRunsEnd):
	if (not skip == 0):
		rand1 = random.uniform(-3, -1)
		rand2 = random.uniform(-2, 2)
		p1.append(rand1/8000)
		p2.append(rand2/8000)
		p3.append(0)
    	#print("Accessing one single value (eg. DSPName): {0}".format(item.Point))
		i = i + 1
		skip += 1
	skip += 1
    
print ("P1: ", p1)
print ("P2: ", p2)

TS = 20		# Time step length for pflotran input temperatures

massFlow = 0
bcCounter = -1
for i in range(nRunsStart,nRunsEnd):
	bcCounter += 1
	os.system("rm -r permeability.h5")
	os.system("python3 initial_gauss_perm_creator.py")
	if (i >= nRunsStart):
		for j in range(0,2):
			print("Running Simulation J: ", j, " - With Inputs: ", i)
			print("bcCounter: ", bcCounter)
			if (j == 0):
				massFlow = 0
			else:
				massFlow = 0.05
				
			file = open("pflotran.in","w")
			file.write(SetwordsFirst)
			file.write("    PRESSURE ")
			file.write(str(p1[bcCounter]))
			file.write(" ")
			file.write(str(p2[bcCounter]))
			file.write(" ")
			file.write(str(p3[bcCounter]))
			file.write(SetwordsSecond)
			file.write("    0.d0 " + str(massFlow) + "d0" + "\n")
			file.write("    40.d0 " + str(massFlow) + "d0" + "\n")
			file.write("    80.d0 " + str(massFlow) + "d0" + "\n")
			file.write("    120.d0 " + str(massFlow) + "d0" + "\n")
			file.write("    320.d0 " + str(massFlow) + "d0")
			file.write(SetwordsThird)
			file.close()
			print("Pressure Input: ", p1[i-nRunsStart], " , ", p2[i-nRunsStart])
			os.system("pflotran pflotran.in > log.pflotran")
			#input()
			if (j == 0):
				os.system("cp pflotran.in results/pflotran-noFlow-" + str(i) + ".in")
				os.system("cp pflotran-004.vtk results/pflotran-noFlow-" + str(i) +".vtk")
				os.system("cp pflotran-vel-004.vtk results/pflotran-noFlow-vel-" + str(i) + ".vtk")
				with open('results/cell.dat', 'r') as f1, open('results/pflotran-noFlow-'+str(i) +'.vtk', 'r') as f2, open('results/pflotran-noFlow-vel-'+str(i) + '.vtk', 'r') as f3, open('results/pflotran-noFlow-new-'+ str(i) + '.vtk', 'w') as newVTK, open('results/pflotran-noFlow-new-vel-'+ str(i) + '.vtk', 'w') as newVEL:
					#input2 = f.read()
					lines1 = f1.readlines()
					lines2 = f2.readlines()
					lines3 = f3.readlines()
					newVTK.writelines(lines1[:])
					newVTK.writelines(lines2[5:])
					newVEL.writelines(lines1[:])
					newVEL.writelines(lines3[5:])
			else:
				os.system("cp pflotran.in results/pflotran-withFlow-" + str(i) + ".in")
				os.system("cp pflotran-004.vtk results/pflotran-withFlow-" + str(i) +".vtk")
				os.system("cp pflotran-vel-004.vtk results/pflotran-withFlow-vel-" + str(i) + ".vtk")
				with open('results/cell.dat', 'r') as f1, open('results/pflotran-withFlow-'+str(i) +'.vtk', 'r') as f2, open('results/pflotran-withFlow-vel-'+str(i) + '.vtk', 'r') as f3, open('results/pflotran-withFlow-new-'+ str(i) + '.vtk', 'w') as newVTK, open('results/pflotran-withFlow-new-vel-'+ str(i) + '.vtk', 'w') as newVEL:
					#input2 = f.read()
					lines1 = f1.readlines()
					lines2 = f2.readlines()
					lines3 = f3.readlines()
					newVTK.writelines(lines1[:])
					newVTK.writelines(lines2[5:])
					newVEL.writelines(lines1[:])
					newVEL.writelines(lines3[5:])
				

