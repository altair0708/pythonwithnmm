from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap


class ElementDirector:
    def __init__(self):
        self.__builder = None

    @property
    def builder(self):
        return self.__builder

    @builder.setter
    def builder(self, builder: AbstractElementBuilder):
        self.__builder = builder

    def build_matrix_element(self, element_id: int):
        self.__builder.set_simple_properties(element_id)
        self.__builder.set_material_parameters(element_id)
        self.__builder.set_vertexes(element_id)
        self.__builder.set_patches(element_id)
        self.__builder.set_special_points(element_id)

    def build_contact_element(self, element_id: int):
        self.__builder.set_simple_properties(element_id)
        self.__builder.set_material_parameters(element_id)
        self.__builder.set_vertexes(element_id)
        self.__builder.set_patches(element_id)

