from vtkmodules.vtkCommonDataModel import vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints


def calculate_area(points: vtkPoints):
    normal = [0, 0, 0]
    point_number = points.GetNumberOfPoints()
    point_id = [i for i in range(point_number)]
    vtkPolygon.ComputeNormal(points, point_number, point_id, normal)
    area = vtkPolygon.ComputeArea(points, point_number, point_id, normal)
    return area

if __name__ == '__main__':

    points = vtkPoints()
    points.InsertNextPoint((0, 0, 0))
    points.InsertNextPoint((1, 0, 0))
    points.InsertNextPoint((1, 1, 0))
    points.InsertNextPoint((0, 2, 0))
    points.InsertNextPoint((0, 1, 0))

    print(calculate_area(points))

