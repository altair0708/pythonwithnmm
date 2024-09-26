import sqlite3


def select_a_relationship(file_name: str, table_name: str, entity_name: str, entity_id: int):
    with sqlite3.connect(file_name) as connection:
        entity_list = table_name.split('_')
        assert len(entity_list) == 2
        goal_entity_name = entity_list.remove(entity_name)[0]
        cursor = connection.cursor()
        database_statement = f'SELECT {entity_name}_id,{goal_entity_name}_id' \
                             f'FROM {table_name}' \
                             f'WHERE {entity_name}_id = {entity_id}'
        cursor.execute(database_statement)

        result_relationship = []
        result = cursor.fetchall()
        for each_row in result:
            result_relationship.append({f'{entity_name}': each_row[0], f'{goal_entity_name}': each_row[1]})

    return result_relationship
