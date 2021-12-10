from NMM.base.DataBase import query_by_id, query_by_column
from NMM.fem.ElementWithDataBase import *
import sqlite3

database_name = '../data/test.db'
connect = sqlite3.connect(database_name)
cursor = connect.cursor()
a = get_one_element(id_value=1, cursor=cursor)
print(a)
