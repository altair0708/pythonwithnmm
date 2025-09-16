from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkConvexPointSet, vtkTriangle, vtkImageData, vtkPolyhedron, vtkPolyData, vtkCellArray
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, VTK_UNSIGNED_CHAR
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance, vtkContourFilter, vtkConnectivityFilter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkImagingHybrid import vtkSampleFunction, vtkVoxelModeller
from vtkmodules.vtkImagingStencil import vtkPolyDataToImageStencil, vtkImageStencil, vtkImageToImageStencil
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingMorphological import vtkImageConnectivityFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter, vtkXMLUnstructuredGridWriter
from vtkmodules.vtkRenderingCore import vtkActor, vtkRenderer, vtkPolyDataMapper, vtkRenderWindow, vtkRenderWindowInteractor
from NMM.base.VTKBase.test_example import generate_tetra_polyhedron
from NMM.base.VTKBase.write_file import write_file

# 创建一个立方体
cube_source = vtkCubeSource()
cube_source.SetXLength(10)
cube_source.SetYLength(10)
cube_source.SetZLength(10)
cube_source.Update()
cube = cube_source.GetOutput()

# 创建一个穿过立方体的开放曲面（三角面）
points = vtkPoints()
points.InsertNextPoint(-10, 0, 0)
points.InsertNextPoint(10, 0, 0)
points.InsertNextPoint(0, 10, 0)

triangle = vtkTriangle()
triangle.GetPointIds().SetId(0, 0)
triangle.GetPointIds().SetId(1, 1)
triangle.GetPointIds().SetId(2, 2)

cells = vtkCellArray()
cells.InsertNextCell(triangle)

open_surface = vtkPolyData()
open_surface.SetPoints(points)
open_surface.SetPolys(cells)

# 将立方体转换为体素
voxel = vtkVoxelModeller()
voxel.SetInputData(cube)
voxel.SetSampleDimensions(100, 100, 100)
voxel.SetModelBounds(cube.GetBounds())
voxel.SetScalarTypeToFloat()
voxel.SetMaximumDistance(0.1)
voxel.Update()
volume = voxel.GetOutput()

# 距离函数（隐式函数）
distance = vtkImplicitPolyDataDistance()
distance.SetInput(open_surface)

sample = vtkSampleFunction()
sample.SetImplicitFunction(distance)
sample.SetModelBounds(volume.GetBounds())
sample.SetSampleDimensions(volume.GetDimensions())
sample.ComputeNormalsOff()
sample.Update()
distance_field = sample.GetOutput()

# 阈值掩膜
threshold = vtkImageThreshold()
threshold.SetInputData(distance_field)
threshold.ThresholdByLower(0.0)
threshold.SetInValue(255)
threshold.SetOutValue(0)
threshold.SetOutputScalarTypeToUnsignedChar()
threshold.Update()
mask = threshold.GetOutput()

# 裁剪
to_stencil = vtkImageToImageStencil()
to_stencil.SetInputData(mask)
to_stencil.ThresholdByLower(1)
to_stencil.Update()

stencil = vtkImageStencil()
stencil.SetInputData(volume)
stencil.SetStencilConnection(to_stencil.GetOutputPort())
stencil.ReverseStencilOff()
stencil.SetBackgroundValue(0)
stencil.Update()
clipped = stencil.GetOutput()

# 用等值面提取裁剪结果（clipped）进行可视化
contour = vtkContourFilter()
contour.SetInputData(clipped)
contour.SetValue(0, 0.5)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1.0, 0.4, 0.4)
contour_actor.GetProperty().SetOpacity(1.0)

# 可视化开放曲面（原始切割面）
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputData(open_surface)
surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetColor(0.2, 0.8, 1.0)
surface_actor.GetProperty().SetOpacity(0.5)

# 渲染窗口
renderer = vtkRenderer()
renderer.AddActor(contour_actor)
renderer.AddActor(surface_actor)
renderer.SetBackground(0.1, 0.1, 0.1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# 开始渲染
render_window.Render()
interactor.Start()

