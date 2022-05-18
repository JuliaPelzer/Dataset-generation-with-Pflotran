# vary grad(p)

#pflotran_in_file = open("pflotran.in", "r")
#content = pflotran_in_file.read()
#
#print(content.format)

# version Kyle
import os
import matplotlib.pyplot as plt
import random 
import logging
import sys

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
        return(f"Region object:\n"
               f"  Well_Number = {self.id}\n"
               f"  Point = {self.Point}\n"
               f"  X1 = {self.X1}\n"
               f"  Y1 = {self.Y1}\n"
               f"  Z1 = {self.Z1}\n"
               f"  X2 = {self.X2}\n"
               f"  Y2 = {self.Y2}\n"
               f"  Z2 = {self.Z2}\n"
               f"  n_Temps = {self.nTemps}")

def text_pflotran_input_file():
  SetwordsFirst = '''
  #Description: flow in a 3D area plus one heatpump - super super simplified for approach 2 try 1
  SIMULATION
    SIMULATION_TYPE SUBSURFACE
    PROCESS_MODELS
      SUBSURFACE_FLOW flow
        MODE TH
      /
    /
  END

  SUBSURFACE

  #=========================== times ============================================
  TIME
    FINAL_TIME 5.0 y
    INITIAL_TIMESTEP_SIZE 0.1 y
    MAXIMUM_TIMESTEP_SIZE 0.5 y
  /

  REFERENCE_PRESSURE 101325. #[Pa]

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

  #=========================== fluid properties =================================
  FLUID_PROPERTY
    DIFFUSION_COEFFICIENT 1.d-9 #[m^2/s] #checked
  END

  #=========================== material properties ==============================
  MATERIAL_PROPERTY gravel
    ID 1
    POROSITY 0.25d0                     #[-] #Größenordnung passt
    TORTUOSITY 0.5d0                    #[-] #Größenordnung passt
    ROCK_DENSITY 2.8d3                  #[kg/m^3] #checked
    SPECIFIC_HEAT 4.1d3                 #[J/(kg*K)?] #checked
    THERMAL_CONDUCTIVITY_DRY 0.7        #[W/(K*m)] #checked
    THERMAL_CONDUCTIVITY_WET 1.0
    LONGITUDINAL_DISPERSIVITY 3.1536d0  #[m] # checked
    PERMEABILITY                        #[m^2] #checked
      PERM_ISO 1.d-9 
    /
    CHARACTERISTIC_CURVES cc1
  END

  MATERIAL_PROPERTY gravel_inj
    ID 2
    POROSITY 0.25d0                     
    TORTUOSITY 0.5d0                    
    ROCK_DENSITY 2.8d3                  
    SPECIFIC_HEAT 4.1d3                 
    THERMAL_CONDUCTIVITY_DRY 0.7        
    THERMAL_CONDUCTIVITY_WET 1.0
    LONGITUDINAL_DISPERSIVITY 3.1536d0  
    PERMEABILITY                        
      PERM_ISO 1.d-9 
    /
    CHARACTERISTIC_CURVES cc1
  END

  MATERIAL_PROPERTY gravel_ext
    ID 3
    POROSITY 0.25d0                     
    TORTUOSITY 0.5d0                    
    ROCK_DENSITY 2.8d3                  
    SPECIFIC_HEAT 4.1d3                 
    THERMAL_CONDUCTIVITY_DRY 0.7        
    THERMAL_CONDUCTIVITY_WET 1.0
    LONGITUDINAL_DISPERSIVITY 3.1536d0  
    PERMEABILITY                       
      PERM_ISO 1.d-9 
    /
    CHARACTERISTIC_CURVES cc1
  END

  #=========================== characteristic curves ============================
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

  #=========================== discretization ===================================
  GRID
    TYPE structured
    NXYZ 20 150 16
    BOUNDS
      0.d0 0.d0 0.d0
      100.d0 750.d0 80.d0
    /
  END

  #=========================== regions ==========================================
  REGION all
    COORDINATES
      0.d0 0.d0 0.d0
      100.d0 750.d0 80.d0
    /
  /

  REGION south
    COORDINATES
      0.d0 0.d0 0.d0
      100.d0 0.d0 80.d0
    /
    FACE SOUTH
  /

  REGION north
    COORDINATES
      0.d0 750.d0 0.d0
      100.d0 750.d0 80.d0
    /
    FACE NORTH
  /

  REGION heatpump_extract1
    COORDINATE 50.d0 100.d0 50.d0
  /
  REGION heatpump_inject1
    COORDINATE 50.d0 120.d0 50.d0
  /

  #=========================== flow conditions ==================================
  FLOW_CONDITION initial
    TYPE
      LIQUID_PRESSURE HYDROSTATIC
      TEMPERATURE DIRICHLET
    /
    DATUM 50.d0 0.d0 80.d0
    GRADIENT
  '''

  SetwordsSecond = '''  
    /
    LIQUID_PRESSURE 101325.d0
    TEMPERATURE 10.6d0 ! [C]
  /

  FLOW_CONDITION extraction
    TYPE
      RATE SCALED_VOLUMETRIC_RATE VOLUME
      TEMPERATURE DIRICHLET
    /
    RATE -4.2 m^3/day
    TEMPERATURE -10.6d0
  /

  FLOW_CONDITION injection
    TYPE
      RATE SCALED_VOLUMETRIC_RATE VOLUME
      TEMPERATURE DIRICHLET
    /
    RATE 4.2 m^3/day
    TEMPERATURE 15.6d0
  /

  #=========================== condition couplers ===============================
  # initial condition
  INITIAL_CONDITION
    FLOW_CONDITION initial
    REGION all
  /

  # boundary conditions
  BOUNDARY_CONDITION
    FLOW_CONDITION initial
    REGION north
  /

  BOUNDARY_CONDITION
    FLOW_CONDITION initial
    REGION south
  /

  # heatpump source/sink
  SOURCE_SINK heatpump_extract1
    FLOW_CONDITION extraction
    REGION heatpump_extract1
  /
  SOURCE_SINK heatpump_inject1
    FLOW_CONDITION injection
    REGION heatpump_inject1
  /

  #=========================== stratigraphy couplers ============================
  STRATA
    REGION all
    MATERIAL gravel
  END

  # same but different material for hps to get a map with the hp locations alias Material_ID
  STRATA
    REGION heatpump_inject1
    MATERIAL gravel_inj
  END
  STRATA
    REGION heatpump_extract1
    MATERIAL gravel_ext
  END

  #=========================== output options ===================================
  OUTPUT
    SNAPSHOT_FILE
      #PERIODIC TIME 1. y BETWEEN 5. y AND 5. y
      TIMES y 5.
      #PERIODIC TIME 0.1 y
      FORMAT HDF5 #VTK
      PRINT_COLUMN_IDS
      VARIABLES
        LIQUID_PRESSURE
        TEMPERATURE
      /
    /
    VELOCITY_AT_CENTER
  /

  END_SUBSURFACE
  '''

  return SetwordsFirst, SetwordsSecond

if __name__ == "__main__":
      # predefine stuff
      SetwordsFirst, SetwordsSecond = text_pflotran_input_file()

      # parameters
      skip = 1

      # read input parameters
      cla_args = sys.argv

      # how much output should be printed
      logging.basicConfig(level = cla_args[1])
      #logging.info(f"input arguments: {cla_args}")

      # test varying pressure gradient, one heat pump
      pressure_gradient_x = 0
      pressure_gradient_y = cla_args[2]
      pressure_gradient_z = 0

      #logging.info(f"Running Simulation with Inputs: {pressure_gradient_y}")
      file = open("pflotran.in","w")
      file.write(SetwordsFirst)
      file.write("    PRESSURE ")
      file.write(str(pressure_gradient_x))
      file.write(" ")
      file.write(str(pressure_gradient_y))
      file.write(" ")
      file.write(str(pressure_gradient_z))
      file.write(SetwordsSecond)
      file.close()
      logging.info(f"Pressure Input: {pressure_gradient_x}, {pressure_gradient_y}, {pressure_gradient_z}")
      #os.system("pflotran pflotran.in > log.pflotran")
      #os.system("cp pflotran.in results/pflotran-withFlow-" + str(i) + ".in")
      #os.system("cp pflotran-004.vtk results/pflotran-withFlow-" + str(i) +".vtk")
      #os.system("cp pflotran-vel-004.vtk results/pflotran-withFlow-vel-" + str(i) + ".vtk")
      #with open('results/cell.dat', 'r') as f1, open('results/pflotran-withFlow-'+str(i) +'.vtk', 'r') as f2, open('results/pflotran-withFlow-vel-'+str(i) + '.vtk', 'r') as f3, open('results/pflotran-withFlow-new-'+ str(i) + '.vtk', 'w') as newVTK, open('results/pflotran-withFlow-new-vel-'+ str(i) + '.vtk', 'w') as newVEL:
      #    #input2 = f.read()
      #    lines1 = f1.readlines()
      #    lines2 = f2.readlines()
      #    lines3 = f3.readlines()
      #    newVTK.writelines(lines1[:])
      #    newVTK.writelines(lines2[5:])
      #    newVEL.writelines(lines1[:])
      #    newVEL.writelines(lines3[5:])