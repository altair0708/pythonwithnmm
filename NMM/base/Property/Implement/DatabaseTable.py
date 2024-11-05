from NMM.base.Property.Property import Property
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.SqliteBase import new_a_table_with_connection as new_a_table
from NMM.base.SqliteBase import add_a_relationship_with_connection as add_a_relationship
from NMM.base.SqliteBase import exist_a_table_with_connection as exist_a_table
from NMM.base.SqliteBase import select_a_relationship_with_connection as select_a_relationship
from NMM.base.CacheBase import relationship_cache
from copy import deepcopy


class DatabaseTable(Property):
    def __init__(self, relationship_name: str, file_name: str, connection):
        super(DatabaseTable, self).__init__()
        self._type = 'DatabaseTable'

        self.name = relationship_name
        self.__database_path = file_name
        self.__connection = connection

        # lazy mode
        self._value = None
        if not exist_a_table(relationship_name, self.__connection):
            self.add_table()

        relationship_cache.add_observer(self)

    def add_table(self):
        new_a_table(self.__connection, self._name)

    # Interface from relationship_cache, modify relationship(add)
    def insert(self, relationship: Relationship):
        if relationship.name == self.name:
            add_a_relationship(self.__connection, relationship.name, relationship.value)

    def select(self, relationship: Relationship, result_list: list):
        if relationship.name == self.name:
            relationship_dict: dict = deepcopy(relationship.value)
            relationship_list = [(key, value) for key, value in relationship_dict.items()]
            assert len(relationship_list) == 2

            entity_name = None
            entity_id = None
            for each_entity in relationship_list:
                if None not in each_entity:
                    entity_name = each_entity[0]
                    entity_id = each_entity[1]
            assert entity_name is not None
            result = select_a_relationship(self.__connection, relationship.name, entity_name, entity_id)
            for each_relationship in result:
                temp_relationship = Relationship.generate_by_dict(relationship.name, each_relationship)
                result_list.append(temp_relationship)

