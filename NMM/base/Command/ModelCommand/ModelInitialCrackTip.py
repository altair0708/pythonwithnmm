from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCracker.CrackStatusUpdate import CrackStatusUpdate
from NMM.base.Algorithm.ElementCracker.CrackTipOnSurface import CrackTipOnSurface
from NMM.base.Algorithm.ElementCracker.ElementCrackerGlobal import ElementCrackerGlobal
from NMM.base.VTKBase.calculate_contour_out_normal_coplane import compute_outer_normal


class ModelInitialCrackTip(AbstractCommand):
    def __init__(self):
        self.__initial_crack: VtkGrid = entrance_cache.get_item('initial_crack_VtkGrid')
        self.__crack_tip: VtkGrid = entrance_cache.get_item('crack_tip_VtkGrid')
        self.__crack_propagation: VtkGrid = entrance_cache.get_item('crack_propagation_VtkGrid')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__geometric_shell: VtkGrid = entrance_cache.get_item('geometric_shell_VtkGrid')

    def execute(self):
        for each_cell_id in range(self.__crack_tip.get_cell_number()):
            self.__crack_tip.set_cell_attribute('line_on_shell', each_cell_id, 0)
        for each_point_id in range(self.__crack_tip.get_point_number()):
            self.__crack_tip.set_point_attribute('point_on_shell', each_point_id, 0)
            self.__crack_tip.set_point_attribute('crack_point_type', each_point_id, 0)
            direction = compute_outer_normal(self.__crack_tip.value, each_point_id)
            self.__crack_tip.set_point_attribute('propagate_direction', each_point_id, direction)
            self.__crack_tip.set_point_attribute('propagate_vector', each_point_id, (0, 0, 0))

        algorithm = CrackTipOnSurface(self.__crack_tip, self.__geometric_shell)
        algorithm.update()

        algorithm = CrackStatusUpdate(self.__crack_tip, self.__crack_propagation, self.__manifold_element)
        algorithm.update()
        crack_point_dict = algorithm.crack_point_dict

        # algorithm = ElementCrackerGlobal(self.__manifold_element)
        # algorithm.crack_point_dict = crack_point_dict
        # algorithm.update()





