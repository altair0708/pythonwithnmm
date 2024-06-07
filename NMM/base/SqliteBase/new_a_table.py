import sqlite3


def new_a_table(file_name: str, table_name: str):
    entity_list = table_name.split('_')
    assert len(entity_list) == 2

    with sqlite3.connect(file_name) as connection:
        cursor = connection.cursor()
        database_statement = f'CREATE TABLE {entity_list[0]}_{entity_list[1]}(' \
                             f'id                  INTEGER PRIMARY KEY AUTOINCREMENT ,' \
                             f'{entity_list[0]}_id INT                 NOT NULL,' \
                             f'{entity_list[1]}_id INT                 NOT NULL);'

        cursor.execute(database_statement)
