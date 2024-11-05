import sqlite3


def exist_a_table(table_name: str, file_name: str):
    with sqlite3.connect(file_name) as connection:
        cursor = connection.cursor()
        database_statement = f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table_name}';"
        cursor.execute(database_statement)
        result = cursor.fetchone()

    if result:
        return True
    else:
        return False


def exist_a_table_with_connection(table_name: str, connection):

    cursor = connection.cursor()
    database_statement = f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table_name}';"
    cursor.execute(database_statement)
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
