from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.Property.Implement.DatabaseTable import DatabaseTable
from NMM.base.Command.Invoker import Invoker
from NMM.base.Command.ModelCommand.ModelGetPath import ModelGetPath
from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabase import NmmDatabase


class NmmDatabaseBuilder(AbstractConstructor):
    def build(self):
        database_path = self.get_path('database')
        database = NmmDatabase(database_path)

        database_table_list = ['cover_element', 'element_specialpoint', 'element_surface', 'element_cracksurface',
                               'surface_crackedge', 'cracksurface_crackedge', 'element_newelement', 'surface_newsurface']
        for each_database_table in database_table_list:
            temp_database_table = DatabaseTable(each_database_table, database_path)
            database.add_property(temp_database_table)

        return database

    @staticmethod
    def get_path(path_name: str):
        from NMM.preprocess_3D.Model.Model import preprocess_model
        path_part = preprocess_model.get_property('file_path')

        invoker = Invoker()
        invoker.set_command(ModelGetPath(path_name, path_part))
        return invoker.press_button()
