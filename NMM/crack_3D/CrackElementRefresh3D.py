from NMM.GlobalVariable import DataStructure
from NMM.base.PropertyGetSetFunction import set_property, get_property
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from typing import List
import numpy as np


class CrackElementRefresher:
    @staticmethod
    def refresh_manifold_element(data_structure: DataStructure, element_list: List[CrackedElement3D]):
        temp_vtk_model = data_structure.manifold_element.content
        temp_crack_vtk = data_structure.crack_surface.content
        for element_id in range(len(element_list)):
            temp_element = element_list[element_id]
            temp_crack = temp_element.cracked
            temp_surface = temp_element.crack_surface
            set_property(temp_vtk_model, 'cracked', element_id, np.array((temp_crack,)))

            # this time step have ability to crack
            if temp_crack == 1:
                crack_edge_number = temp_element.crack_edge_number
                set_property(temp_vtk_model, 'cracked', element_id, np.array((2,)))
                set_property(temp_vtk_model, 'crack_edge_number', element_id, np.array((crack_edge_number, )))

                for edge_id in range(crack_edge_number):

                    edge_points = temp_element.crack_edge[edge_id]
                    temp_edge = list(edge_points[0])
                    point_2 = edge_points[1]
                    temp_edge.extend(point_2)

                    edge_name = 'crack_edge_{temp_id}'.format(temp_id=edge_id+1)
                    set_property(temp_vtk_model, edge_name, element_id, np.array(temp_edge))

            # this time step cracked
            if temp_crack == 3:
                # the number of crack surface in recent crack surface model
                crack_number = temp_crack_vtk.GetNumberOfCells()

                # insert the crack information of the element model
                set_property(temp_vtk_model, 'cracked', element_id, np.array((4,)))
                set_property(temp_vtk_model, 'crack_surface_id', element_id, np.array((crack_number,)))

                # insert the crack surface into crack surface model
                insert_a_cell(temp_crack_vtk, temp_surface)
                set_property(temp_crack_vtk, 'element_id', crack_number, np.array((element_id,)))

    @staticmethod
    def refresh_physical_cover(data_structure: DataStructure, element_list):
        pass
