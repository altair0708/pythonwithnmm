from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from NMM.GlobalVariable import Variable
from typing import List


class ElementCracker3D(object):
    @staticmethod
    def crack_all_element(element_list: List[CrackedElement3D]):
        for each_id in range(Variable.element_number):
            ElementCracker3D.crack_an_element(element_list[each_id])

    @staticmethod
    def crack_an_element(element: CrackedElement3D):
        if element.strain.max_component[0] > 0.00001 and element.cracked is False:
            element.cracked = True
            element.crack_new = True
            element.generate_crack_surface()
