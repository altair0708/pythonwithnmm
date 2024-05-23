from NMM.crack_3D.ElementBase3D import Element3D
from vtkmodules.vtkCommonDataModel import vtkGenericCell, vtkCell, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.base.CopyFunction import copy_vtk_cell
from NMM.crack_3D.ObjectBase3D import ObjectBase3D


class NewElement3D(ObjectBase3D):
    def __init__(self, id_value):
        super().__init__(id_value)
        self.__super_id = -1
        self.__super_cell = None

        self.__adjacent_id = -1
        self.__adjacent_cell = None

    @property
    def super_id(self):
        return self.__super_id

    @super_id.setter
    def super_id(self, id_value):
        assert type(id_value) == int
        self.__super_id = id_value

    @property
    def super_cell(self):
        return self.__super_cell

    @super_cell.setter
    def super_cell(self, cell: Element3D):
        self.__super_cell = cell

    @property
    def adjacent_id(self):
        return self.__adjacent_id

    @adjacent_id.setter
    def adjacent_id(self, id_value):
        assert type(id_value) == int
        self.__adjacent_id = id_value

    @property
    def adjacent_cell(self):
        return self.__adjacent_cell

    @adjacent_cell.setter
    def adjacent_cell(self, cell):
        self.__adjacent_cell = cell


def create_an_new_element(element_id_0: int,
                          element_id_1: int,
                          super_element: Element3D,
                          element_grid_0: vtkUnstructuredGrid,
                          element_grid_1: vtkUnstructuredGrid):

    # element id 0
    element_cell_0 = NewElement3D(id_value=element_id_0)
    # element vtk cell
    element_vtk_cell: vtkCell = element_grid_0.GetCell(0)
    element_grid_points: vtkPoints = element_grid_0.GetPoints()
    element_cell_0.vtk_cell = copy_vtk_cell(element_vtk_cell, element_grid_points)
    # super element id
    element_cell_0.super_id = super_element.id
    # super element cell
    element_cell_0.super_cell = super_element

    # element id 1
    element_cell_1 = NewElement3D(id_value=element_id_1)
    # element vtk cell
    element_vtk_cell: vtkCell = element_grid_1.GetCell(0)
    element_grid_points: vtkPoints = element_grid_1.GetPoints()
    element_cell_1.vtk_cell = copy_vtk_cell(element_vtk_cell, element_grid_points)
    # super element id
    element_cell_1.super_id = super_element.id
    # super element cell
    element_cell_1.super_cell = super_element

    # adjacent element id
    element_cell_0.adjacent_id = element_id_1
    element_cell_1.adjacent_id = element_id_0
    # adjacent element cell
    element_cell_0.adjacent_cell = element_cell_1
    element_cell_1.adjacent_cell = element_cell_0

    return element_cell_0, element_cell_1

