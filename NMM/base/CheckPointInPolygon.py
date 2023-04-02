from vtkmodules.vtkCommonDataModel import vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkFloatArray
from NMM.GlobalVariable import CONST


def check_point_in_polygon(point, vtk_polygon: vtkPolygon):

    bounds = vtk_polygon.GetBounds()
    points: vtkPoints = vtk_polygon.GetPoints()
    points_number = vtk_polygon.GetNumberOfPoints()
    points_data: vtkFloatArray = points.GetData()
    points_data_list = [points_data.GetValue(i) for i in range(points_data.GetNumberOfValues())]

    # normal = [0, 0, 0]
    # vtkPolygon.ComputeNormal(points, normal)
    # result = vtkPolygon.PointInPolygon(point, points_number, points_data_list, bounds, normal)

    # if result == 1:
    #     return True
    # elif result == 0:
    #     return False
    # else:
    #     raise Exception('check_point_in_polygon function error!')

    close_point = [0, 0, 0]
    distance = vtkPolygon.DistanceToPolygon(point, points_number, points_data_list, bounds, close_point)

    if distance < CONST.TOLERANCE:
        return True
    else:
        return False
