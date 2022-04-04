# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
pflotran0 = LegacyVTKReader(registrationName='pflotran-0*', FileNames=['/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-000.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-001.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-002.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-003.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-004.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-005.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-006.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-007.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-008.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-009.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-010.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-011.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-012.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-013.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-014.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-015.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-016.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-017.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-018.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-019.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-020.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-021.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-022.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-023.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-024.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-025.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-026.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-027.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-028.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-029.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-030.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-031.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-032.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-033.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-034.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-035.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-036.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-037.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-038.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-039.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-040.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-041.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-042.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-043.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-044.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-045.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-046.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-047.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-048.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-049.vtk', '/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/output/pflotran-050.vtk'])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
pflotran0Display = Show(proxy=pflotran0, view=renderView1)#, representationType='UnstructuredGridRepresentation')

# get color transfer function/color map for 'Temperature'
temperatureLUT = GetColorTransferFunction('Temperature')
temperatureLUT.RGBPoints = [10.600000381469727, 0.231373, 0.298039, 0.752941, 10.600976943969727, 0.865003, 0.865003, 0.865003, 10.601953506469727, 0.705882, 0.0156863, 0.14902]
temperatureLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'Temperature'
temperaturePWF = GetOpacityTransferFunction('Temperature')
temperaturePWF.Points = [10.600000381469727, 0.0, 0.5, 0.0, 10.601953506469727, 1.0, 0.5, 0.0]
temperaturePWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
pflotran0Display.Representation = 'Surface'
pflotran0Display.ColorArrayName = ['CELLS', 'Temperature']
pflotran0Display.LookupTable = temperatureLUT
#pflotran0Display.SelectTCoordArray = 'None'
#pflotran0Display.SelectNormalArray = 'None'
#pflotran0Display.SelectTangentArray = 'None'
pflotran0Display.OSPRayScaleFunction = 'PiecewiseFunction'
pflotran0Display.SelectOrientationVectors = 'None'
pflotran0Display.ScaleFactor = 60.0
pflotran0Display.SelectScaleArray = 'Temperature'
pflotran0Display.GlyphType = 'Arrow'
pflotran0Display.GlyphTableIndexArray = 'Temperature'
pflotran0Display.GaussianRadius = 3.0
pflotran0Display.SetScaleArray = [None, '']
pflotran0Display.ScaleTransferFunction = 'PiecewiseFunction'
pflotran0Display.OpacityArray = [None, '']
pflotran0Display.OpacityTransferFunction = 'PiecewiseFunction'
pflotran0Display.DataAxesGrid = 'GridAxesRepresentation'
pflotran0Display.PolarAxes = 'PolarAxesRepresentation'
pflotran0Display.ScalarOpacityFunction = temperaturePWF
pflotran0Display.ScalarOpacityUnitDistance = 7.274018321161722
#pflotran0Display.OpacityArrayName = ['CELLS', 'Temperature'] #>TODO important for Legend?

# show color bar/color legend
pflotran0Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color legend/bar for temperatureLUT in view renderView1
temperatureLUTColorBar = GetScalarBar(temperatureLUT, renderView1)
temperatureLUTColorBar.Title = 'Temperature'
temperatureLUTColorBar.ComponentTitle = ''

# change scalar bar placement
temperatureLUTColorBar.WindowLocation = 'AnyLocation'
temperatureLUTColorBar.Position = [0.912958115183246, 0.3405063291139241]
temperatureLUTColorBar.ScalarBarLength = 0.32999999999999996

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=pflotran0)
clip1.ClipType = 'Plane'
#clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['CELLS', 'Temperature']
clip1.Value = 10.600000381469727

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [50.0, 300.0, 40.0]

# init the 'Plane' selected for 'HyperTreeGridClipper'
#clip1.HyperTreeGridClipper.Origin = [50.0, 300.0, 40.0]

# show data in view
clip1Display = Show(clip1, renderView1) #, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['CELLS', 'Temperature']
clip1Display.LookupTable = temperatureLUT
#clip1Display.SelectTCoordArray = 'None'
#clip1Display.SelectNormalArray = 'None'
#clip1Display.SelectTangentArray = 'None'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.SelectOrientationVectors = 'None'
clip1Display.ScaleFactor = 60.0
clip1Display.SelectScaleArray = 'Temperature'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'Temperature'
clip1Display.GaussianRadius = 3.0
clip1Display.SetScaleArray = [None, '']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = [None, '']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = temperaturePWF
clip1Display.ScalarOpacityUnitDistance = 9.0729233672746
#clip1Display.OpacityArrayName = ['CELLS', 'Temperature']

# hide data in view
Hide(pflotran0, renderView1)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=clip1.ClipType)

# reset view to fit data
renderView1.ResetCamera()

animationScene1.GoToNext()

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=clip1)
cellDatatoPointData1.CellDataArraytoprocess = ['Material_ID', 'Temperature']

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, renderView1)#, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
cellDatatoPointData1Display.Representation = 'Surface'
cellDatatoPointData1Display.ColorArrayName = ['POINTS', 'Temperature']
cellDatatoPointData1Display.LookupTable = temperatureLUT
#cellDatatoPointData1Display.SelectTCoordArray = 'None'
#cellDatatoPointData1Display.SelectNormalArray = 'None'
#cellDatatoPointData1Display.SelectTangentArray = 'None'
cellDatatoPointData1Display.OSPRayScaleArray = 'Temperature'
cellDatatoPointData1Display.OSPRayScaleFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.SelectOrientationVectors = 'None'
cellDatatoPointData1Display.ScaleFactor = 60.0
cellDatatoPointData1Display.SelectScaleArray = 'Temperature'
cellDatatoPointData1Display.GlyphType = 'Arrow'
cellDatatoPointData1Display.GlyphTableIndexArray = 'Temperature'
cellDatatoPointData1Display.GaussianRadius = 3.0
cellDatatoPointData1Display.SetScaleArray = ['POINTS', 'Temperature']
cellDatatoPointData1Display.ScaleTransferFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.OpacityArray = ['POINTS', 'Temperature']
cellDatatoPointData1Display.OpacityTransferFunction = 'PiecewiseFunction'
cellDatatoPointData1Display.DataAxesGrid = 'GridAxesRepresentation'
cellDatatoPointData1Display.PolarAxes = 'PolarAxesRepresentation'
cellDatatoPointData1Display.ScalarOpacityFunction = temperaturePWF
cellDatatoPointData1Display.ScalarOpacityUnitDistance = 9.0729233672746
#cellDatatoPointData1Display.OpacityArrayName = ['POINTS', 'Temperature']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
cellDatatoPointData1Display.ScaleTransferFunction.Points = [10.599305152893066, 0.0, 0.5, 0.0, 13.089489936828613, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
cellDatatoPointData1Display.OpacityTransferFunction.Points = [10.599305152893066, 0.0, 0.5, 0.0, 13.089489936828613, 1.0, 0.5, 0.0]

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
cellDatatoPointData1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Temporal Interpolator'
temporalInterpolator1 = TemporalInterpolator(registrationName='TemporalInterpolator1', Input=cellDatatoPointData1)

# show data in view
temporalInterpolator1Display = Show(temporalInterpolator1, renderView1)#, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
temporalInterpolator1Display.Representation = 'Surface'
temporalInterpolator1Display.ColorArrayName = ['POINTS', 'Temperature']
temporalInterpolator1Display.LookupTable = temperatureLUT
#temporalInterpolator1Display.SelectTCoordArray = 'None'
#temporalInterpolator1Display.SelectNormalArray = 'None'
#temporalInterpolator1Display.SelectTangentArray = 'None'
temporalInterpolator1Display.OSPRayScaleArray = 'Temperature'
temporalInterpolator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
temporalInterpolator1Display.SelectOrientationVectors = 'None'
temporalInterpolator1Display.ScaleFactor = 60.0
temporalInterpolator1Display.SelectScaleArray = 'Temperature'
temporalInterpolator1Display.GlyphType = 'Arrow'
temporalInterpolator1Display.GlyphTableIndexArray = 'Temperature'
temporalInterpolator1Display.GaussianRadius = 3.0
temporalInterpolator1Display.SetScaleArray = ['POINTS', 'Temperature']
temporalInterpolator1Display.ScaleTransferFunction = 'PiecewiseFunction'
temporalInterpolator1Display.OpacityArray = ['POINTS', 'Temperature']
temporalInterpolator1Display.OpacityTransferFunction = 'PiecewiseFunction'
temporalInterpolator1Display.DataAxesGrid = 'GridAxesRepresentation'
temporalInterpolator1Display.PolarAxes = 'PolarAxesRepresentation'
temporalInterpolator1Display.ScalarOpacityFunction = temperaturePWF
temporalInterpolator1Display.ScalarOpacityUnitDistance = 9.0729233672746
#temporalInterpolator1Display.OpacityArrayName = ['POINTS', 'Temperature']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
temporalInterpolator1Display.ScaleTransferFunction.Points = [10.599305152893066, 0.0, 0.5, 0.0, 13.089489936828613, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
temporalInterpolator1Display.OpacityTransferFunction.Points = [10.599305152893066, 0.0, 0.5, 0.0, 13.089489936828613, 1.0, 0.5, 0.0]

# hide data in view
Hide(cellDatatoPointData1, renderView1)

# show color bar/color legend
temporalInterpolator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on temporalInterpolator1
#temporalInterpolator1.ResampleFactor = 6

# update the view to ensure updated data information
renderView1.Update()

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
#layout1.SetSize(1528, 790)

# current camera placement for renderView1
renderView1.CameraPosition = [378.5674071009585, 262.9278771745436, 163.0554144827319]
renderView1.CameraFocalPoint = [25.391372165226173, 258.15793863260865, 40.50068071468933]
renderView1.CameraViewUp = [-0.32785611688787264, 0.002176734790805271, 0.9447251602687716]
renderView1.CameraParallelScale = 303.6856927812043

# save animation
SaveAnimation('/home/pelzerja/Development/simulation_groundtruth_pflotran/Phd_simulation_groundtruth/th_3D_2hp_behind_eachother_rate_list/test_video/test.avi', renderView1, ImageResolution=[1528, 788],
    FrameRate=24,
    FrameWindow=[0, 300])
