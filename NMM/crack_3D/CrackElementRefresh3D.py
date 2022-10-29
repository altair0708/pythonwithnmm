from NMM.GlobalVariable import DataStructure
from NMM.base.PropertyGetSetFunction import set_property
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
            temp_crack_new = element_list[element_id].crack_new
            temp_surface = element_list[element_id].crack_surface
            if temp_crack:
                set_property(temp_vtk_model, 'cracked', element_id, np.array((1, )))
                if temp_crack_new:
                    insert_a_cell(temp_crack_vtk, temp_surface)
            elif not temp_crack:
                set_property(temp_vtk_model, 'cracked', element_id, np.array((0, )))


    @staticmethod
    def refresh_physical_cover(data_structure: DataStructure, element_list):
        pass
