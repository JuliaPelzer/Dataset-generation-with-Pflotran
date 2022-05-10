from datetime import datetime
import os
import sys

# create absolute path
cla_args = sys.argv
dir_output = os.path.join(os.getcwd(), cla_args[1])
dir_vis = os.path.join(os.getcwd(), cla_args[2])

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
fileNames=[f"{dir_output}/pflotran-00{number}.vtk" for number in range(0,10)]
fileNames.extend([f"{dir_output}/pflotran-0{number}.vtk" for number in range(10,51)])
pflotran0 = LegacyVTKReader(registrationName='pflotran-0*', FileNames=fileNames)

# get animation scene
animationScene1 = GetAnimationScene()
# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=pflotran0)
clip1.ClipType = 'Plane'
#clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['CELLS', 'Temperature']
clip1.Value = 10.600000381469727
# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [50.0, 300.0, 40.0]

# hide data in view
Hide(pflotran0, renderView1)

animationScene1.GoToNext()

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=clip1)
cellDatatoPointData1.CellDataArraytoprocess = ['Material_ID', 'Temperature']

# create a new 'Temporal Interpolator'
temporalInterpolator1 = TemporalInterpolator(registrationName='TemporalInterpolator1', Input=cellDatatoPointData1)

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# Properties modified on temporalInterpolator1
#temporalInterpolator1.ResampleFactor =6

# update the view to ensure updated data information
renderView1.Update()

# current camera placement for renderView1
renderView1.CameraPosition = [378.5674071009585, 262.9278771745436, 163.0554144827319]
renderView1.CameraFocalPoint = [25.391372165226173, 258.15793863260865, 40.50068071468933]
renderView1.CameraViewUp = [-0.32785611688787264, 0.002176734790805271, 0.9447251602687716]
renderView1.CameraParallelScale = 303.6856927812043

# save animation
SaveAnimation(dir_vis +'/test_video'+current_time+'.avi', renderView1, ImageResolution=[1528, 788],
    FrameRate=24,
    FrameWindow=[0, 300])
