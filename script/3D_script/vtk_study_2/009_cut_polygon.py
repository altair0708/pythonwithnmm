from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon, vtkPlane, vtkTriangle, vtkTetra, vtkPolyData, vtkCellArray, vtkPolyLine, vtkStaticPointLocator, vtkMergePoints, vtkPointLocator
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIdListCollection, vtkVersion, reference
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet, vtkCleanUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkClipPolyData, vtkAppendFilter, vtkFeatureEdges, vtkStripper, vtkDecimatePolylineFilter, vtkCutter
from vtkmodules.vtkFiltersGeneric import vtkGenericClip
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter
from vtkmodules.vtkCommonMisc import vtkPolygonBuilder
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
from NMM.base.VTKBase import write_file


points = vtkPoints()
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(-1, 1, 1)
points.InsertNextPoint(-3, 0.5, 2)
points.InsertNextPoint(-1, 0, 1)

polygon = vtkPolygon()
polygon.GetPointIds().SetNumberOfIds(5)
polygon.GetPointIds().SetId(0, 0)
polygon.GetPointIds().SetId(1, 1)
polygon.GetPointIds().SetId(2, 2)
polygon.GetPointIds().SetId(3, 3)
polygon.GetPointIds().SetId(4, 4)
# polyhedron = vtkTetra()
# polyhedron.GetPointIds().SetNumberOfIds(4)
# polyhedron.GetPointIds().SetId(0, 0)
# polyhedron.GetPointIds().SetId(1, 1)
# polyhedron.GetPointIds().SetId(2, 2)
# polyhedron.GetPointIds().SetId(3, 3)

polys = vtkCellArray()
polys.InsertNextCell(polygon)

u_grid = vtkPolyData()
u_grid.SetPolys(polys)
u_grid.SetPoints(points)

origin = (0, 0, 10)
normal = (1, 0, 0)

clip_plane_1 = vtkPlane()
clip_plane_1.SetOrigin(origin)
clip_plane_1.SetNormal(normal)

clipper = vtkClipPolyData()
# clipper = vtkGenericClip()
# clipper.GenerateClippedOutputOn()
clipper.InsideOutOn()
clipper.SetClipFunction(clip_plane_1)
clipper.SetInputData(u_grid)
clipper.Update()

edges = vtkFeatureEdges()
edges.SetInputConnection(clipper.GetOutputPort())
edges.BoundaryEdgesOn()
edges.FeatureEdgesOff()
edges.ManifoldEdgesOff()
edges.NonManifoldEdgesOff()

stripper = vtkStripper()
stripper.SetInputConnection(edges.GetOutputPort())
stripper.Update()

result: vtkPolyData = stripper.GetOutput()
writer = vtkXMLPolyDataWriter()
writer.SetInputData(result)
writer.SetFileName('re009_0.vtp')
writer.Write()

new_id_list = vtkIdList()
new_id_list.DeepCopy(result.GetCell(0).GetPointIds())
id_list = [new_id_list.GetId(i) for i in range(new_id_list.GetNumberOfIds())]
id_list.pop(0)
id_list.append(id_list[0])

polyline = vtkPolyLine()
# polyline.GetPointIds().SetNumberOfIds(len(id_list))
[polyline.GetPointIds().InsertNextId(i) for i in id_list]

a = vtkCellArray()
a.InsertNextCell(polyline)

b = vtkPolyData()
b.SetLines(a)
b.SetPoints(result.GetPoints())

u_grid = vtkUnstructuredGrid()

writer = vtkXMLPolyDataWriter()
writer.SetInputData(b)
writer.SetFileName('re009_1.vtp')
writer.Write()

decimate = vtkDecimatePolylineFilter()
decimate.SetMaximumError(0.000001)
decimate.SetInputData(b)
decimate.Update()
# decimate.SetInputConnection(stripper.GetOutputPort())

result: vtkPolyData = decimate.GetOutput()
# print(result.GetNumberOfCells())
# print(result.GetNumberOfPoints())
writer = vtkXMLPolyDataWriter()
writer.SetInputData(result)
writer.SetFileName('re009_2.vtp')
writer.Write()

looper = vtkContourLoopExtraction()
looper.SetInputData(b)
# looper.SetInputConnection(decimate.GetOutputPort())

appender = vtkAppendFilter()
appender.SetInputConnection(looper.GetOutputPort())
appender.Update()

# cleaner = vtkCleanUnstructuredGrid()
# cleaner.RemovePointsWithoutCellsOn()
# cleaner.SetInputConnection(appender.GetOutputPort())
# cleaner.Update()
result: vtkUnstructuredGrid = appender.GetOutput()

# print(result.GetCell(0).GetNumberOfPoints())
# print(result.GetCell(0).GetPointIds().GetId(0))
# print(result.GetNumberOfPoints())
# print(result.GetNumberOfCells())

# print(result.GetCells())
# polygon_collection = vtkIdListCollection()
# polygon_builder = vtkPolygonBuilder()
# for each_id in range(result.GetNumberOfCells()):
#     temp_cell = result.GetCell(each_id)
#     triangle_list = []
#     for each in range(temp_cell.GetPointIds().GetNumberOfIds()):
#         triangle_list.append(temp_cell.GetPointIds().GetId(each))
#     print(triangle_list)
#     polygon_builder.InsertTriangle(triangle_list)
# polygon_builder.GetPolygons(polygon_collection)
# print(polygon_collection.GetNumberOfItems())

print(vtkVersion.GetVTKVersion())
write_file(result, 're009_3.vtu')


def clip_a_surface(surface_grid: vtkUnstructuredGrid, origin_point, normal_vector):
    assert surface_grid.GetNumberOfCells() == 1

    plane = vtkPlane()
    plane.SetNormal(normal_vector)
    plane.SetOrigin(origin_point)

    poly_data = vtkPolyData()

    temp = vtkCellArray()
    temp.DeepCopy(surface_grid.GetCells())
    poly_data.SetPolys(temp)

    temp = vtkPoints()
    temp.DeepCopy(surface_grid.GetPoints())
    poly_data.SetPoints(temp)

    clipper = vtkClipPolyData()
    clipper.SetClipFunction(plane)
    clipper.SetInputData(poly_data)
    clipper.GenerateClippedOutputOn()

    def push_a_location(p_grid: vtkPolyData):
        new_id_list = vtkIdList()
        new_id_list.DeepCopy(p_grid.GetCell(0).GetPointIds())
        id_list = [new_id_list.GetId(i) for i in range(new_id_list.GetNumberOfIds())]
        id_list.pop(0)
        id_list.append(id_list[0])

        polyline = vtkPolyLine()
        [polyline.GetPointIds().InsertNextId(i) for i in id_list]

        cell_array = vtkCellArray()
        cell_array.InsertNextCell(polyline)

        points = vtkPoints()
        points.DeepCopy(p_grid.GetPoints())
        poly_data = vtkPolyData()
        poly_data.SetLines(cell_array)
        poly_data.SetPoints(points)

        return poly_data

    def in_points(point_0, p_grid: vtkUnstructuredGrid):
        # p_grid.BuildLocator()
        locator = vtkPointLocator()
        # print(locator.GetClassName())
        # locator.InitPointInsertion(p_grid.GetPoints(), p_grid.GetBounds())
        locator.SetDataSet(p_grid)
        temp_points = [p_grid.GetPoint(i) for i in range(p_grid.GetNumberOfPoints())]
        print(point_0)
        print(temp_points)
        print(point_0 in temp_points)
        # locator.InsertNextPoint(point_0)
        result = vtkIdList()
        locator.FindPointsWithinRadius(0.00001, point_0, result)
        print(result.GetNumberOfIds())
        if result.GetNumberOfIds() > 0:
            return True
        else:
            return False

    def pipeline(clip_port, origin_poly_data):
        edges = vtkFeatureEdges()
        edges.SetInputConnection(clip_port)
        edges.BoundaryEdgesOn()
        edges.FeatureEdgesOff()
        edges.ManifoldEdgesOff()
        edges.NonManifoldEdgesOff()

        stripper = vtkStripper()
        stripper.SetInputConnection(edges.GetOutputPort())
        stripper.Update()

        temp: vtkPolyData = stripper.GetOutput()
        point_0 = temp.GetPoint(temp.GetCell(0).GetPointId(0))
        # print(in_points(point_0, origin_poly_data))
        origin_poly_data.ComputeBounds()
        while not in_points(point_0, origin_poly_data):
            point_0 = temp.GetPoint(temp.GetCell(0).GetPointId(0))
            temp = push_a_location(temp)

        decimate = vtkDecimatePolylineFilter()
        decimate.SetMaximumError(0.000001)
        # decimate.SetInputConnection(stripper.GetOutputPort())
        decimate.SetInputData(temp)

        looper = vtkContourLoopExtraction()
        looper.SetInputConnection(decimate.GetOutputPort())

        appender = vtkAppendFilter()
        appender.SetInputConnection(looper.GetOutputPort())

        appender.Update()
        result: vtkUnstructuredGrid = appender.GetOutput()
        return result

    result_0 = pipeline(clipper.GetOutputPort(0), surface_grid)
    result_1 = pipeline(clipper.GetOutputPort(1), surface_grid)

    return result_0, result_1


if __name__ == '__main__':

    points = vtkPoints()
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(-1, 1, 1)
    points.InsertNextPoint(-3, 0.5, 2)
    points.InsertNextPoint(-1, 0, 1)

    polygon = vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(5)
    polygon.GetPointIds().SetId(0, 0)
    polygon.GetPointIds().SetId(1, 1)
    polygon.GetPointIds().SetId(2, 2)
    polygon.GetPointIds().SetId(3, 3)
    polygon.GetPointIds().SetId(4, 4)

    u_grid = vtkUnstructuredGrid()
    u_grid.InsertNextCell(polygon.GetCellType(), polygon.GetPointIds())
    u_grid.SetPoints(points)

    surface_0, surface_1 = clip_a_surface(u_grid, (0, 0, 0), (1, 0, 0))

    write_file(surface_0, 're009_4.vtu')
    write_file(surface_1, 're009_5.vtu')

