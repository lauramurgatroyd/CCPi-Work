import vtk


def AdjustCamera(ren, sliceOrientation, activeSlice, resetcamera=False):
    ren.ResetCameraClippingRange()

    # adjust camera focal point
    camera = ren.GetActiveCamera()
    fp = list(camera.GetFocalPoint())
    fp[sliceOrientation] = activeSlice
    camera.SetFocalPoint(fp)

    if resetcamera:
        ren.ResetCamera()


reader = vtk.vtkMetaImageReader()
reader.SetFileName(
    r'head.mha')
reader.Update()
img3D = reader.GetOutput()

# select one slice in Z
extent = [i for i in img3D.GetExtent()]
slicenos = [0, 0, 0]
for i in range(len(slicenos)):
    slicenos[i] = round((extent[i * 2+1] + extent[i * 2])/2)

sliceOrientation = 2
activeSlice = 10

extent[sliceOrientation * 2] = 10
extent[sliceOrientation * 2 + 1] = 10

# VOI:
voi = vtk.vtkExtractVOI()
voi.SetInputData(img3D)
voi.SetVOI(extent[0], extent[1],
           extent[2], extent[3],
           extent[4], extent[5])

voi.Update()

# set window/level for current slices
ia = vtk.vtkImageHistogramStatistics()
ia.SetInputData(voi.GetOutput())
ia.SetAutoRangePercentiles(1.0, 95.)
ia.Update()
cmin, cmax = ia.GetAutoRange()
# probably the level could be the median of the image within
# the percentiles
level = ia.GetMedian()
# accomodates all values between the level an the percentiles
window = 2*max(abs(level-cmin), abs(level-cmax))

InitialLevel = level
InitialWindow = window

imageSlice = vtk.vtkImageSlice()

imageSliceMapper = vtk.vtkImageSliceMapper()
imageSliceMapper.SetInputData(voi.GetOutput())
imageSlice.SetMapper(imageSliceMapper)

imageSlice.GetProperty().SetColorLevel(InitialLevel)
imageSlice.GetProperty().SetColorWindow(InitialWindow)
imageSlice.GetProperty().SetInterpolationTypeToNearest()

ren = vtk.vtkRenderer()
ren.AddViewProp(imageSlice)

ren.ResetCamera()

AdjustCamera(ren, sliceOrientation, activeSlice, resetcamera=True)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(ren)
renderWindow.SetWindowName("ImageTracerWidget")

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

style = vtk.vtkInteractorStyleImage() # same effect with vtk.vtkInteractorStyle3D()
interactor.SetInteractorStyle(style)

tracer = vtk.vtkImageTracerWidget()
tracer.GetLineProperty().SetLineWidth(5)
tracer.SetInteractor(interactor)


tracer.GetLineProperty().SetColor(0.8, 0.8, 1.0)
tracer.GetLineProperty().SetLineWidth(3.0)
tracer.GetHandleProperty().SetColor(0.4, 0.4, 1.0)
tracer.GetSelectedHandleProperty().SetColor(1.0, 1.0, 1.0)
tracer.AutoCloseOn()
tracer.SetCaptureRadius(1.5)
tracer.ProjectToPlaneOn()
# # Set the size of the glyph handle
tracer.GetGlyphSource().SetScale(2.0)
# Set the initial rotation of the glyph if desired.  The default glyph
# set internally by the widget is a '+' so rotating 45 deg. gives a 'x'
tracer.GetGlyphSource().SetRotationAngle(45.0)
tracer.GetGlyphSource().Modified()

tracer.SetProjectionNormal(sliceOrientation)
# Set the Tracer widget's position along the current projection normal,
# which should be the same location as the current slice.
slice_coords = [0, 0, 0]
slice_coords[sliceOrientation] = activeSlice
tracer.SetProjectionPosition(slice_coords[sliceOrientation])
tracer.SetViewProp(imageSlice)


renderWindow.Render()

tracer.On()

tracer.SetInteraction(True)
interactor.Start()
