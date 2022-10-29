import numpy as np
from numpy.linalg import eigh
from NMM.base.ShapeCheckFuction import check_shape
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkCell, vtkTetra, vtkVertex, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


class CrackedElement3D(object):
    def __init__(self, id_value):
        self.__id = id_value
        self.__strain_total = np.zeros((6, 1), dtype=np.float64)
        self.__cracked = False
        self.__strain = Tensor(np.zeros((6, 1), dtype=np.float64))
        self.__vtkCell = None
        self.__center = None
        self.__crack_surface = None
        self.__crack_new = None

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
        return self.__cracked

    @cracked.setter
    def cracked(self, value):
        if isinstance(value, bool):
            self.__cracked = value
        else:
            raise Exception('cracked type error!!')

    @property
    def crack_new(self):
        return self.__crack_new

    @crack_new.setter
    def crack_new(self, value):
        self.__crack_new = value

    def generate_crack_surface(self):
        max_component = self.__strain.max_component
        max_direct = max_component[1]
        for each in range(3):
            if self.__center[each] != calculate_mass_center(self.__vtkCell)[each]:
                print(calculate_mass_center(self.__vtkCell))
                print(self.__center)
                print('center error!!!')
        self.__crack_surface = clip_a_vtk_cell(self.__vtkCell, self.__center, max_direct)

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
            raise Exception('clip error!!!')

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


def calculate_mass_center(vtk_cell: vtkCell):
    temp_cell: vtkCell = vtk_cell
    point_number = temp_cell.GetNumberOfPoints()
    point_list: vtkPoints = temp_cell.GetPoints()

    # calculate mass center
    x = 0
    y = 0
    z = 0
    for each_point in range(point_number):
        x = x + point_list.GetPoint(each_point)[0]
        y = y + point_list.GetPoint(each_point)[1]
        z = z + point_list.GetPoint(each_point)[2]
    center = np.array((x / point_number, y / point_number, z / point_number)).reshape((3, ))
    return center

if __name__ == '__main__':
    from tests3D.object.tetra_polyhedron import generate_tetra_polyhedron
    temp_tetra = generate_tetra_polyhedron(point_1=(1, -10, 1))
    print(calculate_mass_center(temp_tetra))
