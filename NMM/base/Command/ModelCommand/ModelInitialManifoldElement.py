from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ModelInitialManifoldElement(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')

    def execute(self):
        for each_point_id in range(self.__manifold_element.get_point_number()):
            self.__manifold_element.set_attribute('material_id', each_point_id, 0)
            self.__manifold_element.set_attribute('point_displacement_total', each_point_id, (0, 0, 0))
            self.__manifold_element.set_attribute('point_displacement_increment', each_point_id, (0, 0, 0))
            self.__manifold_element.set_attribute('point_velocity', each_point_id, (0, 0, 0))
