import numpy as np
from NMM.base.ShapeCheckFuction import check_shape
from NMM.crack_3D.ObjectBase3D import ObjectBase3D
from NMM.GlobalVariable import DataStructure, Variable
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_polyhedron, copy_vtk_cell
from NMM.base.TensorBase import Tensor
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


class Element3D(ObjectBase3D):
    def __init__(self, id_value):
        super().__init__(id_value)

        self.__surface_id = [-1, -1, -1, -1]
        self.__surface_cell_list = [None, None, None, None]

        self.__cracked = 0
        self.__crack_surface_id = [-1, -1]
        self.__crack_surface_cell_list = [None, None]

        self.__strain_total = np.zeros((6, 1), dtype=np.float64)
        self.__strain = Tensor(np.zeros((6, 1), dtype=np.float64))

        self.__stress_total = np.zeros((6, 1), dtype=np.float64)
        self.__stress = Tensor(np.zeros((6, 1), dtype=np.float64))

    @property
    def surface_id(self):
        assert len(self.__surface_id) == 4
        return self.__surface_id

    @property
    def surface_cell_list(self):
        assert len(self.__surface_cell_list) == 4
        return self.__surface_cell_list

    @property
    def cracked(self):
        # check the element crack status
        # 0: not cracked and have no choice to crack
        # 1: not cracked, adjacent element has been cracked this time step(status 3), unable to cracked.
        # 2: not cracked, adjacent element has been cracked previous time step(status 4), be able to cracked.
        # 3: have been crack in this step
        # 4: have been crack in previous step
        # 9: initial crack surface
        return self.__cracked

    @cracked.setter
    def cracked(self, value):
        if isinstance(value, int):
            self.__cracked = value
        else:
            raise Exception('cracked type error!!')

    @property
    def crack_surface_id(self):
        assert len(self.__crack_surface_id) == 2
        return self.__crack_surface_id

    @property
    def crack_surface_cell_list(self):
        assert len(self.__crack_surface_cell_list) == 2
        return self.__crack_surface_cell_list

    @property
    def strain_total(self):
        return self.__strain_total

    @strain_total.setter
    def strain_total(self, strain_total):
        strain_total = np.array(strain_total).reshape(6, 1)
        check_shape(strain_total, (6, 1))
        strain_total[3][0] = strain_total[3][0] / 2
        strain_total[4][0] = strain_total[4][0] / 2
        strain_total[5][0] = strain_total[5][0] / 2
        self.__strain_total = strain_total
        self.__strain = Tensor(self.__strain_total)

    @property
    def strain(self):
        return self.__strain

    @property
    def stress_total(self):
        return self.__stress_total

    @stress_total.setter
    def stress_total(self, stress_total):
        stress_total = np.array(stress_total).reshape(6, 1)
        self.__stress_total = stress_total
        self.__stress = Tensor(self.__stress_total)

    @property
    def stress(self):
        return self.__stress


def schmidt_orthogonalization(vector_1, vector_2):
    # v1, v2
    vector_1 = np.array(vector_1).reshape(3)
    vector_2 = np.array(vector_2).reshape(3)
    result = vector_2 - (np.dot(vector_1, vector_2) / np.dot(vector_1, vector_1)) * vector_1
    return result


def create_an_element(data_structure: DataStructure, element_id: int):

    # vtk element Model
    element_grid: vtkUnstructuredGrid = data_structure.manifold_element.content

    # assemble a crack element
    element_cell = Element3D(id_value=element_id)

    # strain_total
    element_cell.strain_total = get_property(element_grid, 'strain_total', element_id)

    # stress_total
    element_cell.stress_total = get_property(element_grid, 'stress_total', element_id)

    # vtk_cell
    element_vtk_cell: vtkCell = element_grid.GetCell(element_id)
    element_grid_points: vtkPoints = element_grid.GetPoints()
    element_cell.vtk_cell = copy_polyhedron(element_vtk_cell, element_grid_points)

    # element surface
    surface_id_list = get_property(element_grid, 'surface_id', element_id)
    for i, each_surface_id in enumerate(surface_id_list):
        element_cell.surface_id[i] = int(each_surface_id)

    # cracked flag
    element_cracked_flag = get_property(element_grid, 'cracked', element_id)
    element_cell.cracked = int(element_cracked_flag[0])

    # crack surface
    if element_cell.cracked == 9 or element_cell.cracked == 4:
        crack_surface_id_list = get_property(element_grid, 'crack_surface_id', element_id)
        for i, each_crack_surface_id in enumerate(crack_surface_id_list):
            element_cell.crack_surface_id[i] = int(each_crack_surface_id)

    return element_cell


if __name__ == '__main__':
    v_1 = (0, 1, 1)
    v_2 = (1, 1, 0)

    print(schmidt_orthogonalization(v_1, v_2))
