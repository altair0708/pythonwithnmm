import sys
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from NMM.GlobalVariable import Variable
from NMM.base.ElementClipFunction import generate_crack_edge_surface
from typing import List


def find_adjacent_element(crack_id: int, element_list: List[CrackedElement3D]):
    pass


class ElementCracker3D(object):
    @staticmethod
    def crack_all_element(element_list: List[CrackedElement3D]):
        for each_id in range(Variable.element_number):
            adjacent_element_dict = ElementCracker3D.crack_an_element(element_list[each_id])
            if adjacent_element_dict is not None:
                for each_face in range(len(adjacent_element_dict)):
                    face_dict = adjacent_element_dict[each_face]
                    adjacent_element_id = face_dict['adjacent_cell_id']
                    # if 'edge_points' in face_dict:
                    adjacent_element = element_list[adjacent_element_id]
                    if 'edge_points' in face_dict:
                        points: vtkPoints = face_dict['edge_points']
                        point_1 = points.GetPoint(0)
                        point_2 = points.GetPoint(1)

                        # element without crack edge
                        if adjacent_element.cracked < 1:
                            adjacent_element.cracked = 1
                            adjacent_element.crack_edge_number = 1
                            adjacent_element.crack_edge[0].append(point_1)
                            adjacent_element.crack_edge[0].append(point_2)

                        # element with one or more crack edges
                        elif adjacent_element.cracked == 1 or adjacent_element.cracked == 2:
                            temp_edge_number = adjacent_element.crack_edge_number
                            try:
                                assert temp_edge_number < 4
                            except AssertionError:
                                [print(i) for i in adjacent_element.crack_edge]
                                sys.exit()
                            adjacent_element.crack_edge[temp_edge_number].append(point_1)
                            adjacent_element.crack_edge[temp_edge_number].append(point_2)
                            adjacent_element.crack_edge_number += 1
                            adjacent_element.cracked = 1


    @staticmethod
    def crack_an_element(element: CrackedElement3D):
        # element crack!!!
        # if element.strain.max_component[0] > 0.00001 and element.cracked == 2:
        if element.cracked == 2:
            element.cracked = 3
            element.generate_crack_surface()

        # deliver adjacent element information
        if element.cracked == 3:
            generate_crack_edge_surface(element.adjacent_element, element.crack_surface)

        return element.adjacent_element
