from datetime import datetime
import os

# create absolute path
dir_output = os.path.join(os.getcwd(), 'output/')
dir_vis = os.path.join(os.getcwd(), 'visualisation/')

# get current time for file names
now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M")

# --------------------------------------------
# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
pflotranvel0 = LegacyVTKReader(registrationName='pflotran-vel-0*', FileNames=[dir_output+'pflotran-vel-000.vtk', dir_output+'pflotran-vel-001.vtk', dir_output+'pflotran-vel-002.vtk', dir_output+'pflotran-vel-003.vtk', dir_output+'pflotran-vel-004.vtk', dir_output+'pflotran-vel-005.vtk', dir_output+'pflotran-vel-006.vtk', dir_output+'pflotran-vel-007.vtk', dir_output+'pflotran-vel-008.vtk', dir_output+'pflotran-vel-009.vtk', dir_output+'pflotran-vel-010.vtk', dir_output+'pflotran-vel-011.vtk', dir_output+'pflotran-vel-012.vtk', dir_output+'pflotran-vel-013.vtk', dir_output+'pflotran-vel-014.vtk', dir_output+'pflotran-vel-015.vtk', dir_output+'pflotran-vel-016.vtk', dir_output+'pflotran-vel-017.vtk', dir_output+'pflotran-vel-018.vtk', dir_output+'pflotran-vel-019.vtk', dir_output+'pflotran-vel-020.vtk', dir_output+'pflotran-vel-021.vtk', dir_output+'pflotran-vel-022.vtk', dir_output+'pflotran-vel-023.vtk', dir_output+'pflotran-vel-024.vtk', dir_output+'pflotran-vel-025.vtk', dir_output+'pflotran-vel-026.vtk', dir_output+'pflotran-vel-027.vtk', dir_output+'pflotran-vel-028.vtk', dir_output+'pflotran-vel-029.vtk', dir_output+'pflotran-vel-030.vtk', dir_output+'pflotran-vel-031.vtk', dir_output+'pflotran-vel-032.vtk', dir_output+'pflotran-vel-033.vtk', dir_output+'pflotran-vel-034.vtk', dir_output+'pflotran-vel-035.vtk', dir_output+'pflotran-vel-036.vtk', dir_output+'pflotran-vel-037.vtk', dir_output+'pflotran-vel-038.vtk', dir_output+'pflotran-vel-039.vtk', dir_output+'pflotran-vel-040.vtk', dir_output+'pflotran-vel-041.vtk', dir_output+'pflotran-vel-042.vtk', dir_output+'pflotran-vel-043.vtk', dir_output+'pflotran-vel-044.vtk', dir_output+'pflotran-vel-045.vtk', dir_output+'pflotran-vel-046.vtk', dir_output+'pflotran-vel-047.vtk', dir_output+'pflotran-vel-048.vtk', dir_output+'pflotran-vel-049.vtk', dir_output+'pflotran-vel-050.vtk'])

# get animation scene
animationScene1 = GetAnimationScene()
# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# create a new 'Python Calculator'
pythonCalculator1 = PythonCalculator(registrationName='PythonCalculator1', Input=pflotranvel0)
pythonCalculator1.ArrayAssociation = 'Cell Data'
# Properties modified on pythonCalculator1
pythonCalculator1.Expression = 'make_vector(Vlx,Vly,Vlz)'
pythonCalculator1.ArrayName = 'V'

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=pythonCalculator1)
cellDatatoPointData1.CellDataArraytoprocess = ['Material_ID', 'V', 'Vlx', 'Vly', 'Vlz']

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=cellDatatoPointData1)
clip1.ClipType = 'Plane'
clip1.Scalars = ['POINTS', 'V']
# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [50.0, 300.0, 40.0]

# show data in view
clip1Display = Show(clip1, renderView1)#, 'UnstructuredGridRepresentation')
# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
# set scalar coloring
ColorBy(clip1Display, ('POINTS', 'V', 'Magnitude'))
# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

animationScene1.GoToLast()

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# current camera placement for renderView1
renderView1.CameraPosition = [683.3800052725995, 300.0, 34.96236980003521]
renderView1.CameraFocalPoint = [49.999999999999986, 300.0, 40.0]
renderView1.CameraViewUp = [0.007953315272502374, 0.0, 0.9999683718879194]
renderView1.CameraParallelScale = 425.2077461397823
# save screenshot
SaveScreenshot(dir_vis +'V_field_vertical_cut_last_step'+current_time+'.png', renderView1, ImageResolution=[2852, 1580])

# Properties modified on animationScene1
animationScene1.AnimationTime = 1.0

# set scalar coloring
ColorBy(clip1Display, ('POINTS', 'V', 'Magnitude'))

# save screenshot
SaveScreenshot(dir_vis +'V_field_vertical_cut_first_step'+current_time+'.png', renderView1, ImageResolution=[1424, 790])


# set scalar coloring
ColorBy(clip1Display, ('POINTS', 'V', 'Magnitude'))

animationScene1.GoToLast()

# set active source
SetActiveSource(cellDatatoPointData1)

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# set scalar coloring
ColorBy(cellDatatoPointData1Display, ('POINTS', 'V', 'Magnitude'))

## hide data in view
#Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# rescale color and/or opacity maps used to exactly fit the current data range
cellDatatoPointData1Display.RescaleTransferFunctionToDataRange(False, True)

# current camera placement for renderView1
renderView1.CameraPosition = [43.800494036970036, 240.17476745676086, 496.9532069081173]
renderView1.CameraFocalPoint = [43.800494036970036, 240.17476745676086, 40.0]
renderView1.CameraViewUp = [-1.0, 2.220446049250313e-16, 0.0]
renderView1.CameraParallelScale = 306.75723300355935

# save screenshot
SaveScreenshot(dir_vis +'V_field_top_view_last_step'+current_time+'.png', renderView1, ImageResolution=[1424, 790])