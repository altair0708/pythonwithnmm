from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.Property.Implement.PropertyList import PropertyList
from NMM.base.Algorithm.ElementRefresher.InterpolationFunction import displacement_interpolation
from typing import List
import numpy as np


class GeneralRefresher(AbstractAlgorithm):
    def __init__(self, point_id: int, mathematics_point: VtkGrid, special_point: VtkGrid, relationship_list: List[Relationship]):
        self.__point_id = point_id
        self.__cover = mathematics_point
        self.__special_point = special_point
        self.__relationship_list = relationship_list

    def update(self, *args, **kwargs):
        cover_id = [each_relationship['cover'] for each_relationship in self.__relationship_list]
        point_id = self.__point_id

        point_coordinate = self.__special_point.get_cell_attribute('special_point_coordinate', point_id)
        cover_displacement = PropertyList([self.__cover.get_cell_attribute('math_cover_displacement_increment', i) for i in cover_id])
        cover_coordinate = PropertyList([self.__cover.get_cell_attribute('math_cover_coordinate', i) for i in cover_id])

        displacement_increment = displacement_interpolation(point_coordinate, cover_displacement, cover_coordinate)
        self.__special_point.set_cell_attribute('special_point_displacement_increment', point_id, displacement_increment)

        displacement_total = self.__special_point.get_cell_attribute('special_point_displacement_total', point_id)
        displacement_total = np.array(displacement_total, dtype=np.float64) + np.array(displacement_increment, dtype=np.float64)
        self.__special_point.set_cell_attribute('special_point_displacement_total', point_id, displacement_total)

        point_coordinate = self.__special_point.get_cell_attribute('special_point_coordinate', point_id)
        point_coordinate = np.array(point_coordinate, dtype=np.float64) + np.array(displacement_increment, dtype=np.float64)
        self.__special_point.set_cell_attribute('special_point_coordinate', point_id, point_coordinate)





