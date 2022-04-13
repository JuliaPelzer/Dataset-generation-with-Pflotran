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

# show data in view
pflotranvel0Display = Show(pflotranvel0, renderView1)#, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'Vlx'
vlxLUT = GetColorTransferFunction('Vlx')
vlxLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.878906683738906e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]
vlxLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'Vlx'
vlxPWF = GetOpacityTransferFunction('Vlx')
vlxPWF.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]
vlxPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
pflotranvel0Display.Representation = 'Surface'
pflotranvel0Display.ColorArrayName = ['CELLS', 'Vlx']
pflotranvel0Display.LookupTable = vlxLUT
#pflotranvel0Display.SelectTCoordArray = 'None'
#pflotranvel0Display.SelectNormalArray = 'None'
#pflotranvel0Display.SelectTangentArray = 'None'
pflotranvel0Display.OSPRayScaleFunction = 'PiecewiseFunction'
pflotranvel0Display.SelectOrientationVectors = 'None'
pflotranvel0Display.ScaleFactor = 60.0
pflotranvel0Display.SelectScaleArray = 'Vlx'
pflotranvel0Display.GlyphType = 'Arrow'
pflotranvel0Display.GlyphTableIndexArray = 'Vlx'
pflotranvel0Display.GaussianRadius = 3.0
pflotranvel0Display.SetScaleArray = [None, '']
pflotranvel0Display.ScaleTransferFunction = 'PiecewiseFunction'
pflotranvel0Display.OpacityArray = [None, '']
pflotranvel0Display.OpacityTransferFunction = 'PiecewiseFunction'
pflotranvel0Display.DataAxesGrid = 'GridAxesRepresentation'
pflotranvel0Display.PolarAxes = 'PolarAxesRepresentation'
pflotranvel0Display.ScalarOpacityFunction = vlxPWF
pflotranvel0Display.ScalarOpacityUnitDistance = 7.274018321161722
#pflotranvel0Display.OpacityArrayName = ['CELLS', 'Vlx']

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
pflotranvel0Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Python Calculator'
pythonCalculator1 = PythonCalculator(registrationName='PythonCalculator1', Input=pflotranvel0)
pythonCalculator1.Expression = ''
pythonCalculator1.ArrayAssociation = 'Cell Data'

# Properties modified on pythonCalculator1
pythonCalculator1.Expression = 'make_vector(Vlx,Vly,Vlz)'
pythonCalculator1.ArrayName = 'V'

# show data in view
pythonCalculator1Display = Show(pythonCalculator1, renderView1)#, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
pythonCalculator1Display.Representation = 'Surface'
pythonCalculator1Display.ColorArrayName = ['CELLS', 'Vlx']
pythonCalculator1Display.LookupTable = vlxLUT
#pythonCalculator1Display.SelectTCoordArray = 'None'
#pythonCalculator1Display.SelectNormalArray = 'None'
#pythonCalculator1Display.SelectTangentArray = 'None'
pythonCalculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
pythonCalculator1Display.SelectOrientationVectors = 'None'
pythonCalculator1Display.ScaleFactor = 60.0
pythonCalculator1Display.SelectScaleArray = 'Vlx'
pythonCalculator1Display.GlyphType = 'Arrow'
pythonCalculator1Display.GlyphTableIndexArray = 'Vlx'
pythonCalculator1Display.GaussianRadius = 3.0
pythonCalculator1Display.SetScaleArray = [None, '']
pythonCalculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
pythonCalculator1Display.OpacityArray = [None, '']
pythonCalculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
pythonCalculator1Display.DataAxesGrid = 'GridAxesRepresentation'
pythonCalculator1Display.PolarAxes = 'PolarAxesRepresentation'
pythonCalculator1Display.ScalarOpacityFunction = vlxPWF
pythonCalculator1Display.ScalarOpacityUnitDistance = 7.274018321161722
#pythonCalculator1Display.OpacityArrayName = ['CELLS', 'Vlx']

# hide data in view
Hide(pflotranvel0, renderView1)

# show color bar/color legend
pythonCalculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(pythonCalculator1Display, ('CELLS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
pythonCalculator1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
pythonCalculator1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'V'
vLUT = GetColorTransferFunction('V')
vLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.878906683738906e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]
vLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'V'
vPWF = GetOpacityTransferFunction('V')
vPWF.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]
vPWF.ScalarRangeInitialized = 1

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=pythonCalculator1)
cellDatatoPointData1.CellDataArraytoprocess = ['Material_ID', 'V', 'Vlx', 'Vly', 'Vlz']

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
cellDatatoPointData1Display.Representation = 'Surface'
cellDatatoPointData1Display.ColorArrayName = ['POINTS', 'Vlx']
cellDatatoPointData1Display.LookupTable = vlxLUT
#cellDatatoPointData1Display.SelectTCoordArray = 'None'
#cellDatatoPointData1Display.SelectNormalArray = 'None'
#cellDatatoPointData1Display.SelectTangentArray = 'None'
cellDatatoPointData1Display.OSPRayScaleArray = 'Vlx'
cellDatatoPointData1Display.OSPRayScaleFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.SelectOrientationVectors = 'None'
cellDatatoPointData1Display.ScaleFactor = 60.0
cellDatatoPointData1Display.SelectScaleArray = 'Vlx'
cellDatatoPointData1Display.GlyphType = 'Arrow'
cellDatatoPointData1Display.GlyphTableIndexArray = 'Vlx'
cellDatatoPointData1Display.GaussianRadius = 3.0
cellDatatoPointData1Display.SetScaleArray = ['POINTS', 'Vlx']
cellDatatoPointData1Display.ScaleTransferFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.OpacityArray = ['POINTS', 'Vlx']
cellDatatoPointData1Display.OpacityTransferFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.DataAxesGrid = 'GridAxesRepresentation'
cellDatatoPointData1Display.PolarAxes = 'PolarAxesRepresentation'
cellDatatoPointData1Display.ScalarOpacityFunction = vlxPWF
cellDatatoPointData1Display.ScalarOpacityUnitDistance = 7.274018321161722
#cellDatatoPointData1Display.OpacityArrayName = ['POINTS', 'Vlx']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
cellDatatoPointData1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
cellDatatoPointData1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(pythonCalculator1, renderView1)

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=cellDatatoPointData1)
slice1.SliceType = 'Plane'
#slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [50.0, 300.0, 40.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
#slice1.HyperTreeGridSlicer.Origin = [50.0, 300.0, 40.0]

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [50.0, 300.0, 50.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1)#, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'Vlx']
slice1Display.LookupTable = vlxLUT
#slice1Display.SelectTCoordArray = 'None'
#slice1Display.SelectNormalArray = 'None'
#slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'Vlx'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = 60.0
slice1Display.SelectScaleArray = 'Vlx'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'Vlx'
slice1Display.GaussianRadius = 3.0
slice1Display.SetScaleArray = ['POINTS', 'Vlx']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'Vlx']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=slice1,
    SeedType='High Resolution Line Source')
streamTracer1.Vectors = ['POINTS', 'V']
streamTracer1.MaximumStreamlineLength = 600.0

# init the 'Line' selected for 'SeedType'
streamTracer1.SeedType.Point1 = [0.0, 0.0, 50.0]
streamTracer1.SeedType.Point2 = [100.0, 600.0, 50.0]

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=streamTracer1.SeedType)

# destroy streamTracer1
Delete(streamTracer1)
del streamTracer1

# set active source
SetActiveSource(cellDatatoPointData1)

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=cellDatatoPointData1,
    SeedType='High Resolution Line Source')
streamTracer1.Vectors = ['POINTS', 'V']
streamTracer1.MaximumStreamlineLength = 600.0

# init the 'Line' selected for 'SeedType'
streamTracer1.SeedType.Point2 = [100.0, 600.0, 80.0]

# Properties modified on streamTracer1
streamTracer1.MaximumStreamlineLength = 180.0

# show data in view
streamTracer1Display = Show(streamTracer1, renderView1)#, 'GeometryRepresentation')

# trace defaults for the display properties.
streamTracer1Display.Representation = 'Surface'
streamTracer1Display.ColorArrayName = ['POINTS', 'Vlx']
streamTracer1Display.LookupTable = vlxLUT
#streamTracer1Display.SelectTCoordArray = 'None'
#streamTracer1Display.SelectNormalArray = 'None'
#streamTracer1Display.SelectTangentArray = 'None'
streamTracer1Display.OSPRayScaleArray = 'Vlx'
streamTracer1Display.OSPRayScaleFunction = 'PiecewiseFunction'
streamTracer1Display.SelectOrientationVectors = 'Normals'
streamTracer1Display.ScaleFactor = 9.864920270442964
streamTracer1Display.SelectScaleArray = 'Vlx'
streamTracer1Display.GlyphType = 'Arrow'
streamTracer1Display.GlyphTableIndexArray = 'Vlx'
streamTracer1Display.GaussianRadius = 0.49324601352214814
streamTracer1Display.SetScaleArray = ['POINTS', 'Vlx']
streamTracer1Display.ScaleTransferFunction = 'PiecewiseFunction'
streamTracer1Display.OpacityArray = ['POINTS', 'Vlx']
streamTracer1Display.OpacityTransferFunction = 'PiecewiseFunction'
streamTracer1Display.DataAxesGrid = 'GridAxesRepresentation'
streamTracer1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
streamTracer1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
streamTracer1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
streamTracer1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=streamTracer1.SeedType)

# reset view to fit data
renderView1.ResetCamera()

# reset view to fit data
renderView1.ResetCamera()

# set active source
SetActiveSource(streamTracer1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=streamTracer1.SeedType)

# set scalar coloring
ColorBy(streamTracer1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
streamTracer1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
streamTracer1Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=streamTracer1.SeedType)

# set active source
SetActiveSource(cellDatatoPointData1)

# set scalar coloring
ColorBy(cellDatatoPointData1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
cellDatatoPointData1Display.RescaleTransferFunctionToDataRange(True, False)

# set active source
SetActiveSource(slice1)

# set active source
SetActiveSource(streamTracer1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=streamTracer1.SeedType)

animationScene1.GoToLast()

animationScene1.GoToLast()

# rescale color and/or opacity maps used to exactly fit the current data range
streamTracer1Display.RescaleTransferFunctionToDataRange(False, True)

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
#layout1.SetSize(1528, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [225.0072180445995, 228.80741721980357, 79.18658715619807]
renderView1.CameraFocalPoint = [52.23961808329736, 222.39922819734466, 54.28126993474887]
renderView1.CameraViewUp = [-0.14252356605637787, -0.004273409936834669, 0.9897821836576395]
renderView1.CameraParallelScale = 304.13816320408245

# save screenshot
SaveScreenshot(dir_vis +'streamlines_V_horizontal_cut'+current_time+'.png', renderView1, ImageResolution=[1528, 790])

# set active source
SetActiveSource(cellDatatoPointData1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=streamTracer1.SeedType)

# hide data in view
Hide(streamTracer1, renderView1)

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# destroy streamTracer1
Delete(streamTracer1)
del streamTracer1

# set active source
SetActiveSource(slice1)

# set active source
SetActiveSource(cellDatatoPointData1)

# hide data in view
Hide(slice1, renderView1)

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# destroy slice1
Delete(slice1)
del slice1

# rescale color and/or opacity maps used to exactly fit the current data range
cellDatatoPointData1Display.RescaleTransferFunctionToDataRange(False, True)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=cellDatatoPointData1)
slice1.SliceType = 'Plane'
#slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [50.0, 300.0, 40.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
#slice1.HyperTreeGridSlicer.Origin = [50.0, 300.0, 40.0]

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# show data in view
slice1Display = Show(slice1, renderView1)#, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'Vlx']
slice1Display.LookupTable = vlxLUT
#slice1Display.SelectTCoordArray = 'None'
#slice1Display.SelectNormalArray = 'None'
#slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'Vlx'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = 60.0
slice1Display.SelectScaleArray = 'Vlx'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'Vlx'
slice1Display.GaussianRadius = 3.0
slice1Display.SetScaleArray = ['POINTS', 'Vlx']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'Vlx']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [-97.45648956298828, 0.0, 0.5, 0.0, 95.1446533203125, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [-97.45648956298828, 0.0, 0.5, 0.0, 95.1446533203125, 1.0, 0.5, 0.0]

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# layout/tab size in pixels
#layout1.SetSize(1528, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [302.82801551215385, 203.51197878062527, 218.871260766039]
renderView1.CameraFocalPoint = [43.94146676307447, 222.47915608056823, 50.43314616070595]
renderView1.CameraViewUp = [-0.5457407216438945, -0.0077824733080826165, 0.8379179541272584]
renderView1.CameraParallelScale = 304.13816320408245

# save screenshot
SaveScreenshot(dir_vis +'V_field_vertical_cut'+current_time+'.png', renderView1, ImageResolution=[1528, 790])

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=slice1,
    SeedType='High Resolution Line Source')
streamTracer1.Vectors = ['POINTS', 'V']
streamTracer1.MaximumStreamlineLength = 600.0

# init the 'Line' selected for 'SeedType'
streamTracer1.SeedType.Point1 = [50.0, 0.0, 0.0]
streamTracer1.SeedType.Point2 = [50.0, 600.0, 80.0]

# Properties modified on streamTracer1
streamTracer1.MaximumStreamlineLength = 100.0

# show data in view
streamTracer1Display = Show(streamTracer1, renderView1)#, 'GeometryRepresentation')

# trace defaults for the display properties.
streamTracer1Display.Representation = 'Surface'
streamTracer1Display.ColorArrayName = ['POINTS', 'Vlx']
streamTracer1Display.LookupTable = vlxLUT
#streamTracer1Display.SelectTCoordArray = 'None'
#streamTracer1Display.SelectNormalArray = 'None'
#streamTracer1Display.SelectTangentArray = 'None'
streamTracer1Display.OSPRayScaleArray = 'Vlx'
streamTracer1Display.OSPRayScaleFunction = 'PiecewiseFunction'
streamTracer1Display.SelectOrientationVectors = 'Normals'
streamTracer1Display.ScaleFactor = 19.772200775146487
streamTracer1Display.SelectScaleArray = 'Vlx'
streamTracer1Display.GlyphType = 'Arrow'
streamTracer1Display.GlyphTableIndexArray = 'Vlx'
streamTracer1Display.GaussianRadius = 0.9886100387573242
streamTracer1Display.SetScaleArray = ['POINTS', 'Vlx']
streamTracer1Display.ScaleTransferFunction = 'PiecewiseFunction'
streamTracer1Display.OpacityArray = ['POINTS', 'Vlx']
streamTracer1Display.OpacityTransferFunction = 'PiecewiseFunction'
streamTracer1Display.DataAxesGrid = 'GridAxesRepresentation'
streamTracer1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
streamTracer1Display.ScaleTransferFunction.Points = [-3.8008921146392822, 0.0, 0.5, 0.0, 94.81583404541016, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
streamTracer1Display.OpacityTransferFunction.Points = [-3.8008921146392822, 0.0, 0.5, 0.0, 94.81583404541016, 1.0, 0.5, 0.0]

# hide data in view
Hide(slice1, renderView1)

# show color bar/color legend
streamTracer1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on streamTracer1
streamTracer1.Input = cellDatatoPointData1

# set active source
SetActiveSource(slice1)

# show data in view
slice1Display = Show(slice1, renderView1)# 'GeometryRepresentation')

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(streamTracer1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=streamTracer1.SeedType)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(streamTracer1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
streamTracer1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
streamTracer1Display.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera()

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=streamTracer1.SeedType)

# Properties modified on streamTracer1
streamTracer1.MaximumStreamlineLength = 200.0

# update the view to ensure updated data information
renderView1.Update()

# get color legend/bar for vLUT in view renderView1
vLUTColorBar = GetScalarBar(vLUT, renderView1)
vLUTColorBar.Title = 'V'
vLUTColorBar.ComponentTitle = 'Magnitude'

# change scalar bar placement
vLUTColorBar.WindowLocation = 'AnyLocation'
vLUTColorBar.Position = [0.8808900523560209, 0.4759493670886076]
vLUTColorBar.ScalarBarLength = 0.33000000000000074

# change scalar bar placement
vLUTColorBar.Position = [0.8893979057591622, 0.4227848101265822]

# layout/tab size in pixels
#layout1.SetSize(1528, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [234.3956375053563, 183.84018238099065, 43.73481269935398]
renderView1.CameraFocalPoint = [60.43722724914551, 183.84018238099065, 43.73481269935398]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 302.8972733547114

# save screenshot
SaveScreenshot(dir_vis +'streamlines_V_field_vertical_cut'+current_time+'.png', renderView1, ImageResolution=[1528, 790])

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
#layout1.SetSize(1528, 790)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [190.20708223694058, 209.59847485087883, 77.6446131680386]
renderView1.CameraFocalPoint = [49.28719814613809, 226.3756030703026, 54.64145292464706]
renderView1.CameraViewUp = [-0.1610415408355278, 0.0005338142130951705, 0.9869474845034588]
renderView1.CameraParallelScale = 302.8972733547114

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).