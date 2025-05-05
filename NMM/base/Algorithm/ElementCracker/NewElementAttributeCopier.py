from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class AttributeCopier(AbstractAlgorithm):
    def __init__(self, element_id: int, new_element_id: int, manifold_element: VtkGrid, new_element: VtkGrid):
        self.__element_id = element_id
        self.__new_element_id = new_element_id
        self.__manifold_element = manifold_element
        self.__new_element = new_element

    def update(self, *args, **kwargs):
        material_id = self.__manifold_element.get_attribute('material_id', self.__element_id)[0]
        self.__new_element.set_attribute('material_id', self.__new_element_id, material_id)

        initial_strain_total = self.__manifold_element.get_attribute('initial_strain_total', self.__element_id)
        self.__new_element.set_attribute('initial_strain_total', self.__new_element_id, initial_strain_total)

        for each_point_id in self.__new_element.get_cell_point_id(self.__new_element_id):
            point_coordinate = self.__new_element.get_point_coordinate(each_point_id)
            self.__new_element.set_attribute('point_coordinate', each_point_id, point_coordinate)

            self.__new_element.set_attribute('point_displacement_total', each_point_id, (0, 0, 0))
            self.__new_element.set_attribute('point_displacement_increment', each_point_id, (0, 0, 0))
            self.__new_element.set_attribute('point_velocity', each_point_id, (0, 0, 0))
