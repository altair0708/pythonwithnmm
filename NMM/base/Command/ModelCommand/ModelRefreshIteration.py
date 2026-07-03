from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.ElementIteration.CompleteElementIterator import CompleteElementIterator
from NMM.base.Algorithm.ElementIteration.SeparateElementIterator import SeparateElementIterator
from NMM.base.CacheBase import entrance_cache


class ModelRefreshIteration(AbstractCommand):
    def __init__(self):
        self.__matrix_solver = entrance_cache.get_item('matrix_solver_Part')

    def execute(self):
        element_list = self.__matrix_solver.get_property('element_list')
        complete_iterator = CompleteElementIterator()
        separate_iterator = SeparateElementIterator()
        for each_element in element_list:
            element_type = each_element.name
            if element_type == 'complete_element':
                complete_iterator.update(each_element)
            elif element_type == 'separate_element':
                separate_iterator.update(each_element)
