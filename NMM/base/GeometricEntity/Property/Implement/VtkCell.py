from NMM.base.GeometricEntity.Property.PropertyInterface import AbstractProperty
from NMM.base.CopyFunction import copy_polyhedron, copy_vtk_cell, get_polyhedron_list
from NMM.base.ModifyVtkCellNew import insert_a_grid
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
        vtk_cell: vtkCell = grid.GetCell(id_value)
        new_vtk_cell: vtk_cell = copy_vtk_cell(vtk_cell, grid.GetPoints())

        # vtkPoints, vtkIdList, vtkCellType
        vtk_cell_points = new_vtk_cell.GetPoints()
        if new_vtk_cell.GetCellType() == 42:
            vtk_id_list = get_polyhedron_list(new_vtk_cell, new_vtk_cell.GetPoints())
        else:
            vtk_id_list = new_vtk_cell.GetPointIds()

        new_grid = vtkUnstructuredGrid()
        new_grid.InsertNextCell(new_vtk_cell.GetCellType(), vtk_id_list)
        new_grid.SetPoints(vtk_cell_points)

        return new_grid
