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
            temp_crack = element_list[element_id].cracked
            temp_surface = element_list[element_id].crack_surface
            set_property(temp_vtk_model, 'cracked', element_id, np.array((temp_crack,)))
            if temp_crack == 1:
                crack_edge = element_list[element_id].crack_edge
                point_1 = crack_edge[0]
                point_2 = crack_edge[1]
                set_property(temp_vtk_model, 'cracked', element_id, np.array((2,)))
                set_property(temp_vtk_model, 'crack_point_1', element_id, np.array(point_1))
                set_property(temp_vtk_model, 'crack_point_2', element_id, np.array(point_2))
            if temp_crack == 3:
                set_property(temp_vtk_model, 'cracked', element_id, np.array((4,)))
                insert_a_cell(temp_crack_vtk, temp_surface)
                crack_number = temp_crack_vtk.GetNumberOfCells()
                set_property(temp_crack_vtk, 'element_id', crack_number - 1, np.array((element_id,)))

    @staticmethod
    def refresh_physical_cover(data_structure: DataStructure, element_list):
        pass
