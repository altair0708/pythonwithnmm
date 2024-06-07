import sqlite3
from typing import Dict


def add_a_relationship(file_name: str, table_name: str, record: Dict):
    with sqlite3.connect(file_name) as connection:
        entity_list = table_name.split('_')
        cursor = connection.cursor()
        database_statement = f'INSERT INTO {entity_list[0]}_{entity_list[1]} ' \
                             f'({entity_list[0]}_id, {entity_list[1]}_id)' \
                             f'VALUES ({record[entity_list[0]]}, {record[entity_list[1]]});'
        cursor.execute(database_statement)



