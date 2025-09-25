from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCracker.ElementCracker import ElementCracker


class ModelCopyCoverAttribute(AbstractCommand):
    def __init__(self):
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')

    def execute(self):
        new_cover_list = global_variable_cache.get_item('new_cover_id')

        for each_new_cover_id in new_cover_list:
            relationship_list = relationship_cache.get_item(name_0='cover', name_1='newcover', id_0=None, id_1=each_new_cover_id)
            assert len(relationship_list) == 1
            cover_id = relationship_list[0]['cover']

            point_coordinate = self.__new_cover.get_point_coordinate(each_new_cover_id)
            self.__new_cover.set_attribute('math_cover_coordinate', each_new_cover_id, point_coordinate)

            displacement_total = self.__mathematics_point.get_attribute('math_cover_displacement_total', cover_id)
            self.__new_cover.set_attribute('math_cover_displacement_total', each_new_cover_id, displacement_total)

            displacement_increment = self.__mathematics_point.get_attribute('math_cover_displacement_increment', cover_id)
            self.__new_cover.set_attribute('math_cover_displacement_increment', each_new_cover_id, displacement_increment)

            velocity = self.__mathematics_point.get_attribute('math_cover_velocity', cover_id)
            self.__new_cover.set_attribute('math_cover_velocity', each_new_cover_id, velocity)

        # clean new_cover_id list
        global_variable_cache.add_item('new_cover_id', [])
