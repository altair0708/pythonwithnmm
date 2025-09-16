from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkConvexPointSet, vtkTriangle, vtkImageData
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, VTK_UNSIGNED_CHAR
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkImagingStencil import vtkPolyDataToImageStencil, vtkImageStencil
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingMorphological import vtkImageConnectivityFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter, vtkXMLUnstructuredGridWriter


triangle_ugrid = vtkUnstructuredGrid()
triangle_points = vtkPoints()
triangle_points.InsertNextPoint(0, 0, 0)
triangle_points.InsertNextPoint(1, 0, 1)
triangle_points.InsertNextPoint(0, 1, 1)
triangle_points.InsertNextPoint(1, 1, 0)
triangle_ugrid.SetPoints(triangle_points)

tri1 = vtkTriangle()
tri1.GetPointIds().SetId(0, 0)
tri1.GetPointIds().SetId(1, 1)
tri1.GetPointIds().SetId(2, 2)

tri2 = vtkTriangle()
tri2.GetPointIds().SetId(0, 1)
tri2.GetPointIds().SetId(1, 3)
tri2.GetPointIds().SetId(2, 2)

triangle_ugrid.InsertNextCell(tri1.GetCellType(), tri1.GetPointIds())
triangle_ugrid.InsertNextCell(tri2.GetCellType(), tri2.GetPointIds())

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(triangle_ugrid)
writer.SetFileName('re007_surface_ugrid.vtu')
writer.Write()

poly_geom = vtkGeometryFilter()
poly_geom.SetInputData(triangle_ugrid)
poly_geom.Update()
poly_data = poly_geom.GetOutput()

implicit_distance = vtkImplicitPolyDataDistance()
implicit_distance.SetInput(poly_geom.GetOutput())

sample = vtkSampleFunction()
sample.SetImplicitFunction(implicit_distance)
sample.SetSampleDimensions(100, 100, 100)
bounds = list(poly_data.GetBounds())
sample.SetModelBounds(bounds)
sample.ComputeNormalsOff()

threshold = vtkImageThreshold()
threshold.SetInputConnection(sample.GetOutputPort())

# 设置阈值范围（提取距离小于 0 的区域）
threshold.ThresholdByLower(0.0)  # 提取小于等于 0 的体素

# 设置提取后体素值
threshold.SetInValue(1)    # 在范围内的体素设为 1
threshold.SetOutValue(0)   # 范围外体素设为 0
threshold.SetOutputScalarTypeToUnsignedChar()  # 可设为 uchar 掩码

writer = vtkXMLImageDataWriter()
writer.SetInputConnection(threshold.GetOutputPort())
writer.SetFileName('re007_surface_voxel.vti')
writer.Write()


