import numpy as np
from numpy.linalg import eigh
from NMM.base.ShapeCheckFuction import check_shape
from vtkmodules.vtkCommonDataModel import vtkCell, vtkLine


class Surface3D(object):
    def __init__(self, id_value):
        self.__id = id_value
        self.__vtkCell = None

        self.__element_id = [-1, -1]
        self.__element_cell_list = [None, None]

        self.__cracked = 0
        self.__crack_edge = None

        self.__edge_vector = np.array((0, 0, 0)).reshape(3)

    @property
    def element_id(self):
        assert len(self.__element_id) == 2
        return self.__element_id

    @property
    def element_cell_list(self):
        assert len(self.__element_cell_list) == 2
        return self.__element_cell_list

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
    def crack_edge(self):
        return self.__crack_edge

    @crack_edge.setter
    def crack_edge(self, crack_edge: vtkLine):
        if self.__cracked == 0:
            raise Exception('This surface has not been cracked!')
        self.__crack_edge = crack_edge

        temp_point_0 = crack_edge.GetPoints().GetPoint(0)
        temp_point_1 = crack_edge.GetPoints().GetPoint(1)
        temp_vector: np.ndarray = np.array(temp_point_0) - np.array(temp_point_1)
        self.__edge_vector = temp_vector.reshape(3)

    @property
    def edge_vector(self):
        return self.__edge_vector


class Element3D(object):
    def __init__(self, id_value):
        self.__id = id_value
        self.__vtkCell = None

        self.__surface_id = [-1, -1, -1, -1]
        self.__surface_cell_list = [None, None, None, None]

        self.__cracked = 0
        self.__crack_surface = None

        self.__strain_total = np.zeros((6, 1), dtype=np.float64)
        self.__strain = Tensor(np.zeros((6, 1), dtype=np.float64))

    @property
    def surface_id(self):
        assert len(self.__surface_id) == 4
        return self.__surface_id

    @property
    def surface_cell_list(self):
        assert len(self.__surface_cell_list) == 4
        return self.__surface_cell_list

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
    def strain_total(self):
        return self.__strain_total

    @strain_total.setter
    def strain_total(self, strain_total):
        strain_total = np.array(strain_total).reshape(6, 1)
        check_shape(strain_total, (6, 1))
        self.__strain_total = strain_total
        self.__strain = Tensor(self.__strain_total)

    @property
    def strain(self):
        return self.__strain

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
    def crack_surface(self):
        return self.__crack_surface

    @crack_surface.setter
    def crack_surface(self, crack_surface):
        if self.__cracked < 3:
            raise Exception('This element has not been cracked!')
        assert crack_surface is not None
        self.__crack_surface = crack_surface


class Tensor(object):
    def __init__(self, tensor_total):
        check_shape(tensor_total, (6, 1))
        self.__tensor_total = tensor_total

        # sigma(x) sigma(y) sigma(z) tau(xy) tau(xz) tau(yz)
        self.__xx = self.__tensor_total[0, 0]
        self.__yy = self.__tensor_total[1, 0]
        self.__zz = self.__tensor_total[2, 0]
        self.__xy = self.__tensor_total[3, 0]
        self.__xz = self.__tensor_total[4, 0]
        self.__yz = self.__tensor_total[5, 0]

        self.__matrix = np.matrix([[self.__xx, self.__xy, self.__xz],
                                   [self.__xy, self.__yy, self.__yz],
                                   [self.__xz, self.__yz, self.__zz]], dtype=np.float64)

        self.__eigenvalue_vector, self.__eigenvector_matrix = eigh(self.__matrix)

        self.__component_1 = [self.__eigenvalue_vector[0], self.__eigenvector_matrix[0]]
        self.__component_2 = [self.__eigenvalue_vector[1], self.__eigenvector_matrix[1]]
        self.__component_3 = [self.__eigenvalue_vector[2], self.__eigenvector_matrix[2]]

        def max_component(component_1, component_2):
            if component_1[0] > component_2[0]:
                return component_1
            else:
                return component_2

        self.__max_component = max_component(self.__component_1, self.__component_2)
        self.__max_component = max_component(self.__max_component, self.__component_3)

    @property
    def max_component(self):
        return self.__max_component


def schmidt_orthogonalization(vector_1, vector_2):
    # v1, v2
    vector_1 = np.array(vector_1).reshape(3)
    vector_2 = np.array(vector_2).reshape(3)
    result = vector_2 - (np.dot(vector_1, vector_2) / np.dot(vector_1, vector_1)) * vector_1
    return result


if __name__ == '__main__':
    v_1 = (0, 1, 1)
    v_2 = (1, 1, 0)

    print(schmidt_orthogonalization(v_1, v_2))
