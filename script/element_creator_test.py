from NMM.fem.ElementCreator import ElementCreator
import sqlite3
import matplotlib.pyplot as plt

for database_id in range(1, 16):
    database_name = '../data/test{database_id}.db'.format(database_id=str(database_id).rjust(2, '0'))
    with sqlite3.connect(database_name) as connection:
        database_cursor = connection.cursor()
        element_creator = ElementCreator(database_cursor)
        temp_list = element_creator.run()
        for each_element in temp_list:
            each_element.draw_edge()
            each_element.draw_patch()
        plt.show()


