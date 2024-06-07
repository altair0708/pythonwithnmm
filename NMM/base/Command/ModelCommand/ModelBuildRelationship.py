from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabase import NmmDatabase
from NMM.base.Property.Implement.Relationship import Relationship


class ModelBuildRelationship(AbstractCommand):
    def __init__(self, relationship: Relationship, database: NmmDatabase):
        self.__relationship = relationship
        self.__database = database

    def execute(self):
        self.__database.add_relationship(self.__relationship)

