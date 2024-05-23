import sys
from NMM.GlobalVariable import DataStructure, CrackList
from NMM.base.PropertyGetSetFunction import set_property, get_property
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.crack_3D.ElementBase3D import Element3D
from NMM.crack_3D.SurfaceBase3D import Surface3D
from NMM.crack_3D.CrackSurfaceBase3D import CrackSurface3D
from NMM.crack_3D.CrackEdgeBase3D import CrackEdge3D
from typing import List
import numpy as np

# element
# surface
# crack surface
# edge


class CrackElementRefresher:
    @staticmethod
    def refresh_manifold_element(data_structure: DataStructure, element_list: List[Element3D]):
        element_grid = data_structure.manifold_element.content
        for i, each_element_cell in enumerate(element_list):
            temp_cracked = each_element_cell.cracked
            set_property(element_grid, 'cracked', i, np.array((temp_cracked,)))

            # strain 1
            set_property(element_grid, 'strain_1', i, np.array(each_element_cell.strain.component_vector_1[1]).reshape(3))
            set_property(element_grid, 'strain_1_value', i, np.array(each_element_cell.strain.component_vector_1[0]).reshape(1))
            # strain 2
            set_property(element_grid, 'strain_2', i, np.array(each_element_cell.strain.component_vector_2[1]).reshape(3))
            set_property(element_grid, 'strain_2_value', i, np.array(each_element_cell.strain.component_vector_2[0]).reshape(1))
            # strain 3
            set_property(element_grid, 'strain_3', i, np.array(each_element_cell.strain.component_vector_3[1]).reshape(3))
            set_property(element_grid, 'strain_3_value', i, np.array(each_element_cell.strain.component_vector_3[0]).reshape(1))
            # strain max
            set_property(element_grid, 'strain_Max', i, np.array(each_element_cell.strain.max_component_vector[1]).reshape(3))
            set_property(element_grid, 'strain_Max_value', i, np.array(each_element_cell.strain.max_component_vector[0]).reshape(1))

            # this time step have ability to crack
            if temp_cracked == 1:
                set_property(element_grid, 'cracked', i, np.array((2,)))
            # this time step cracked
            elif temp_cracked == 3:
                # insert the crack information of the element model
                set_property(element_grid, 'cracked', i, np.array((4,)))
                set_property(element_grid, 'crack_surface_id', i, each_element_cell.crack_surface_id)

    @staticmethod
    def refresh_element_surface(data_structure: DataStructure, surface_list: List[Surface3D]):
        surface_grid = data_structure.element_surface.content
        for i, each_surface_cell in enumerate(surface_list):
            temp_cracked = each_surface_cell.cracked
            set_property(surface_grid, 'cracked', i, np.array((temp_cracked,)))
            # this time step cracked
            if temp_cracked == 1:
                # insert the crack information of the element model
                set_property(surface_grid, 'cracked', i, np.array((2,)))
                set_property(surface_grid, 'edge_id', i, each_surface_cell.crack_edge_id)

    @staticmethod
    def refresh_crack_surface(data_structure: DataStructure, crack_surface_list: List[CrackSurface3D]):
        crack_surface_grid = data_structure.crack_surface.content
        last_crack_surface_number = crack_surface_grid.GetNumberOfCells()
        for each_crack_surface_cell in crack_surface_list[last_crack_surface_number:]:
            # vtk cell
            insert_a_cell_0(crack_surface_grid, each_crack_surface_cell.vtk_cell)
            # element id
            set_property(crack_surface_grid, 'element_id', each_crack_surface_cell.id, each_crack_surface_cell.element_id)
            # crack edge id
            set_property(crack_surface_grid, 'edge_id', each_crack_surface_cell.id, each_crack_surface_cell.crack_edge_id)

    @staticmethod
    def refresh_crack_edge(data_structure: DataStructure, crack_edge_list: List[CrackEdge3D]):
        crack_edge_grid = data_structure.crack_edge.content
        last_crack_edge_number = crack_edge_grid.GetNumberOfCells()
        for each_crack_edge_cell in crack_edge_list[last_crack_edge_number:]:
            # vtk cell
            insert_a_cell_0(crack_edge_grid, each_crack_edge_cell.vtk_cell)
            # surface id
            set_property(crack_edge_grid, 'surface_id', each_crack_edge_cell.id, each_crack_edge_cell.surface_id)
            # crack surface id
            set_property(crack_edge_grid, 'crack_surface_id', each_crack_edge_cell.id, each_crack_edge_cell.crack_surface_id)

    @staticmethod
    def refresh_physical_cover(data_structure: DataStructure, element_list):
        pass

    @staticmethod
    def refresh_new_element(data_structure: DataStructure, new_element_list):
        new_element_grid = data_structure.new_element.content
        for each_new_element_cell in new_element_list:
            # vtk cell
            # print(each_new_element_cell.vtk_cell)
            # print(each_new_element_cell.id)
            # print(each_new_element_cell.super_id)
            # print(each_new_element_cell.adjacent_id)
            insert_a_cell(new_element_grid, each_new_element_cell.vtk_cell)
            # id in new_element_grid
            set_property(new_element_grid, 'id', each_new_element_cell.id, np.array((each_new_element_cell.id, )))
            # id of super element
            set_property(new_element_grid, 'element_id', each_new_element_cell.id, np.array((each_new_element_cell.super_id, )))
            # id of adjacent element
            set_property(new_element_grid, 'adjacent_element_id', each_new_element_cell.id, np.array((each_new_element_cell.adjacent_id, )))
