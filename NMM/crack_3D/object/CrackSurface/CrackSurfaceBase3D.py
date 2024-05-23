from NMM.crack_3D.ObjectBase3D import ObjectBase3D
from NMM.GlobalVariable import DataStructure
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints


class CrackSurface3D(ObjectBase3D):
    def __init__(self, id_value):
        super().__init__(id_value)

        self.__element_id = [-1]
        self.__element_cell_list = [None]

        self.__crack_edge_id = [-1, -1, -1, -1]
        self.__crack_edge_cell_list = [None, None, None, None]

    @property
    def element_id(self):
        assert len(self.__element_id) == 1
        return self.__element_id

    @property
    def element_cell_list(self):
        assert len(self.__element_cell_list) == 1
        return self.__element_cell_list

    @property
    def crack_edge_id(self):
        assert len(self.__crack_edge_id) == 4
        return self.__crack_edge_id

    @property
    def crack_edge_cell_list(self):
        assert len(self.__crack_edge_cell_list) == 4
        return self.__crack_edge_cell_list

    @property
    def normal_vector(self):
        points: vtkPoints = self.vtk_cell.GetPoints()
        normal_vector = [0, 0, 0]
        vtkPolygon.ComputeNormal(points, normal_vector)
        return normal_vector

    @property
    def type(self):
        return self.vtk_cell.GetCellType()


def create_a_crack_surface(data_structure: DataStructure, crack_surface_id: int):

    # vtk crack surface model
    crack_surface_grid: vtkUnstructuredGrid = data_structure.crack_surface.content

    # assemble a crack element
    crack_surface_cell = CrackSurface3D(id_value=crack_surface_id)

    # vtk_cell
    crack_surface_vtk_cell: vtkCell = crack_surface_grid.GetCell(crack_surface_id)
    crack_surface_grid_points: vtkPoints = crack_surface_grid.GetPoints()
    crack_surface_cell.vtk_cell = copy_vtk_cell(crack_surface_vtk_cell, crack_surface_grid_points)

    # element id
    element_id_list = get_property(crack_surface_grid, 'element_id', crack_surface_id)
    for i, each_element_id in enumerate(element_id_list):
        crack_surface_cell.element_id[i] = int(each_element_id)

    # crack edge id
    crack_edge_id_list = get_property(crack_surface_grid, 'edge_id', crack_surface_id)
    for i, edge_id in enumerate(crack_edge_id_list):
        edge_id = int(edge_id)
        crack_surface_cell.crack_edge_id[i] = edge_id

    return crack_surface_cell
