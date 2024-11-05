from NMM.preprocess_3D.Part.ElementList.ElementList import ElementList
from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor


class ElementListBuilder(AbstractConstructor):
    def build(self, element_type: str):
        preprocess_element_list = ElementList(element_type)
        return preprocess_element_list
