from vtkmodules.vtkCommonDataModel import vtkCell, vtkLine
from vtkmodules.vtkCommonCore import vtkPoints


class ObjectBase3D(object):
    def __init__(self, id_value):
        self.__id = id_value
        self.__vtkCell = None

    @property
    def id(self):
        return self.__id

    @property
    def vtk_cell(self):
        return self.__vtkCell

    @vtk_cell.setter
    def vtk_cell(self, cell):
        self.__vtkCell: vtkCell = cell

    @property
    def point_0(self):
        points: vtkPoints = self.vtk_cell.GetPoints()
        point_0 = points.GetPoint(0)
        return point_0

    @property
    def point_1(self):
        points: vtkPoints = self.vtk_cell.GetPoints()
        point_1 = points.GetPoint(1)
        return point_1
