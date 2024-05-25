from NMM.base.GeometricEntity.Property.PropertyInterface import AbstractProperty
from NMM.base.CopyFunction import copy_polyhedron, copy_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell
from vtkmodules.vtkCommonCore import vtkPoints


class VtkCell(AbstractProperty):
    def __init__(self, id_value: int, grid: vtkUnstructuredGrid):
        self.__name = 'VtkCell'
        self.__type = 11  # vtkUnstructuredGrid

        temp_vtk_cell_grid = self.get_vtk_cell_grid(id_value, grid)
        self.__value = temp_vtk_cell_grid

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, temp_value):
        self.__value = temp_value

    # todo
    @staticmethod
    def get_vtk_cell_grid(id_value: int, grid: vtkUnstructuredGrid):
        temp_grid = vtkUnstructuredGrid()
        vtk_cell: vtkCell = grid.GetCell(id_value)
        element_grid_points: vtkPoints = grid.GetPoints()
        element_cell.vtk_cell = copy_polyhedron(element_vtk_cell, element_grid_points)
        return temp_grid
