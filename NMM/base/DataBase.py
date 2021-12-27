import sqlite3
import numpy as np


def insert_a_rows(table_name: str, data: list, database_cursor: sqlite3.Cursor = None):
    value_line = '('
    for each_value in data:
        if type(each_value) != str:
            value_line = value_line + str(each_value) + ', '
        else:
            value_line = value_line + '\'' + str(each_value) + '\', '
    value_line = value_line[:-2]
    value_line = value_line + ')'
    sql_statement = 'INSERT INTO {table} VALUES {values}'.format(table=table_name, values=value_line)
    database_cursor.execute(sql_statement)


def query_by_id(table_name: str, id_number: int = 1, database_cursor: sqlite3.Cursor = None):
    sql_statement = 'SELECT * FROM {table} WHERE ID = {id}'.format(table=table_name, id=id_number)
    data = database_cursor.execute(sql_statement)
    data = data.fetchall()
    return data


def delete_all_tables(database_cursor: sqlite3.Cursor = None):
    table_name_list = database_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name_list = table_name_list.fetchall()
    for table_name in table_name_list:
        sql_statement = 'DROP TABLE {name};'.format(name=table_name[0])
        database_cursor.execute(sql_statement)


def create_a_table(table_name: str, table_column: dict):
    pass


def query_by_column(table_name: str, column_name: str, column_value, database_cursor: sqlite3.Cursor = None):
    sql_statement = 'SELECT * FROM {table} WHERE {column} = {value}'.format(table=table_name, column=column_name, value=column_value)
    data = database_cursor.execute(sql_statement)
    data = data.fetchall()
    return data


if __name__ == '__main__':
    data_list = [1, 2, 3, 4]
    table_name1 = 'SpecialPoints'
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE SpecialPoints('
                   'ID        INT  PRIMARY KEY          NOT NULL,'
                   'xValue    REAL DEFAULT 0            NOT NULL,'
                   'yValue    REAL DEFAULT 0            NOT NULL,'
                   'elementID INT  DEFAULT 0            NOT NULL);')
    cursor.execute('CREATE TABLE SpecialPoint1('
                   'ID        INT  PRIMARY KEY          NOT NULL,'
                   'xValue    REAL DEFAULT 0            NOT NULL,'
                   'yValue    REAL DEFAULT 0            NOT NULL,'
                   'elementID INT  DEFAULT 0            NOT NULL);')
    a = cursor.execute('SELECT name FROM sqlite_master;')
    a = a.fetchall()
    print(a)
    delete_all_tables(cursor)
    a = cursor.execute('SELECT name FROM sqlite_master;')
    a = a.fetchall()
    print(a)
    connection.close()
