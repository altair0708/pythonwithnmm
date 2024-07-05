from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.Property.Implement.DatabaseTable import DatabaseTable


class PropertyBuildRelationship(AbstractCommand):
    def __init__(self, relationship: Relationship, database_table: DatabaseTable):
        self.__relationship = relationship
        self.__database_table = database_table

    def execute(self):
        self.__database_table.add_relationship(self.__relationship)

