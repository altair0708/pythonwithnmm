from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyMap, PropertyVector
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from typing import List
import numpy as np


class CompleteElementBuilder(AbstractElementBuilder):
    def __init__(self):
        self.__element = ElementBase('complete_element')
        self.reset()

    def reset(self):
        self.__element = ElementBase('complete_element')

    def get_element(self):
        element = self.__element
        self.reset()
        return element

    def set_material_parameters(self, element_id: int, manifold_element: VtkGrid, material_parameter: PropertyMap):
        material_id = int(manifold_element.get_cell_attribute('material_id', element_id)[0])

        temp_property = PropertyInteger(material_id)
        temp_property.set_name('material_id')
        self.__element.add_property(temp_property)

        temp_property = PropertyMap(material_parameter[str(material_id)])
        temp_property.set_name('material_parameter')
        self.__element.add_property(temp_property)

    def set_simple_properties(self, element_id: int, manifold_element: VtkGrid):
        temp_property = PropertyInteger(int(manifold_element.get_cell_attribute('cell_id', element_id)[0]))
        temp_property.set_name('cell_id')
        self.__element.add_property(temp_property)

        temp_property = PropertyInteger(int(manifold_element.get_cell_attribute('cracked', element_id)[0]))
        temp_property.set_name('cracked')
        self.__element.add_property(temp_property)

        temp_vector = PropertyVector(np.array(manifold_element.get_cell_attribute('initial_strain_total', element_id), dtype=np.float64).reshape((6, 1)))
        temp_vector.set_name('initial_strain_total')
        self.__element.add_property(temp_vector)

    def set_vertexes(self, element_id: int, manifold_element: VtkGrid):
        point_id: List = manifold_element.get_cell_point_id(element_id)
        temp_property = PropertyList(point_id)
        temp_property.set_name('point_id')
        self.__element.add_property(temp_property)

        point_displacement_total = [manifold_element.get_point_attribute('point_displacement_total', i) for i in point_id]
        temp_property = PropertyList(point_displacement_total)
        temp_property.set_name('point_displacement_total')
        self.__element.add_property(temp_property)

        # point_coordinate_old = [manifold_element.get_point_coordinate(i) for i in point_id]
        # point_coordinate = []
        # for each_coordinate, each_displacement in zip(point_coordinate_old, point_displacement_total):
        #     new_coordinate = tuple([each_coordinate[i] + each_displacement[i] for i in range(3)])
        #     point_coordinate.append(new_coordinate)
        point_coordinate = [manifold_element.get_point_coordinate(i) for i in point_id]
        temp_property = PropertyList(point_coordinate)
        temp_property.set_name('point_coordinate')

        self.__element.add_property(temp_property)
        point_displacement_increment = [manifold_element.get_point_attribute('point_displacement_increment', i) for i in point_id]
        temp_property = PropertyList(point_displacement_increment)
        temp_property.set_name('point_displacement_increment')
        self.__element.add_property(temp_property)

        point_velocity = [manifold_element.get_point_attribute('point_velocity', i) for i in point_id]
        temp_property = PropertyList(point_velocity)
        temp_property.set_name('point_velocity')
        self.__element.add_property(temp_property)

    def set_patches(self, element_id: int, math_cover: VtkGrid):
        relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None, id_1=element_id)
        patch_id = [int(each_relationship['cover']) for each_relationship in relationship_list]
        temp_property = PropertyList(patch_id)
        temp_property.set_name('math_cover_id')
        self.__element.add_property(temp_property)

        patch_coordinate = [math_cover.get_cell_attribute('math_cover_coordinate', i) for i in patch_id]
        temp_property = PropertyList(patch_coordinate)
        temp_property.set_name('math_cover_coordinate')
        self.__element.add_property(temp_property)

        patch_displacement_total = [math_cover.get_cell_attribute('math_cover_displacement_total', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_total)
        temp_property.set_name('math_cover_displacement_total')
        self.__element.add_property(temp_property)

        patch_displacement_increment = [math_cover.get_cell_attribute('math_cover_displacement_increment', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_increment)
        temp_property.set_name('math_cover_displacement_increment')
        self.__element.add_property(temp_property)

    def set_special_points(self, element_id: int, special_point: VtkGrid):
        relationship_list = relationship_cache.get_item(name_0='element', name_1='specialpoint', id_0=element_id, id_1=None)

        loading_point_id = []  # point_type = 0
        fixed_point_id = []  # point_type = 1
        measured_point_id = []  # point_type = 2

        for each_relationship in relationship_list:
            special_point_id = int(each_relationship['specialpoint'])
            point_type = special_point.get_cell_attribute('point_type', special_point_id)[0]
            if point_type == 0:
                loading_point_id.append(special_point_id)
            elif point_type == 1:
                fixed_point_id.append(special_point_id)
            elif point_type == 2:
                measured_point_id.append(special_point_id)

        temp_property = PropertyList(loading_point_id)
        temp_property.set_name('loading_point_id')
        self.__element.add_property(temp_property)

        temp_property = PropertyList(fixed_point_id)
        temp_property.set_name('fixed_point_id')
        self.__element.add_property(temp_property)

        temp_property = PropertyList(measured_point_id)
        temp_property.set_name('measured_point_id')
        self.__element.add_property(temp_property)

        loading_point_coordinate = [special_point.get_cell_attribute('special_point_coordinate', i) for i in loading_point_id]
        temp_property = PropertyList(loading_point_coordinate)
        temp_property.set_name('loading_point_coordinate')
        self.__element.add_property(temp_property)

        fixed_point_coordinate = [special_point.get_cell_attribute('special_point_coordinate', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_coordinate)
        temp_property.set_name('fixed_point_coordinate')
        self.__element.add_property(temp_property)

        measured_point_coordinate = [special_point.get_cell_attribute('special_point_coordinate', i) for i in measured_point_id]
        temp_property = PropertyList(measured_point_coordinate)
        temp_property.set_name('measured_point_coordinate')
        self.__element.add_property(temp_property)

        loading_point_force = [special_point.get_cell_attribute('force', i) for i in loading_point_id]
        temp_property = PropertyList(loading_point_force)
        temp_property.set_name('loading_point_force')
        self.__element.add_property(temp_property)

        fixed_point_velocity = [special_point.get_cell_attribute('velocity', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_velocity)
        temp_property.set_name('fixed_point_velocity')
        self.__element.add_property(temp_property)

        fixed_point_displacement_total = [special_point.get_cell_attribute('special_point_displacement_total', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_displacement_total)
        temp_property.set_name('fixed_point_displacement_total')
        self.__element.add_property(temp_property)

        fixed_point_displacement_increment = [special_point.get_cell_attribute('special_point_displacement_increment', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_displacement_increment)
        temp_property.set_name('fixed_point_displacement_increment')
        self.__element.add_property(temp_property)
