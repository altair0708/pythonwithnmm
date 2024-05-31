from NMM.crack_3D.ObjectBase3D import ObjectBase3D
from NMM.GlobalVariable import DataStructure, Variable
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_polyhedron, copy_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


class Surface3D(ObjectBase3D):
    def __init__(self, id_value):
        super().__init__(id_value)

        self.__element_id = [-1, -1]
        self.__element_cell_list = [None, None]

        self.__cracked = 0
        self.__crack_edge_id = [-1]
        self.__crack_edge_cell_list = [None]

    @property
    def element_id(self):
        assert len(self.__element_id) == 2
        return self.__element_id

    @property
    def element_cell_list(self):
        assert len(self.__element_cell_list) == 2
        return self.__element_cell_list

    @property
    def cracked(self):
        # check the surface crack status
        # 0: do not have a crack edge
        # 1: have been crack in this step
        # 2: have been crack in previous step
        # 9: initial crack surface
        return self.__cracked

    @cracked.setter
    def cracked(self, value):
        if isinstance(value, int):
            self.__cracked = value
        else:
            raise Exception('cracked type error!!')

    @property
    def crack_edge_id(self):
        assert len(self.__crack_edge_id) == 1
        return self.__crack_edge_id

    @property
    def crack_edge_cell_list(self):
        assert len(self.__crack_edge_cell_list) == 1
        return self.__crack_edge_cell_list

    @property
    def normal_vector(self):
        points: vtkPoints = self.vtk_cell.GetPoints()
        normal_vector = [0, 0, 0]
        vtkPolygon.ComputeNormal(points, normal_vector)
        return normal_vector


def create_a_surface(data_structure: DataStructure, surface_id: int):

    # vtk element surface Model
    surface_grid: vtkUnstructuredGrid = data_structure.element_surface.content

    # assemble a surface
    surface_cell = Surface3D(surface_id)

    # cracked flag
    surface_cracked_flag = get_property(surface_grid, 'cracked', surface_id)
    surface_cell.cracked = int(surface_cracked_flag[0])

    # crack edge id
    if surface_cell.cracked == 2 or surface_cell.cracked == 9:

        edge_id = get_property(surface_grid, 'edge_id', surface_id)
        edge_id = int(edge_id[0])
        surface_cell.crack_edge_id[0] = edge_id

    # vtk_cell
    surface_vtk_cell: vtkCell = surface_grid.GetCell(surface_id)
    surface_grid_points: vtkPoints = surface_grid.GetPoints()
    surface_cell.vtk_cell = copy_vtk_cell(surface_vtk_cell, surface_grid_points)

    # element id
    element_id_list = get_property(surface_grid, 'element_id', surface_id)
    for i, each_element_id in enumerate(element_id_list):
        surface_cell.element_id[i] = int(each_element_id)

    return surface_cell

