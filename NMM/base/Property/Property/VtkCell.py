from NMM.base.Property.PropertyInterface import AbstractProperty
from NMM.base.VTKBase.Implement.VTKBase import VTKBase
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


class VtkCell(AbstractProperty):
    def __init__(self, id_value: int, grid: vtkUnstructuredGrid):
        self.__name = 'VtkCell'
        self.__type = 11  # vtkUnstructuredGrid with only one cell

        temp_vtk_cell_grid = VTKBase.get_a_vtk_cell_grid(grid, id_value)
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

