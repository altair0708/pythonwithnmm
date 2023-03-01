import sys
import numpy as np
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.base.CleanUnstructuredGridFunction import clean_unstructured_grid, clean_poly_data
from NMM.base.CheckDihedralAngle import check_dihedral_angle
from NMM.crack_3D.CrackElementBase3D import Element3D, Surface3D, schmidt_orthogonalization
from NMM.base.WriteErrorVTU import write_error_vtu
from typing import List
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkGenericCell, vtkPolyData


def change_adjacent_element_crack_status(element_list: List[Element3D], element_id_set: set):
    element_id_set.discard(-1)
    for each_element_id in element_id_set:
        if element_list[each_element_id].cracked == 0:
            element_list[each_element_id].cracked = 1


def generate_crack_surface(element: Element3D):

    # crack edge in element surface
    edge_vtk_cell_list = []

    # cracked adjacent element
    element_cell_list = []

    # vector of crack edge
    vector_list = []
    max_strain = element.strain.max_component[1]
    for each_surface_cell in element.surface_cell_list:
        if each_surface_cell.cracked > 0:

            temp_element = each_surface_cell.element_cell_list[0]
            if temp_element.cracked != 4:
                temp_element = each_surface_cell.element_cell_list[1]
            element_cell_list.append(temp_element)

            if element.id == 4355:
                print(each_surface_cell.element_id)

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
        # project: crack_module_study
        normal_vector = schmidt_orthogonalization(vector_0, (0, 1, 0))

        # project: crack_generate_direction
        # normal_vector = schmidt_orthogonalization(vector_0, (-10, 0, 1))

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

    # check if the dihedral angle of two crack is Acute Angle
    if len(element_cell_list) == 1:

        temp_element_cell: Element3D = element_cell_list[0]
        assert temp_element_cell.cracked == 4
        temp_crack_surface_vtk_cell = vtkGenericCell()
        temp_crack_surface_vtk_cell.SetCellType(temp_element_cell.crack_surface.GetCellType())
        temp_crack_surface_vtk_cell.DeepCopy(temp_element_cell.crack_surface)

        new_crack_surface_vtk_cell = vtkGenericCell()
        new_crack_surface_vtk_cell.SetCellType(surface_vtk_cell.GetCellType())
        new_crack_surface_vtk_cell.DeepCopy(surface_vtk_cell)

        test_grid = vtkUnstructuredGrid()
        insert_a_cell_0(test_grid, temp_crack_surface_vtk_cell)
        insert_a_cell_0(test_grid, new_crack_surface_vtk_cell)
        # write_error_vtu(test_grid, 0)

        if check_dihedral_angle(test_grid) is False:
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
