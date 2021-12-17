from NMM.fem.ElementCreator import ElementCreator
from NMM.fem.ElementBase import Element
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_creator = ElementCreator(database_cursor)
    temp_element_list = element_creator.run()
    temp_element: Element = temp_element_list[0]
    temp_list = [[2 * x - 2, 2 * x - 1] for x in temp_element.patch_id]
    temp_array = np.array(temp_list).reshape((1, -1))[0]
    row, column = np.meshgrid(temp_array, temp_array)
    row = row.reshape((1, -1))[0]
    column = column.reshape((1, -1))[0]
    value = temp_element.total_matrix.reshape((1, -1))[0]
