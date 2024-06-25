from NMM.preprocess_3D.Part.ElementList.ElementList import PreprocessElementList
from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor


class PreprocessElementListBuilder(AbstractConstructor):
    def build(self):
        preprocess_element_list = PreprocessElementList()
        return preprocess_element_list
