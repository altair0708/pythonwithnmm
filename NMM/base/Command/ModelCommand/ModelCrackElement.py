from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCracker.ElementCracker import ElementCracker
from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensileStress import MaximumTensileStress


class ModelCrackElement(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')

    def execute(self):
        for each_id in range(self.__manifold_element.get_cell_number()):
            element_cracked = self.__manifold_element.get_attribute('cracked', each_id)[0]
            if element_cracked == 8:
                cracker = ElementCracker(each_id, self.__manifold_element)

                criterion = MaximumTensileStress()

                cracker.set_criterion(criterion)
                cracker.update()

