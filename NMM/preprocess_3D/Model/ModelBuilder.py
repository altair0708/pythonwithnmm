from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Part import (ElementListBuilder,
                                    NmmDatabaseBuilder,
                                    DataStructureBuilder,
                                    FilePathBuilder,
                                    MatrixSolverBuilder,
                                    GlobalVariableBuilder)
from NMM.preprocess_3D.Model.Model import preprocess_model
from NMM.preprocess_3D.Part.PartBuilder import PartBuilder


class PreprocessModelBuilder(AbstractConstructor):
    def build(self, root_name: str):
        file_path_builder = FilePathBuilder(root_name)
        preprocess_model.add_property(file_path_builder.build())

        data_structure_builder = DataStructureBuilder()
        preprocess_model.add_property(data_structure_builder.build())

        nmm_database_builder = NmmDatabaseBuilder()
        preprocess_model.add_property(nmm_database_builder.build())

        matrix_element_list_builder = ElementListBuilder()
        preprocess_model.add_property(matrix_element_list_builder.build('matrix_element'))

        # matrix_solver_builder = MatrixSolverBuilder()
        # preprocess_model.add_property(matrix_solver_builder.build())
        #
        # global_variable = GlobalVariableBuilder()
        # preprocess_model.add_property(global_variable.build())

        return preprocess_model

