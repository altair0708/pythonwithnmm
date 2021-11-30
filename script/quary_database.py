from NMM.base.DataBase import query_by_id, query_by_column
import sqlite3

database_name = '../data/test.db'
connect = sqlite3.connect(database_name)
cursor = connect.cursor()
a = query_by_column(table_name='ContactLoops', column_name='loopID', column_value=1, database_cursor=cursor)
print(a)
