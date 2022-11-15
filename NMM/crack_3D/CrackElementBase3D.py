import numpy as np
from numpy.linalg import eigh
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.ShapeCheckFuction import check_shape
from NMM.base.ElementClipFunction import clip_a_vtk_cell, generate_crack_edge_surface, calculate_mass_center
from vtkmodules.vtkCommonDataModel import vtkCell, vtkTetra, vtkVertex, vtkUnstructuredGrid, vtkPolygon, vtkPlane
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
        self.__crack_surface = None
        self.__crack_edge = []
        self.__adjacent_element = []

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
        # 1: not cracked but have choice to crack
        # 2: have been crack in this step
        # 3: have been crack in previous step
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

        point_1 = self.__crack_edge[0]
        point_2 = self.__crack_edge[1]

        vector_1 = np.array(point_2) - np.array(point_1)
        vector_2 = np.array(max_direct).reshape(3)

        # todo: verify crack propagation direct
        normal_vector = schmidt_orthogonalization(vector_1, vector_2)
        # normal_vector = (0, 1, 0)
        if self.__id == 18:
            normal_vector = (0, 1, 0)
            point_1 = self.__center
        self.__crack_surface, grid_1, grid_2 = clip_a_vtk_cell(self.__vtkCell, point_1, normal_vector)

        # if self.__id == 29:
        #     writer = vtkXMLUnstructuredGridWriter()
        #     writer.SetFileName('error_1.vtu')
        #     writer.SetInputData(grid_1)
        #     writer.Write()
        #
        #     writer = vtkXMLUnstructuredGridWriter()
        #     writer.SetFileName('error_2.vtu')
        #     writer.SetInputData(grid_2)
        #     writer.Write()
        #
        #     grid_3 = vtkUnstructuredGrid()
        #     grid_3.SetPoints(self.__crack_surface.GetPoints())
        #     grid_3.InsertNextCell(self.__crack_surface.GetCellType(), self.__crack_surface.GetPointIds())
        #     writer = vtkXMLUnstructuredGridWriter()
        #     writer.SetFileName('error_3.vtu')
        #     writer.SetInputData(grid_3)
        #     writer.Write()
        # for each in range(3):
        #     if self.__center[each] != calculate_mass_center(self.__vtkCell)[each]:
        #         print(calculate_mass_center(self.__vtkCell))
        #         print(self.__center)
        #         print('center error!!!')
        # print('##########cell_points#################')
        # print(self.__vtkCell.GetPoints().GetPoint(0))
        # print(self.__vtkCell.GetPoints().GetPoint(1))
        # print(self.__vtkCell.GetPoints().GetPoint(2))
        # print(self.__vtkCell.GetPoints().GetPoint(3))
        # print('##########center#################')
        # print(self.__center)
        # print('##########direct#################')
        # print(max_direct)
        # print('#################################')

        if self.__crack_surface is None:
            print(self.__vtkCell.GetNumberOfPoints())
            print(self.__id)
            tetra_1 = vtkTetra()
            tetra_1.GetPointIds().SetId(0, 0)
            tetra_1.GetPointIds().SetId(1, 1)
            tetra_1.GetPointIds().SetId(2, 2)
            tetra_1.GetPointIds().SetId(3, 3)

            vertex_1 = vtkVertex()
            vertex_1.GetPointIds().SetId(0, 4)

            error_points = vtkPoints()
            error_points.DeepCopy(self.__vtkCell.GetPoints())
            error_points.InsertNextPoint(self.__center)

            error_grid = vtkUnstructuredGrid()
            error_grid.InsertNextCell(tetra_1.GetCellType(), tetra_1.GetPointIds())
            error_grid.InsertNextCell(vertex_1.GetCellType(), vertex_1.GetPointIds())
            error_grid.SetPoints(error_points)

            writer = vtkXMLUnstructuredGridWriter()
            writer.SetInputData(error_grid)
            writer.SetFileName('error.vtu')
            writer.Write()

        generate_crack_edge_surface(self.__adjacent_element, self.__crack_surface)

    @property
    def crack_surface(self):
        return self.__crack_surface


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
