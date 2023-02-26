import sys

from NMM.GlobalVariable import DataStructure
from NMM.base.PropertyGetSetFunction import set_property, get_property
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.crack_3D.CrackElementBase3D import Element3D, Surface3D
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
        crack_surface_grid = data_structure.crack_surface.content

        for i, each_element_cell in enumerate(element_list):
            temp_cracked = each_element_cell.cracked
            temp_crack_surface_vtk = each_element_cell.crack_surface

            set_property(element_grid, 'cracked', i, np.array((temp_cracked,)))

            # this time step have ability to crack
            if temp_cracked == 1:
                set_property(element_grid, 'cracked', i, np.array((2,)))

            # this time step cracked
            elif temp_cracked == 3:
                # the number of crack surface in recent crack surface model
                crack_number = crack_surface_grid.GetNumberOfCells()

                # insert the crack information of the element model
                set_property(element_grid, 'cracked', i, np.array((4,)))
                set_property(element_grid, 'crack_surface_id', i, np.array((crack_number,)))

                # insert the crack surface into crack surface model
                insert_a_cell(crack_surface_grid, temp_crack_surface_vtk)
                assert i == each_element_cell.id
                set_property(crack_surface_grid, 'element_id', crack_number, np.array((i,)))

            # initial crack
            elif temp_cracked == 9:
                set_property(element_grid, 'cracked', i, np.array((4,)))

    @staticmethod
    def refresh_element_surface(data_structure: DataStructure, surface_list: List[Surface3D]):

        surface_grid = data_structure.element_surface.content
        edge_grid = data_structure.crack_edge.content
        for i, each_surface_cell in enumerate(surface_list):
            temp_cracked = each_surface_cell.cracked
            temp_edge_vtk = each_surface_cell.crack_edge

            set_property(surface_grid, 'cracked', i, np.array((temp_cracked,)))

            # this time step cracked
            if temp_cracked == 1:
                set_property(surface_grid, 'cracked', i, np.array((2,)))

                crack_number = edge_grid.GetNumberOfCells()

                # insert the crack information of the element model
                set_property(surface_grid, 'cracked', i, np.array((2,)))
                set_property(surface_grid, 'edge_id', i, np.array((crack_number,)))

                # insert the crack surface into crack surface model
                insert_a_cell(edge_grid, temp_edge_vtk)
                set_property(edge_grid, 'surface_id', crack_number, np.array((i,)))

            # initial crack
            elif temp_cracked == 9:
                set_property(surface_grid, 'cracked', i, np.array((2,)))

    @staticmethod
    def refresh_physical_cover(data_structure: DataStructure, element_list):
        pass
