from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.ElementRefresher import displacement_interpolation
from NMM.base.CacheBase import entrance_cache, relationship_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyList import PropertyList
import numpy as np


class ModelRefreshNewElement(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')

    def execute(self):
        new_element_list = global_variable_cache.get_item('new_element_id')

        for each_new_element_id in new_element_list:
            relationship_list = relationship_cache.get_item(name_0='element', name_1='newelement', id_0=None, id_1=each_new_element_id)
            assert len(relationship_list) == 1
            element_id = relationship_list[0]['element']


            material_id = self.__manifold_element.get_cell_attribute('material_id', element_id)[0]
            self.__new_element.set_cell_attribute('material_id', each_new_element_id, material_id)

            initial_strain_total = self.__manifold_element.get_cell_attribute('initial_strain_total', element_id)
            self.__new_element.set_cell_attribute('initial_strain_total', each_new_element_id, initial_strain_total)

            relationship_list = relationship_cache.get_item(name_0='newcover', name_1='newelement', id_0=None, id_1=each_new_element_id)

            cover_id = [each_relationship['newcover'] for each_relationship in relationship_list]
            assert len(cover_id) == 4
            point_id = self.__new_element.get_cell_point_id(each_new_element_id)

            cover_displacement_increment = PropertyList(
                [self.__new_cover.get_cell_attribute('math_cover_displacement_increment', i) for i in cover_id])
            cover_displacement_total = PropertyList(
                [self.__new_cover.get_cell_attribute('math_cover_displacement_total', i) for i in cover_id])
            cover_coordinate = PropertyList([self.__new_cover.get_point_coordinate(i) for i in cover_id])

            for each_point_id in point_id:
                point_coordinate = self.__new_element.get_point_coordinate(each_point_id)

                displacement_increment = displacement_interpolation(point_coordinate, cover_displacement_increment,
                                                                    cover_coordinate)
                self.__new_element.set_point_attribute('point_displacement_increment', each_point_id, displacement_increment)

                displacement_total = displacement_interpolation(point_coordinate, cover_displacement_total,
                                                                cover_coordinate)
                self.__new_element.set_point_attribute('point_displacement_total', each_point_id, displacement_total)

                temp_point_coordinate = self.__new_element.get_point_coordinate(each_point_id)
                temp_point_coordinate = np.array(temp_point_coordinate, dtype=np.float64) + np.array(
                    displacement_total, dtype=np.float64)
                self.__new_element.set_point_attribute('point_coordinate', each_point_id, temp_point_coordinate)
                self.__new_element.set_point_attribute('point_velocity', each_point_id, (0, 0, 0))
        # clean new_element_id list
        global_variable_cache.add_item('new_element_id', [])
