from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Model.Model import PreprocessModel
from NMM.preprocess_3D.Part.FilePath.FilePathBuilder import FilePathBuilder
from NMM.preprocess_3D.Part.DataStructure.DataStructureBuilder import DataStructureBuilder
from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabaseBuilder import NmmDatabaseBuilder
from NMM.preprocess_3D.Part.ElementList.ElementListBuilder import PreprocessElementListBuilder


class PreprocessModelBuilder(AbstractConstructor):
    def build(self, root_name: str):
        model = PreprocessModel()

        file_path_builder = FilePathBuilder()
        file_path_part = file_path_builder.build(root_name)
        model.add_property(file_path_part)

        data_structure_builder = DataStructureBuilder()
        data_structure_part = data_structure_builder.build()
        model.add_property(data_structure_part)

        nmm_database_builder = NmmDatabaseBuilder()
        nmm_database_part = nmm_database_builder.build()
        model.add_property(nmm_database_part)

        preprocess_element_list_builder = PreprocessElementListBuilder()
        preprocess_element_part = preprocess_element_list_builder.build()
        model.add_property(preprocess_element_part)

        return model

