from NMM.base.Property.Property import Property
from NMM.base.SqliteBase import new_a_table, add_a_relationship
from NMM.base.Property.Implement.Relationship import Relationship


class DatabaseTable(Property):
    def __init__(self, relationship_name: str, file_name: str):
        super(DatabaseTable, self).__init__()
        self._name = relationship_name
        self._type = 'DatabaseTable'
        self.__database_path = file_name

        # lazy mode
        self._value = None
        self.add_table()

    def add_table(self):
        new_a_table(self.__database_path, self._name)

    def add_relationship(self, relationship: Relationship):
        add_a_relationship(self.__database_path, relationship.name, relationship.value)



