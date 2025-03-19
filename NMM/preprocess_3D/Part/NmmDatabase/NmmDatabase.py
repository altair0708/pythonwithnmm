from NMM.base.Part.Part import Part
from NMM.base.SqliteBase import new_a_database
from NMM.base.Property.Implement.Relationship import Relationship
import sqlite3


class NmmDatabase(Part):
    def __init__(self, file_name, new_database: bool = True):
        super(NmmDatabase, self).__init__()
        self.name = 'database'

        self.__database_path = file_name
        if new_database is True:
            new_a_database(self.__database_path)

        self.__connection = sqlite3.connect(self.__database_path)

    @property
    def database_path(self):
        return self.__database_path

    def add_relationship(self, relationship: Relationship):
        self.get_property(relationship.name).add_relationship()

    @property
    def connection(self):
        return self.__connection

    def __del__(self):
        self.__connection.commit()
        self.__connection.close()
        print('Database closed')
