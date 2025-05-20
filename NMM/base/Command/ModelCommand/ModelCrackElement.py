from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCracker.ElementCracker import ElementCracker
from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensileStress import MaximumTensileStress
from NMM.base.Algorithm.ElementCracker.Criterion.MohrCoulomb import MohrCoulomb


class ModelCrackElement(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')

    def execute(self):
        from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
        iteration_flag = True
        iteration_number = 0

        while iteration_flag:
            new_element_number_0 = global_variable_cache.get_item('new_element_number')

            for each_id in range(self.__manifold_element.get_cell_number()):
                element_cracked = self.__manifold_element.get_attribute('cracked', each_id)[0]
                if element_cracked == 8:
                    cracker = ElementCracker(each_id, self.__manifold_element)

                    criterion = MohrCoulomb()

                    cracker.set_criterion(criterion)
                    cracker.update()
            print(f'Crack propagation step:{iteration_number} completed.')
            new_element_number_1 = global_variable_cache.get_item('new_element_number')
            if new_element_number_0 == new_element_number_1:
                iteration_flag = False
            iteration_number = iteration_number + 1


