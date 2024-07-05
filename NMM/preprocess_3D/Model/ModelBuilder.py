from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Model.Model import PreprocessModel
from NMM.preprocess_3D.Part.PartBuilder import PartBuilder


class PreprocessModelBuilder(AbstractConstructor):
    def build(self, root_name: str):
        model = PreprocessModel()
        factory = PartBuilder(root_name)

        model.add_property(factory.get_part('file_path'))
        model.add_property(factory.get_part('data_structure'))
        model.add_property(factory.get_part('database'))
        model.add_property(factory.get_part('preprocess_element_list'))

        return model

