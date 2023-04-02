from NMM.crack_3D.ObjectBase3D import ObjectBase3D
from NMM.GlobalVariable import DataStructure
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell
from vtkmodules.vtkCommonCore import vtkPoints


class CrackEdge3D(ObjectBase3D):
    def __init__(self, id_value):
        super().__init__(id_value)

        self.__surface_id = [-1]
        self.__surface_cell_list = [None]

        self.__crack_surface_id = [-1, -1]
        self.__crack_surface_cell_list = [None, None]

    @property
    def surface_id(self):
        assert len(self.__surface_id) == 1
        return self.__surface_id

    @property
    def surface_cell_list(self):
        assert len(self.__surface_cell_list) == 1
        return self.__surface_cell_list

    @property
    def crack_surface_id(self):
        assert len(self.__crack_surface_id) == 2
        return self.__crack_surface_id

    @property
    def crack_surface_cell_list(self):
        assert len(self.__crack_surface_cell_list) == 2
        return self.__crack_surface_cell_list

    @property
    def vector(self):
        points: vtkPoints = self.vtk_cell.GetPoints()
        point_0 = points.GetPoint(0)
        point_1 = points.GetPoint(1)
        vector = (point_1[0] - point_0[0], point_1[1] - point_0[1], point_1[2] - point_0[2])
        return vector



def create_a_crack_edge(data_structure: DataStructure, crack_edge_id: int):

    # vtk crack edge model
    crack_edge_grid: vtkUnstructuredGrid = data_structure.crack_edge.content

    # assemble a crack element
    crack_edge_cell = CrackEdge3D(id_value=crack_edge_id)

    # vtk_cell
    crack_edge_vtk_cell: vtkCell = crack_edge_grid.GetCell(crack_edge_id)
    crack_edge_grid_points: vtkPoints = crack_edge_grid.GetPoints()
    crack_edge_cell.vtk_cell = copy_vtk_cell(crack_edge_vtk_cell, crack_edge_grid_points)

    # surface id
    surface_id_list = get_property(crack_edge_grid, 'surface_id', crack_edge_id)
    for i, each_surface_id in enumerate(surface_id_list):
        crack_edge_cell.surface_id[i] = int(each_surface_id)

    # crack surface id
    crack_surface_id_list = get_property(crack_edge_grid, 'crack_surface_id', crack_edge_id)
    for i, each_crack_surface_id in enumerate(crack_surface_id_list):
        crack_edge_cell.crack_surface_id[i] = int(each_crack_surface_id)

    return crack_edge_cell
