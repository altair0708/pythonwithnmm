from NMM.base.Part.Part import Part
from NMM.base.SqliteBase import new_a_database
from NMM.base.Property.Implement.Relationship import Relationship


class NmmDatabase(Part):
    def __init__(self, file_name):
        super(NmmDatabase, self).__init__()
        self.name = 'database'

        self.__database_path = file_name
        new_a_database(self.__database_path)

    @property
    def database_path(self):
        return self.__database_path

    def add_relationship(self, relationship: Relationship):
        self.get_property(relationship.name).add_relationship()
