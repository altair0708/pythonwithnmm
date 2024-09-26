from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellArray, vtkPolyData, vtkPolyLine, vtkPlane, vtkPointLocator
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
from vtkmodules.vtkFiltersCore import vtkClipPolyData, vtkAppendFilter, vtkFeatureEdges, vtkStripper, vtkDecimatePolylineFilter, vtkCutter
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints


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
