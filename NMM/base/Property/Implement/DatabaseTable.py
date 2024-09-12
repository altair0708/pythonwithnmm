from NMM.base.Property.Property import Property
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.SqliteBase import new_a_table, add_a_relationship, exist_a_table
from NMM.base.CacheBase.RelationshipCache import relationship_cache


class DatabaseTable(Property):
    def __init__(self, relationship_name: str, file_name: str):
        super(DatabaseTable, self).__init__()
        self._name = relationship_name
        self._type = 'DatabaseTable'
        self.__database_path = file_name

        # lazy mode
        self._value = None
        if not exist_a_table(relationship_name, file_name):
            self.add_table()

        # relationship_cache.add_observer(self)

    def add_table(self):
        new_a_table(self.__database_path, self._name)

    # Interface from relationship_cache, modify relationship(add)
    def modify(self, relationship: Relationship):
        add_a_relationship(self.__database_path, relationship.name, relationship.value)



