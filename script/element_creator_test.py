from NMM.fem.ElementCreator import ElementCreator
from NMM.fem.ElementBase import Element
from NMM.fem.PatchWithDataBase import get_patch_number
from scipy.sparse import *
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_creator = ElementCreator(database_cursor)
    temp_element_list = element_creator.run()
    patch_number = get_patch_number(database_cursor)
    total_row = np.array([[]])
    total_column = np.array([[]])
    total_value = np.array([[]])
    for temp_element in temp_element_list:
        temp_list = [[2 * x - 2, 2 * x - 1] for x in temp_element.patch_id]
        temp_array = np.array(temp_list, dtype=np.int32).reshape((1, -1))[0]
        row, column = np.meshgrid(temp_array, temp_array)
        row = row.reshape((1, -1))
        column = column.reshape((1, -1))
        value = np.array(temp_element.total_matrix).reshape((1, -1))
        total_row = np.c_[total_row, row]
        total_column = np.c_[total_column, column]
        total_value = np.c_[total_value, value]

    total_row = total_row.astype('int32')
    total_column = total_column.astype('int32')
    stiff_matrix = coo_matrix((total_value[0], (total_row[0], total_column[0])), dtype=np.float32)
    print(stiff_matrix.shape)
