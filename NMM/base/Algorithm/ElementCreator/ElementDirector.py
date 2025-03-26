from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap


class ElementDirector:
    def __init__(self, mathematics_point: VtkGrid, manifold_element: VtkGrid, boundary_condition: VtkGrid, material_parameter: PropertyMap):
        self.__builder = None
        self.__mathematics_point = mathematics_point
        self.__manifold_element = manifold_element
        self.__boundary_condition = boundary_condition
        self.__material_parameter = material_parameter

    @property
    def builder(self):
        return self.__builder

    @builder.setter
    def builder(self, builder: AbstractElementBuilder):
        self.__builder = builder

    def build_matrix_element(self, element_id: int):
        self.__builder.set_simple_properties(element_id, self.__manifold_element)
        self.__builder.set_material_parameters(element_id, self.__manifold_element, self.__material_parameter)
        self.__builder.set_vertexes(element_id, self.__manifold_element)
        self.__builder.set_patches(element_id, self.__mathematics_point)
        self.__builder.set_special_points(element_id, self.__boundary_condition)

