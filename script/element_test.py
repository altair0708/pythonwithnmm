import matplotlib.pyplot as plt

from NMM.fem.ElementBase import *
import sqlite3
import numpy as np
import time

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_number = get_element_number(database_cursor)
    element = create_an_element(1, database_cursor)
    element.draw_patch()
    a = element.stiff_matrix
    b = element.initial_matrix
    c = element.loading_matrix
    print(a)
    print(b)
    print(c)
