from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Command.PropertyCommand.PropertyBuildRelationship import PropertyBuildRelationship
from NMM.base.Command.Invoker import Invoker
from NMM.base.Part.Part import Part


# This a specific command used in preprocess, it is used to build the relationship of cover and element
class ModelCoverElementRelationship(AbstractCommand):
    def __init__(self, nmm_database: Part, data_structure: Part):
        self.__nmm_database = nmm_database
        self.__data_structure = data_structure

    def execute(self):
        invoker = Invoker()
        relationship_list = self.__data_structure.get_property('manifold_element').get_cover_element_list()
        database_table = self.__nmm_database.get_property('cover_element')
        for each_relationship in relationship_list:
            invoker.set_command(PropertyBuildRelationship(each_relationship, database_table))
            invoker.press_button()

