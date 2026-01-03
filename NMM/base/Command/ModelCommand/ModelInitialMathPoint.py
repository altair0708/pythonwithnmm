from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelInitialMathPoint(AbstractCommand):
    def __init__(self):
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')

    def execute(self):
        global_variable_cache.add_item('cover_number', self.__mathematics_point.get_point_number())
        for each_point_id in range(self.__mathematics_point.get_point_number()):
            point_coordinate = self.__mathematics_point.get_point_coordinate(each_point_id)
            self.__mathematics_point.set_attribute('math_cover_coordinate', each_point_id, point_coordinate)
            self.__mathematics_point.set_attribute('math_cover_displacement_total', each_point_id, (0, 0, 0))
            self.__mathematics_point.set_attribute('math_cover_displacement_increment', each_point_id, (0, 0, 0))
            self.__mathematics_point.set_attribute('math_cover_velocity', each_point_id, (0, 0, 0))
            self.__mathematics_point.set_attribute('enrichment', each_point_id, 0)
            self.__mathematics_point.set_attribute('enrichment_vector_x', each_point_id, (0, 0, 0, 0))
            self.__mathematics_point.set_attribute('enrichment_vector_y', each_point_id, (0, 0, 0, 0))
            self.__mathematics_point.set_attribute('enrichment_vector_z', each_point_id, (0, 0, 0, 0))

