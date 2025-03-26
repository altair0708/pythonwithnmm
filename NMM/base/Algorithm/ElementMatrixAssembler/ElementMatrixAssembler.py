from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Algorithm.ElementMatrixAssembler.CompleteElementMatrixAssembler import CompleteAssembler
from typing import List


class ElementMatrixAssembler(AbstractAlgorithm):
    def __init__(self, element_list: List[ElementBase]):
        self.__element_list = element_list

    def update(self, *args, **kwargs):
        for each_element in self.__element_list:
            if each_element.name == 'complete_element':
                assembler = CompleteAssembler(each_element)
            else:
                raise Exception(f'Element_type_error!!!: {each_element.name}')
            assembler.update()
