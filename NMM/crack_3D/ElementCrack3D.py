from vtkmodules.vtkCommonCore import vtkPoints
from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from NMM.GlobalVariable import Variable
from typing import List


def find_adjacent_element(crack_id: int, element_list: List[CrackedElement3D]):
    pass


class ElementCracker3D(object):
    @staticmethod
    def crack_all_element(element_list: List[CrackedElement3D]):
        for each_id in range(Variable.element_number):
            adjacent_element_dict = ElementCracker3D.crack_an_element(element_list[each_id])
            if adjacent_element_dict is not None:
                # a = 0
                for each_face in range(len(adjacent_element_dict)):
                    face_dict = adjacent_element_dict[each_face]
                    adjacent_element_id = face_dict['adjacent_cell_id']
                    # if 'edge_points' in face_dict:
                    #     a += 1
                    adjacent_element = element_list[adjacent_element_id]
                    if adjacent_element.cracked < 1 and 'edge_points' in face_dict:
                        adjacent_element.cracked = 1
                        points: vtkPoints = face_dict['edge_points']
                        point_1 = points.GetPoint(0)
                        adjacent_element.crack_edge.append(point_1)
                        point_2 = points.GetPoint(1)
                        adjacent_element.crack_edge.append(point_2)


    @staticmethod
    def crack_an_element(element: CrackedElement3D):
        if element.strain.max_component[0] > 0.001 and element.cracked == 2:
            element.cracked = 3
            element.generate_crack_surface()
            return element.adjacent_element
