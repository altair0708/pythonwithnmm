from NMM.fem.ElementWithDataBase import get_one_special_point
import sqlite3

database_name = '../data/test03.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    a = get_one_special_point(id_value=4, cursor=database_cursor)
    print(a)

