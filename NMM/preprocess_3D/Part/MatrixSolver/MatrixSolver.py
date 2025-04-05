import numpy as np
from NMM.base.Part.Part import Part
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve, cg, lsmr, lsqr, gmres, aslinearoperator


class MatrixSolver(Part):
    def __init__(self):
        super(MatrixSolver, self).__init__()

        self.name = 'matrix_solver'
        self.__cover_number = 0

        self.__total_row = np.array([[]], dtype=np.int32)
        self.__total_column = np.array([[]], dtype=np.int32)
        self.__total_value = np.array([[]], dtype=np.float64)
        self.__stiff_matrix = coo_matrix((3 * self.__cover_number, 3 * self.__cover_number), dtype=np.float64)
        self.__force_vector = np.zeros(3 * self.__cover_number, dtype=np.float64)

        self.__displacement_vector = None
        self.__exit_code = None

    def reset(self):
        self.__total_row = np.array([[]], dtype=np.int32)
        self.__total_column = np.array([[]], dtype=np.int32)
        self.__total_value = np.array([[]], dtype=np.float64)
        self.__stiff_matrix = coo_matrix((3 * self.__cover_number, 3 * self.__cover_number), dtype=np.float64)
        self.__force_vector = np.zeros(3 * self.__cover_number, dtype=np.float64)

        self.__displacement_vector = None
        self.__exit_code = None

    @property
    def cover_number(self):
        return self.__cover_number

    @cover_number.setter
    def cover_number(self, value):
        self.__cover_number = value
        self.reset()

    def add_element_matrix(self, element: ElementBase):
        temp_list = [[3 * x, 3 * x + 1, 3 * x + 2] for x in element.get_property('math_cover_id')]
        temp_array = np.array(temp_list, dtype=np.int32).reshape((1, -1))[0]
        row, column = np.meshgrid(temp_array, temp_array)
        row = row.reshape((1, -1))
        column = column.reshape((1, -1))
        value = np.array(element.get_property('total_matrix'), dtype=np.float64).reshape((1, -1))
        self.__total_row = np.c_[self.__total_row, row]
        self.__total_column = np.c_[self.__total_column, column]
        self.__total_value = np.c_[self.__total_value, value]

    def add_force_vector(self, element: ElementBase):
        # force vector
        temp_vector = np.zeros(3 * self.__cover_number, dtype=np.float64)
        for step, each_location in enumerate(element.get_property('math_cover_id')):
            temp_vector[3 * each_location] = element.get_property('total_force')[3 * step][0]
            temp_vector[3 * each_location + 1] = element.get_property('total_force')[3 * step + 1][0]
            temp_vector[3 * each_location + 2] = element.get_property('total_force')[3 * step + 2][0]
        self.__force_vector = self.__force_vector + temp_vector

    def solve_conjugate_gradient(self):
        self.__total_row = self.__total_row.astype('int32')
        self.__total_column = self.__total_column.astype('int32')
        self.__stiff_matrix = coo_matrix((self.__total_value[0], (self.__total_row[0], self.__total_column[0])), dtype=np.float64)
        self.__stiff_matrix = self.__stiff_matrix.tocsc()

        assert self.__stiff_matrix.shape == (3 * self.__cover_number, 3 * self.__cover_number)
        assert self.__force_vector.shape == (3 * self.__cover_number)
        print('\rstiff matrix assembled complete!')

        self.__displacement_vector, self.__exit_code = cg(self.__stiff_matrix, self.__force_vector, tol=1e-15, atol=0.01)


class MatrixAssembler3D:
    @staticmethod
    def stiff_matrix(element_list, math_cover_number):
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
            print('\rstiff matrix assembled : {}%'.format(element_id * 100/len(element_list)), end='')
        temp_total_row = temp_total_row.astype('int32')
        temp_total_column = temp_total_column.astype('int32')
        temp_stiff_matrix = coo_matrix((temp_total_value[0], (temp_total_row[0], temp_total_column[0])), dtype=np.float64)
        temp_stiff_matrix = temp_stiff_matrix.tocsc()
        if temp_stiff_matrix.shape != (3 * math_cover_number, 3 * math_cover_number):
            raise Exception('stiff matrix shape don\'t equal patch number')
        print('\rstiff matrix assembled complete!')
        return temp_stiff_matrix

    @staticmethod
    def force_vector(element_list, math_cover_number):

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

