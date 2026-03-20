from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.PropertyList import PropertyList
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.Algorithm.ElementRefresher import displacement_interpolation
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.VTKBase.write_file import write_file
from NMM.base.CacheBase import relationship_cache
from typing import List
import numpy as np


class ContactElementRefresher(AbstractAlgorithm):
    def __init__(self, element_id: int, cover: VtkGrid, element: VtkGrid):
        self.__element_id = element_id
        self.__cover = cover
        self.__element = element

    def update(self, *args, **kwargs):
        surface_id = self.__element_id

        element_id = relationship_cache.get_item('element', 'cracksurface', None, surface_id)[0]['element']
        new_element_id = relationship_cache.get_item('element', 'newelement', element_id, None)
        assert len(new_element_id) == 2

        for each_id, each in enumerate(new_element_id):
            new_cover_id_list = relationship_cache.get_item('newcover', 'newelement', None, each['newelement'])
            cover_id = [int(each_relationship['newcover']) for each_relationship in new_cover_id_list]

            cover_displacement = PropertyList([self.__cover.get_cell_attribute('math_cover_displacement_increment', i) for i in cover_id])
            cover_coordinate = PropertyList([self.__cover.get_point_coordinate(i) for i in cover_id])
            point_coordinate = self.__element.get_cell_attribute(f'center_coordinate_{each_id}', surface_id)
            displacement_increment = displacement_interpolation(point_coordinate, cover_displacement, cover_coordinate)
            point_coordinate = np.array(point_coordinate, dtype=np.float64) + np.array(displacement_increment, dtype=np.float64)

            self.__element.set_cell_attribute(f'center_coordinate_{each_id}', surface_id, point_coordinate)
