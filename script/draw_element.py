import matplotlib.pyplot as plt
import time
from NMM.fem.ElementBase import *
from NMM.fem.ElementCreator import *

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_number = get_element_number(cursor=database_cursor)
    id_list = [8, 23, 34, 89, 93]
    for each_id in range(1, element_number + 1):
        element = create_an_element(id_value=each_id, cursor=database_cursor)
        element.draw_edge()
        element.draw_patch()
    plt.show()
    plt.clf()
