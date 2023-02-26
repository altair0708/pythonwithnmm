import sys
import numpy as np
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.crack_3D.CrackElementBase3D import Element3D, Surface3D, schmidt_orthogonalization
from typing import List


def change_adjacent_element_crack_status(element_list: List[Element3D], element_id_set: set):
    element_id_set.discard(-1)
    for each_element_id in element_id_set:
        if element_list[each_element_id].cracked == 0:
            element_list[each_element_id].cracked = 1


def generate_crack_surface(element: Element3D):
    edge_vtk_cell_list = []
    vector_list = []
    max_strain = element.strain.max_component[1]
    for each_surface_cell in element.surface_cell_list:
        if each_surface_cell.cracked > 0:
            edge_vtk_cell_list.append(each_surface_cell.crack_edge)
            vector_list.append(each_surface_cell.edge_vector)
    try:
        origin_point = edge_vtk_cell_list[0].GetPoints().GetPoint(0)
    except IndexError:
        # error_grid = vtkUnstructuredGrid()
        # for each_surface_cell in element.surface_cell_list:
        #     insert_a_cell(error_grid, each_surface_cell.vtk_cell)
        # writer = vtkXMLUnstructuredGridWriter()
        # writer.SetFileName('error.vtu')
        # writer.SetInputData(error_grid)
        # writer.Write()
        sys.exit()

    if len(edge_vtk_cell_list) == 1:
        vector_0 = vector_list[0]

        # specify propagation direction
        # normal_vector = schmidt_orthogonalization(vector_0, (0, 1, 0))
        normal_vector = schmidt_orthogonalization(vector_0, (0, 0, 1))

        # don't specify propagation direction
        # max_strain = schmidt_orthogonalization(max_strain, (0, 1, 0))
        # normal_vector = schmidt_orthogonalization(vector_0, max_strain)

    elif len(edge_vtk_cell_list) > 1:
        vector_0 = vector_list[0]
        vector_1 = vector_list[1]
        normal_vector = np.cross(vector_0, vector_1)
        # if len(edge_vtk_cell_list) > 2:
        #     print('33333333')
    else:
        raise Exception('edge number error!')

    try:
        surface_vtk_cell, _, _ = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
    except AssertionError:
        return None

    element.crack_surface = surface_vtk_cell
    return origin_point, normal_vector


def generate_crack_edge(surface: Surface3D, origin_point, normal_vector):
    surface_vtk_cell = surface.vtk_cell
    try:
        edge_vtk_cell, _, _ = clip_a_vtk_cell(surface_vtk_cell, origin_point, normal_vector)
    except AssertionError:
        # surface.cracked = 0
        return False
    surface.cracked = 1
    surface.crack_edge = edge_vtk_cell
    assert edge_vtk_cell.GetPoints().GetNumberOfPoints() != 0
    return True


class ElementCracker3D(object):
    @staticmethod
    def crack_all_element(element_list: List[Element3D]):

        element_id_set = set()
        for each_element in element_list:
            result = ElementCracker3D.crack_an_element(each_element)
            if result is None:
                continue
            element_id_set = element_id_set.union(result)
        change_adjacent_element_crack_status(element_list, element_id_set)

    @staticmethod
    def crack_an_element(element: Element3D):
        # element crack!!!

        # if element.strain.max_component[0] > 0.00001 and element.cracked == 2:
        if element.cracked == 2:
            element.cracked = 3

        # deliver adjacent element information
        adjacent_element_set = set()
        if element.cracked == 3:

            # generate crack surface
            result = generate_crack_surface(element)
            if result is None:
                element.cracked = 2
                return None
            origin_point = result[0]
            normal_vector = result[1]

            surface_list: List[Surface3D] = element.surface_cell_list
            for each_surface_cell in surface_list:
                # generate crack edge
                if each_surface_cell.cracked == 0:

                    result = generate_crack_edge(each_surface_cell, origin_point, normal_vector)
                    if result is False:
                        continue

                    adjacent_element_id_list = each_surface_cell.element_id
                    for each_element_id in adjacent_element_id_list:
                        adjacent_element_set.add(each_element_id)

        # initial crack
        elif element.cracked == 9:
            surface_list: List[Surface3D] = element.surface_cell_list
            for each_surface_cell in surface_list:
                # adjacent element id
                if each_surface_cell.cracked == 9:
                    adjacent_element_id_list = each_surface_cell.element_id
                    for each_element_id in adjacent_element_id_list:
                        adjacent_element_set.add(each_element_id)

        return adjacent_element_set
