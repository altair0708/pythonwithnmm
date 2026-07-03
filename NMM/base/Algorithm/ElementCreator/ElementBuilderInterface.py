import numpy as np
from abc import ABC, abstractmethod
from typing import List
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyMap, PropertyVector


class AbstractElementBuilder(ABC):
    def __init__(self, cover: VtkGrid, element: VtkGrid, boundary_condition: VtkGrid, material_parameter: PropertyMap):
        self._cover_grid = cover
        self._element_grid = element
        self._boundary_condition = boundary_condition
        self._material_parameter = material_parameter

        self._element = ElementBase('empty')
        self.reset()

    @abstractmethod
    def reset(self):
        pass

    def get_element(self):
        element = self._element
        self.reset()
        return element

    def set_material_parameters(self, element_id: int):
        element_grid = self._element_grid
        material_parameter = self._material_parameter
        material_id = int(element_grid.get_cell_attribute('material_id', element_id)[0])

        temp_property = PropertyInteger(material_id)
        temp_property.set_name('material_id')
        self._element.add_property(temp_property)

        temp_property = PropertyMap(material_parameter[str(material_id)])
        temp_property.set_name('material_parameter')
        self._element.add_property(temp_property)

    def set_simple_properties(self, element_id: int):
        element_grid = self._element_grid

        temp_property = PropertyInteger(int(element_grid.get_cell_attribute('cell_id', element_id)[0]))
        temp_property.set_name('cell_id')
        self._element.add_property(temp_property)

        temp_vector = PropertyVector(np.array(element_grid.get_cell_attribute('initial_strain_total', element_id), dtype=np.float64).reshape((6, 1)))
        temp_vector.set_name('initial_strain_total')
        self._element.add_property(temp_vector)

    def set_vertexes(self, element_id: int):
        element_grid = self._element_grid

        point_id: List = element_grid.get_cell_point_id(element_id)
        temp_property = PropertyList(point_id)
        temp_property.set_name('point_id')
        self._element.add_property(temp_property)

        point_displacement_total = [element_grid.get_point_attribute('point_displacement_total', i) for i in point_id]
        temp_property = PropertyList(point_displacement_total)
        temp_property.set_name('point_displacement_total')
        self._element.add_property(temp_property)

        # point_coordinate_old = [manifold_element.get_point_coordinate(i) for i in point_id]
        # point_coordinate = []
        # for each_coordinate, each_displacement in zip(point_coordinate_old, point_displacement_total):
        #     new_coordinate = tuple([each_coordinate[i] + each_displacement[i] for i in range(3)])
        #     point_coordinate.append(new_coordinate)
        point_coordinate = [element_grid.get_point_coordinate(i) for i in point_id]
        temp_property = PropertyList(point_coordinate)
        temp_property.set_name('point_coordinate')

        self._element.add_property(temp_property)
        point_displacement_increment = [element_grid.get_point_attribute('point_displacement_increment', i) for i in point_id]
        temp_property = PropertyList(point_displacement_increment)
        temp_property.set_name('point_displacement_increment')
        self._element.add_property(temp_property)

        point_velocity = [element_grid.get_point_attribute('point_velocity', i) for i in point_id]
        temp_property = PropertyList(point_velocity)
        temp_property.set_name('point_velocity')
        self._element.add_property(temp_property)

    @abstractmethod
    def set_patches(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_special_points(self, *args, **kwargs):
        pass
