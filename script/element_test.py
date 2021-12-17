import matplotlib.pyplot as plt
import sqlite3
from NMM.GlobalVariable import *
from NMM.fem.ElementCreator import create_an_element
from NMM.fem.ElementWithDataBase import get_element_number

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_number = get_element_number(database_cursor)
    element_list = []
    for each_id in range(1, element_number + 1):
        element = create_an_element(each_id, database_cursor)
        a = element.stiff_matrix
        b = element.initial_matrix
        c = element.loading_matrix
        d = element.body_matrix
        e, f = element.mass_matrix
        g = element.fixed_matrix
        element_list.append(element)
        # print(a)
        # print(b)
        print('loading matrix: {}'.format(c))
        # print(d)
        # print(e)
        # print(f)
        print('fixed matrix: {}'.format(g))
