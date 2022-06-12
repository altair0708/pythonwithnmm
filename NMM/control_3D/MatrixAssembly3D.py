import numpy as np
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from scipy.sparse import coo_matrix


class MatrixAssembler3D:
    @staticmethod
    def stiff_matrix(element_list, math_cover_file):
        uGridReader = vtkXMLUnstructuredGridReader()
        uGridReader.SetFileName(math_cover_file)
        uGridReader.Update()
        gmshGrid: vtkUnstructuredGrid = uGridReader.GetOutput()
        math_cover_number = gmshGrid.GetNumberOfCells()

        temp_stiff_matrix = coo_matrix((3 * math_cover_number, 3 * math_cover_number), dtype=np.float64)
        temp_total_row = np.array([[]], dtype=np.int32)
        temp_total_column = np.array([[]], dtype=np.int32)
        temp_total_value = np.array([[]], dtype=np.float64)

        for element_id, temp_element in enumerate(element_list):
            # stiff matrix
            temp_list = [[3 * x, 3 * x + 1, 3 * x + 2] for x in temp_element.patch_id]
            temp_array = np.array(temp_list, dtype=np.int32).reshape((1, -1))[0]
            row, column = np.meshgrid(temp_array, temp_array)
            row = row.reshape((1, -1))
            column = column.reshape((1, -1))
            value = np.array(temp_element.total_matrix, dtype=np.float64).reshape((1, -1))
            temp_total_row = np.c_[temp_total_row, row]
            temp_total_column = np.c_[temp_total_column, column]
            temp_total_value = np.c_[temp_total_value, value]
            temp_total_row = temp_total_row.astype('int32')
            temp_total_column = temp_total_column.astype('int32')
            temp_stiff_matrix = coo_matrix((temp_total_value[0], (temp_total_row[0], temp_total_column[0])), dtype=np.float64)
            temp_stiff_matrix = temp_stiff_matrix.tocsc()
            print('\rstiff matrix assembled : {}%'.format(element_id * 100/len(element_list)), end='')
        if temp_stiff_matrix.shape != (3 * math_cover_number, 3 * math_cover_number):
            raise Exception('stiff matrix shape don\'t equal patch number')
        print('\rstiff matrix assembled complete!')
        return temp_stiff_matrix

    @staticmethod
    def force_vector(element_list, math_cover_file):
        uGridReader = vtkXMLUnstructuredGridReader()
        uGridReader.SetFileName(math_cover_file)
        uGridReader.Update()
        gmshGrid: vtkUnstructuredGrid = uGridReader.GetOutput()
        math_cover_number = gmshGrid.GetNumberOfCells()

        force_vector = np.zeros(3 * math_cover_number, dtype=np.float64)
        for temp_element in element_list:
            # force vector
            temp_vector = np.zeros(3 * math_cover_number, dtype=np.float64)
            for step, each_location in enumerate(temp_element.patch_id):
                temp_vector[3 * each_location] = temp_element.total_force[3 * step][0]
                temp_vector[3 * each_location + 1] = temp_element.total_force[3 * step + 1][0]
                temp_vector[3 * each_location + 2] = temp_element.total_force[3 * step + 2][0]
            force_vector = force_vector + temp_vector
        print('force vector assembled complete!')
        return force_vector

