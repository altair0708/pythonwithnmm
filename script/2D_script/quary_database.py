import sqlite3

database_name = '../data/test.db'
with sqlite3.connect(database_name) as database_connect:
    database_cursor = database_connect.cursor()
    result = database_cursor.execute('SELECT * FROM JointPoints WHERE ID = 1')
    result = result.fetchall()
    print(result)
