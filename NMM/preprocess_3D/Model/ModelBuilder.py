from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Model.Model import preprocess_model
from NMM.preprocess_3D.Part.PartBuilder import PartBuilder


class PreprocessModelBuilder(AbstractConstructor):
    def build(self, root_name: str):
        factory = PartBuilder(root_name)

        preprocess_model.add_property(factory.get_part('file_path'))
        preprocess_model.add_property(factory.get_part('data_structure'))
        preprocess_model.add_property(factory.get_part('database'))
        preprocess_model.add_property(factory.get_part('preprocess_element_list'))

        return preprocess_model

