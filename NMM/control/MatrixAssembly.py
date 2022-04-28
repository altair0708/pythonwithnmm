import sqlite3
import numpy as np
from NMM.fem.PatchWithDataBase import get_patch_number
from scipy.sparse import coo_matrix


class MatrixAssembler:
    @staticmethod
    def stiff_matrix(element_list, cursor: sqlite3.Cursor):
        patch_number = get_patch_number(cursor)
        temp_stiff_matrix = coo_matrix((2 * patch_number, 2 * patch_number), dtype=np.float64)
        temp_total_row = np.array([[]], dtype=np.int32)
        temp_total_column = np.array([[]], dtype=np.int32)
        temp_total_value = np.array([[]], dtype=np.float64)
        for temp_element in element_list:
            # stiff matrix
            temp_list = [[2 * x - 2, 2 * x - 1] for x in temp_element.patch_id]
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
        if temp_stiff_matrix.shape != (2 * patch_number, 2 * patch_number):
            raise Exception('stiff matrix shape don\'t equal patch number')
        return temp_stiff_matrix

    @staticmethod
    def force_vector(element_list, cursor: sqlite3.Cursor):
        patch_number = get_patch_number(cursor)
        force_vector = np.zeros(2 * patch_number, dtype=np.float64)
        for temp_element in element_list:
            # force vector
            temp_vector = np.zeros(2 * patch_number, dtype=np.float64)
            for step, each_location in enumerate(temp_element.patch_id):
                temp_vector[2 * each_location - 2] = temp_element.total_force[2 * step][0]
                temp_vector[2 * each_location - 1] = temp_element.total_force[2 * step + 1][0]
            force_vector = force_vector + temp_vector
        return force_vector
