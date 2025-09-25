from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkLine
from vtkmodules.vtkCommonCore import vtkPoints


def generate_line(point_0=(0, 0, 0), point_1=(1, 1, 1)):

    line = vtkLine()
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 1)

    points = vtkPoints()
    points.InsertNextPoint(point_0)
    points.InsertNextPoint(point_1)

    u_grid = vtkUnstructuredGrid()
    u_grid.SetPoints(points)
    u_grid.InsertNextCell(line.GetCellType(), line.GetPointIds())

    return u_grid


