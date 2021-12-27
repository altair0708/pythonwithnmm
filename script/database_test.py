import sqlite3

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    database_statement = 'SELECT * FROM PhysicalPatches WHERE (xValue, yValue) in ' \
                         '(SELECT xValue, yValue FROM PhysicalPatches GROUP BY xValue, yValue HAVING COUNT(*) > 1)'

    result = database_cursor.execute(database_statement)
    result = result.fetchall()
    for each_patch in result:
        print(each_patch)

