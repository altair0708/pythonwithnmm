from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkConvexPointSet, vtkTriangle, vtkImageData
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, VTK_UNSIGNED_CHAR
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkImagingStencil import vtkPolyDataToImageStencil, vtkImageStencil
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingMorphological import vtkImageConnectivityFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter, vtkXMLUnstructuredGridWriter


def generate_test_case():
    """
    创建一个简单的测试场景：
    - 一个立方体作为 vtkPolyhedron（以 vtkConvexPointSet 代替）
    - 一张穿透立方体的三角形平面
    返回两个 vtkUnstructuredGrid
    """
    # 创建立方体
    cube_source = vtkCubeSource()
    cube_source.SetXLength(10.0)
    cube_source.SetYLength(10.0)
    cube_source.SetZLength(10.0)
    cube_source.SetCenter(0.0, 0.0, 0.0)
    cube_source.Update()

    cube_polydata = cube_source.GetOutput()

    # 构造 polyhedron grid（用 ConvexPointSet 模拟）
    polyhedron_ugrid = vtkUnstructuredGrid()
    points = cube_polydata.GetPoints()
    polyhedron_ugrid.SetPoints(points)

    ids = vtkIdList()
    for i in range(points.GetNumberOfPoints()):
        ids.InsertNextId(i)

    polyhedron = vtkConvexPointSet()
    for i in range(ids.GetNumberOfIds()):
        polyhedron.GetPointIds().InsertNextId(ids.GetId(i))

    polyhedron_ugrid.InsertNextCell(polyhedron.GetCellType(), polyhedron.GetPointIds())

    # 创建穿透平面（三角面片）
    triangle_ugrid = vtkUnstructuredGrid()
    triangle_points = vtkPoints()
    triangle_points.InsertNextPoint(-20, 0, 0)
    triangle_points.InsertNextPoint(20, 0, 0)
    triangle_points.InsertNextPoint(0, -20, 5)
    triangle_points.InsertNextPoint(0, 20, 7)
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
    writer.SetFileName('re006_triangle_ugrid.vtu')
    writer.SetInputData(triangle_ugrid)
    writer.Write()

    return polyhedron_ugrid, triangle_ugrid


def surface_divides_polyhedron_voxel(polyhedron_ugrid, surface_ugrid, spacing=(0.1, 0.1, 0.1)):
    bounds = [0]*6
    polyhedron_ugrid.GetBounds(bounds)
    margin = 2.0
    for i in range(3):
        bounds[2*i] -= margin * spacing[i]
        bounds[2*i+1] += margin * spacing[i]

    image = vtkImageData()
    dims = [
        int((bounds[1] - bounds[0]) / spacing[0]) + 1,
        int((bounds[3] - bounds[2]) / spacing[1]) + 1,
        int((bounds[5] - bounds[4]) / spacing[2]) + 1,
    ]
    image.SetDimensions(dims)
    image.SetSpacing(spacing)
    image.SetOrigin(bounds[0], bounds[2], bounds[4])
    image.AllocateScalars(VTK_UNSIGNED_CHAR, 1)
    image.GetPointData().GetScalars().Fill(0)

    poly_geom = vtkGeometryFilter()
    poly_geom.SetInputData(polyhedron_ugrid)

    poly_stencil = vtkPolyDataToImageStencil()
    poly_stencil.SetInputConnection(poly_geom.GetOutputPort())
    poly_stencil.SetOutputOrigin(image.GetOrigin())
    poly_stencil.SetOutputSpacing(image.GetSpacing())
    poly_stencil.SetOutputWholeExtent(image.GetExtent())

    apply_poly = vtkImageStencil()
    apply_poly.SetInputData(image)
    apply_poly.SetStencilConnection(poly_stencil.GetOutputPort())
    apply_poly.ReverseStencilOff()
    apply_poly.SetBackgroundValue(0)
    apply_poly.Update()
    inside_image = apply_poly.GetOutput()
    inside_image.GetPointData().GetScalars().FillComponent(0, 1)

    writer = vtkXMLImageDataWriter()
    writer.SetInputData(inside_image)
    writer.SetFileName('re006_cube_voxel.vti')
    writer.Write()

    surf_geom = vtkGeometryFilter()
    surf_geom.SetInputData(surface_ugrid)

    surf_stencil = vtkPolyDataToImageStencil()
    surf_stencil.SetInputConnection(surf_geom.GetOutputPort())
    surf_stencil.SetOutputOrigin(image.GetOrigin())
    surf_stencil.SetOutputSpacing(image.GetSpacing())
    surf_stencil.SetOutputWholeExtent(image.GetExtent())

    apply_surf = vtkImageStencil()
    apply_surf.SetInputData(inside_image)
    apply_surf.SetStencilConnection(surf_stencil.GetOutputPort())
    apply_surf.ReverseStencilOff()
    apply_surf.SetBackgroundValue(100)
    apply_surf.Update()

    writer = vtkXMLImageDataWriter()
    writer.SetInputConnection(apply_surf.GetOutputPort())
    writer.SetFileName('re006_surface_voxel.vti')
    writer.Write()

    thresh = vtkImageThreshold()
    thresh.SetInputConnection(apply_surf.GetOutputPort())
    thresh.ThresholdBetween(1, 1)
    thresh.SetInValue(1)
    thresh.SetOutValue(0)
    thresh.SetOutputScalarTypeToUnsignedChar()
    thresh.Update()

    conn = vtkImageConnectivityFilter()
    conn.SetInputConnection(thresh.GetOutputPort())
    conn.SetExtractionModeToAllRegions()
    conn.SetLabelModeToSizeRank()
    conn.Update()

    num_regions = conn.GetNumberOfExtractedRegions()

    return conn.GetNumberOfExtractedRegions() >= 2


# ✅ 执行测试
poly, surf = generate_test_case()
if surface_divides_polyhedron_voxel(poly, surf):
    print("✅ 曲面穿透成功，将多面体一分为二")
else:
    print("❌ 曲面未完全穿透多面体")
