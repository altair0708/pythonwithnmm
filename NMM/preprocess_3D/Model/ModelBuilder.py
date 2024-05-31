from NMM.base.Object.Builder.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Model.Model import PreprocessModel
from NMM.preprocess_3D.Part.FilePath.FilePathBuilder import FilePathBuilder


class PreprocessModelBuilder(AbstractConstructor):
    def build(self, root_name: str):
        model = PreprocessModel()

        file_path_builder = FilePathBuilder()
        file_path_part = file_path_builder.build(root_name)
        model.add_property(file_path_part)

        pass
