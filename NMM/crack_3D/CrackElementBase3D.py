import sys
import numpy as np
from numpy.linalg import eigh
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.ShapeCheckFuction import check_shape
from NMM.base.ElementClipFunction import clip_a_vtk_cell, generate_crack_edge_surface, calculate_mass_center
from vtkmodules.vtkCommonDataModel import vtkCell, vtkTetra, vtkVertex, vtkUnstructuredGrid, vtkPolygon, vtkPlane, vtkPolyData
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


class CrackedElement3D(object):
    def __init__(self, id_value):
        self.__id = id_value
        self.__vtkCell = None
        self.__center = None

        self.__strain_total = np.zeros((6, 1), dtype=np.float64)
        self.__strain = Tensor(np.zeros((6, 1), dtype=np.float64))

        self.__cracked = 0
        self.__crack_edge_number = 0
        self.__crack_surface = None
        self.__crack_edge = ([], [], [], [])
        self.__adjacent_element = []

    @property
    def crack_edge_number(self):
        return self.__crack_edge_number

    @crack_edge_number.setter
    def crack_edge_number(self, number):
        self.__crack_edge_number = number

    @property
    def crack_edge(self):
        # the initial edge of crack generate by adjacent element
        return self.__crack_edge

    @property
    def adjacent_element(self):
        return self.__adjacent_element

    @adjacent_element.setter
    def adjacent_element(self, dictionary):
        self.__adjacent_element = dictionary

    @property
    def id(self):
        return self.__id

    @property
    def vtk_cell(self):
        return self.__vtkCell

    @vtk_cell.setter
    def vtk_cell(self, cell):
        self.__vtkCell: vtkCell = cell
        self.__center = calculate_mass_center(self.__vtkCell)

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
        return self.__cracked

    @cracked.setter
    def cracked(self, value):
        if isinstance(value, int):
            self.__cracked = value
        else:
            raise Exception('cracked type error!!')

    def generate_crack_surface(self):
        max_component = self.__strain.max_component
        max_direct = max_component[1]

        try:
            assert self.__crack_edge_number != 0
        except AssertionError:
            print(self.__id)
            print('____error_exit____')
            sys.exit()

        # todo: verify crack propagation direct
        if self.__crack_edge_number == 1:
            point_1 = self.__crack_edge[0][0]
            point_2 = self.__crack_edge[0][1]
            vector_1 = np.array(point_2) - np.array(point_1)
            vector_2 = np.array(max_direct).reshape(3)
            # normal_vector = schmidt_orthogonalization(vector_1, vector_2)
            normal_vector = (1, 0, -1)
        else:
            point_1 = self.__crack_edge[0][0]
            point_2 = self.__crack_edge[0][1]
            vector_1 = np.array(point_2) - np.array(point_1)
            point_1 = self.__crack_edge[1][0]
            point_2 = self.__crack_edge[1][1]
            vector_2 = np.array(point_2) - np.array(point_1)
            normal_vector = np.cross(vector_1, vector_2)
            assert np.linalg.norm(normal_vector) != 0
            # normal_vector = (0, 1, 0)

        origin_point = self.__crack_edge[0][0]
        try:
            self.__crack_surface, _, _ = clip_a_vtk_cell(self.__vtkCell, origin_point, normal_vector)
        except AssertionError:
            print(self.__id)
            tetra_1 = vtkTetra()
            tetra_1.GetPointIds().SetId(0, 0)
            tetra_1.GetPointIds().SetId(1, 1)
            tetra_1.GetPointIds().SetId(2, 2)
            tetra_1.GetPointIds().SetId(3, 3)

            vertex_1 = vtkVertex()
            vertex_1.GetPointIds().SetId(0, 4)

            vertex_2 = vtkVertex()
            vertex_2.GetPointIds().SetId(0, 5)

            error_points = vtkPoints()
            error_points.DeepCopy(self.__vtkCell.GetPoints())
            error_points.InsertNextPoint(self.__crack_edge[0][0])
            error_points.InsertNextPoint(self.__crack_edge[0][1])

            plane = vtkPlaneSource()
            plane.SetCenter(origin_point)
            plane.SetNormal(normal_vector)
            plane.Update()
            plane_poly_data: vtkPolyData = plane.GetOutput()
            plane_cell = plane_poly_data.GetCell(0)

            error_grid = vtkUnstructuredGrid()
            error_grid.InsertNextCell(tetra_1.GetCellType(), tetra_1.GetPointIds())
            error_grid.InsertNextCell(vertex_1.GetCellType(), vertex_1.GetPointIds())
            error_grid.InsertNextCell(vertex_2.GetCellType(), vertex_2.GetPointIds())
            error_grid.SetPoints(error_points)
            insert_a_cell(error_grid, plane_cell)

            writer = vtkXMLUnstructuredGridWriter()
            writer.SetInputData(error_grid)
            writer.SetFileName('error.vtu')
            writer.Write()
            self.__cracked = 0

    @property
    def crack_surface(self):
        return self.__crack_surface

    @crack_surface.setter
    def crack_surface(self, crack_surface):
        if self.__cracked < 3:
            raise Exception('This element has not been cracked!')
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
