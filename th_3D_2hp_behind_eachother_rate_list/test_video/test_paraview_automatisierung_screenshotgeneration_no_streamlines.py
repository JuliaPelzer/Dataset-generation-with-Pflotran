# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
pflotranvel0 = LegacyVTKReader(registrationName='pflotran-vel-0*', FileNames=['/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-000.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-001.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-002.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-003.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-004.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-005.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-006.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-007.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-008.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-009.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-010.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-011.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-012.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-013.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-014.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-015.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-016.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-017.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-018.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-019.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-020.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-021.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-022.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-023.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-024.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-025.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-026.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-027.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-028.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-029.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-030.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-031.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-032.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-033.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-034.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-035.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-036.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-037.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-038.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-039.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-040.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-041.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-042.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-043.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-044.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-045.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-046.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-047.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-048.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-049.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-vel-050.vtk'])

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

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=cellDatatoPointData1)
clip1.ClipType = 'Plane'
#clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['POINTS', 'Vlx']

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [50.0, 300.0, 40.0]

# init the 'Plane' selected for 'HyperTreeGridClipper'
#clip1.HyperTreeGridClipper.Origin = [50.0, 300.0, 40.0]

# show data in view
clip1Display = Show(clip1, renderView1)#, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['POINTS', 'Vlx']
clip1Display.LookupTable = vlxLUT
#clip1Display.SelectTCoordArray = 'None'
#clip1Display.SelectNormalArray = 'None'
#clip1Display.SelectTangentArray = 'None'
clip1Display.OSPRayScaleArray = 'Vlx'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.SelectOrientationVectors = 'None'
clip1Display.ScaleFactor = 60.0
clip1Display.SelectScaleArray = 'Vlx'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'Vlx'
clip1Display.GaussianRadius = 3.0
clip1Display.SetScaleArray = ['POINTS', 'Vlx']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = ['POINTS', 'Vlx']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = vlxPWF
clip1Display.ScalarOpacityUnitDistance = 9.0729233672746
#clip1Display.OpacityArrayName = ['POINTS', 'Vlx']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera()

animationScene1.GoToNext()

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# set scalar coloring
ColorBy(clip1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
clip1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

animationScene1.GoToLast()

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# layout/tab size in pixels
#layout1.SetSize(1424, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [683.3800052725995, 300.0, 34.96236980003521]
renderView1.CameraFocalPoint = [49.999999999999986, 300.0, 40.0]
renderView1.CameraViewUp = [0.007953315272502374, 0.0, 0.9999683718879194]
renderView1.CameraParallelScale = 425.2077461397823

# save screenshot
SaveScreenshot('/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/test_video/V_field_vertical_cut_last_step.png', renderView1, ImageResolution=[1424, 790])

# Properties modified on animationScene1
animationScene1.AnimationTime = 1.0

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# layout/tab size in pixels
#layout1.SetSize(1424, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [683.3800052725995, 300.0, 34.96236980003521]
renderView1.CameraFocalPoint = [49.999999999999986, 300.0, 40.0]
renderView1.CameraViewUp = [0.007953315272502374, 0.0, 0.9999683718879194]
renderView1.CameraParallelScale = 425.2077461397823

# save screenshot
SaveScreenshot('/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/test_video/V_field_vertical_cut_first_step.png', renderView1, ImageResolution=[1424, 790])

animationScene1.GoToLast()

# set active source
SetActiveSource(cellDatatoPointData1)

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# hide data in view
Hide(clip1, renderView1)

# set scalar coloring
ColorBy(cellDatatoPointData1Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
cellDatatoPointData1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=cellDatatoPointData1)
clip2.ClipType = 'Plane'
#clip2.HyperTreeGridClipper = 'Plane'
clip2.Scalars = ['POINTS', 'Vlx']
clip2.Value = 0.011077880859375

# init the 'Plane' selected for 'ClipType'
clip2.ClipType.Origin = [50.0, 300.0, 40.0]

# init the 'Plane' selected for 'HyperTreeGridClipper'
#clip2.HyperTreeGridClipper.Origin = [50.0, 300.0, 40.0]

# Properties modified on clip2.ClipType
clip2.ClipType.Normal = [0.0, 0.0, 1.0]

# show data in view
clip2Display = Show(clip2, renderView1)#, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip2Display.Representation = 'Surface'
clip2Display.ColorArrayName = ['POINTS', 'Vlx']
clip2Display.LookupTable = vlxLUT
#clip2Display.SelectTCoordArray = 'None'
#clip2Display.SelectNormalArray = 'None'
#clip2Display.SelectTangentArray = 'None'
clip2Display.OSPRayScaleArray = 'Vlx'
clip2Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip2Display.SelectOrientationVectors = 'None'
clip2Display.ScaleFactor = 60.0
clip2Display.SelectScaleArray = 'Vlx'
clip2Display.GlyphType = 'Arrow'
clip2Display.GlyphTableIndexArray = 'Vlx'
clip2Display.GaussianRadius = 3.0
clip2Display.SetScaleArray = ['POINTS', 'Vlx']
clip2Display.ScaleTransferFunction = 'PiecewiseFunction'
clip2Display.OpacityArray = ['POINTS', 'Vlx']
clip2Display.OpacityTransferFunction = 'PiecewiseFunction'
clip2Display.DataAxesGrid = 'GridAxesRepresentation'
clip2Display.PolarAxes = 'PolarAxesRepresentation'
clip2Display.ScalarOpacityFunction = vlxPWF
clip2Display.ScalarOpacityUnitDistance = 9.10606545570102
#clip2Display.OpacityArrayName = ['POINTS', 'Vlx']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip2Display.ScaleTransferFunction.Points = [-7.251944541931152, 0.0, 0.5, 0.0, 7.248626708984375, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip2Display.OpacityTransferFunction.Points = [-7.251944541931152, 0.0, 0.5, 0.0, 7.248626708984375, 1.0, 0.5, 0.0]

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
clip2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on clip2.ClipType
clip2.ClipType.Origin = [50.0, 300.0, 50.0]

# update the view to ensure updated data information
renderView1.Update()

# Rescale transfer function
vlxLUT.RescaleTransferFunction(-136.186767578125, 136.20892333984375)

# Rescale transfer function
vlxPWF.RescaleTransferFunction(-136.186767578125, 136.20892333984375)

# set scalar coloring
ColorBy(clip2Display, ('POINTS', 'V', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vlxLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
clip2Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip2Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(cellDatatoPointData1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=clip2.ClipType)

# hide data in view
Hide(clip2, renderView1)

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# destroy clip2
Delete(clip2)
del clip2

# set active source
SetActiveSource(clip1)

# set active source
SetActiveSource(cellDatatoPointData1)

# reset view to fit data
renderView1.ResetCamera()

# rescale color and/or opacity maps used to exactly fit the current data range
cellDatatoPointData1Display.RescaleTransferFunctionToDataRange(False, True)

# layout/tab size in pixels
#layout1.SetSize(1424, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [43.800494036970036, 240.17476745676086, 496.9532069081173]
renderView1.CameraFocalPoint = [43.800494036970036, 240.17476745676086, 40.0]
renderView1.CameraViewUp = [-1.0, 2.220446049250313e-16, 0.0]
renderView1.CameraParallelScale = 306.75723300355935

# save screenshot
SaveScreenshot('/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/test_video/V_field_top_view_last_step.png', renderView1, ImageResolution=[1424, 790])