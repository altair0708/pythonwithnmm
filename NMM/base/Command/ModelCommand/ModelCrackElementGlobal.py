from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCracker.CrackStatusUpdate import CrackStatusUpdate
from NMM.base.Algorithm.ElementCracker.CrackTipOnSurface import CrackTipOnSurface
from NMM.base.Algorithm.ElementCracker.ElementCrackerGlobal import ElementCrackerGlobal


class ModelCrackElementGlobal(AbstractCommand):
    def __init__(self):
        self.__crack_tip: VtkGrid = entrance_cache.get_item('crack_tip_VtkGrid')
        self.__crack_propagation: VtkGrid = entrance_cache.get_item('crack_propagation_VtkGrid')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__geometric_shell: VtkGrid = entrance_cache.get_item('geometric_shell_VtkGrid')

    def execute(self):
        algorithm = CrackTipOnSurface(self.__crack_tip, self.__geometric_shell)
        algorithm.update()

        algorithm = CrackStatusUpdate(self.__crack_tip, self.__crack_propagation, self.__manifold_element)
        algorithm.update()
        crack_point_dict = algorithm.crack_point_dict

        # algorithm = ElementCrackerGlobal(self.__manifold_element)
        # algorithm.crack_point_dict = crack_point_dict
        # algorithm.update()

