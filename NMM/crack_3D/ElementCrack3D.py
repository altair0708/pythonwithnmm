import sys
import numpy as np
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.base.CheckDihedralAngle import check_dihedral_angle, generate_vector
from NMM.crack_3D.CrackElementBase3D import Element3D, Surface3D, schmidt_orthogonalization
from NMM.base.WriteErrorVTU import write_error_vtu
from typing import List
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkGenericCell, vtkPolyData, VTK_LINE
from vtkmodules.vtkCommonCore import vtkIdList


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

            edge_vtk_cell_list.append(each_surface_cell.crack_edge)
            vector_list.append(each_surface_cell.edge_vector)
    try:
        origin_point = edge_vtk_cell_list[0].GetPoints().GetPoint(0)
    except IndexError:
        error_grid = vtkUnstructuredGrid()
        for each_surface_cell in element.surface_cell_list:
            insert_a_cell_0(error_grid, each_surface_cell.vtk_cell)
        write_error_vtu(error_grid, 0)
        sys.exit()

    # check the total number of crack edge
    u_grid = vtkUnstructuredGrid()
    for each_edge_sequence in range(len(edge_vtk_cell_list)):
        temp_edge_vtk_cell = vtkGenericCell()
        temp_edge_vtk_cell.SetCellType(VTK_LINE)
        temp_edge_vtk_cell.DeepCopy(edge_vtk_cell_list[each_edge_sequence])
        insert_a_cell_0(u_grid, temp_edge_vtk_cell)
    print('edge 3:', u_grid.GetNumberOfPoints())

    if len(edge_vtk_cell_list) == 1:
        vector_0 = vector_list[0]

        # specify propagation direction
        # project: crack_module_study
        normal_vector = schmidt_orthogonalization(vector_0, (0, 1, 0))

        # project: crack_generate_direction
        # normal_vector = schmidt_orthogonalization(vector_0, (0, 0, 1))

        # don't specify propagation direction
        # max_strain = schmidt_orthogonalization(max_strain, (0, 1, 0))
        # normal_vector = schmidt_orthogonalization(vector_0, max_strain)

    elif len(edge_vtk_cell_list) == 2:
        vector_0 = vector_list[0]
        vector_1 = vector_list[1]
        normal_vector = np.cross(vector_0, vector_1)

        # edge_0 = vtkGenericCell()
        # edge_0.SetCellType(VTK_LINE)
        # edge_0.DeepCopy(edge_vtk_cell_list[0])
        #
        # edge_1 = vtkGenericCell()
        # edge_1.SetCellType(VTK_LINE)
        # edge_1.DeepCopy(edge_vtk_cell_list[1])
        #
        # u_grid = vtkUnstructuredGrid()
        # insert_a_cell_0(u_grid, edge_0)
        # insert_a_cell_0(u_grid, edge_1)
        # print('edge 2:', u_grid.GetNumberOfPoints())

    elif len(edge_vtk_cell_list) == 3:

        # try to get the point used by two edges
        double_id_list = []
        for each_cell_id in range(u_grid.GetNumberOfCells()):
            temp_id_list = vtkIdList()
            temp_id_list.DeepCopy(u_grid.GetCell(each_cell_id).GetPointIds())
            for each_point_id in range(temp_id_list.GetNumberOfIds()):
                double_id_list.append(temp_id_list.GetId(each_point_id))
        single_id_list = [i for i in range(u_grid.GetNumberOfPoints())]
        # insert_a_cell_0 will insert a additional point(0, 0, 0, id = 0) which need to be remove
        single_id_list.remove(0)
        for each_point_id in single_id_list:
            double_id_list.remove(each_point_id)
        print('edge 3:', len(double_id_list))

        surface_vtk_cell_grid = vtkUnstructuredGrid()
        for each_point_id in double_id_list:
            cell_id_list = vtkIdList()
            u_grid.GetPointCells(each_point_id, cell_id_list)

            vector_list = []
            for each_cell_sequence in range(cell_id_list.GetNumberOfIds()):
                temp_cell_id = cell_id_list.GetId(each_cell_sequence)
                temp_cell = vtkGenericCell()
                temp_cell.DeepCopy(u_grid.GetCell(temp_cell_id))

                assert temp_cell.GetNumberOfPoints() == 2
                end_point_id = temp_cell.GetPointId(0)
                if end_point_id == each_point_id:
                    end_point_id = temp_cell.GetPointId(1)
                vector_list.append(generate_vector(u_grid, end_point_id, each_point_id))

            assert len(vector_list) == 2
            vector_0 = vector_list[0]
            vector_1 = vector_list[1]
            normal_vector = np.cross(vector_0, vector_1)
            origin_point = u_grid.GetPoint(each_point_id)

            surface_vtk_cell, _, _ = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
            insert_a_cell_0(surface_vtk_cell_grid, surface_vtk_cell)
        write_error_vtu(surface_vtk_cell_grid, 0)

        # # find an uncracked surface
        # uncracked_surface_vtk_cell = None
        # for each_surface_cell in element.surface_cell_list:
        #     if each_surface_cell.cracked == 0:
        #         uncracked_surface_vtk_cell = vtkGenericCell()
        #         uncracked_surface_vtk_cell.SetCellType(each_surface_cell.vtk_cell.GetCellType())
        #         uncracked_surface_vtk_cell.DeepCopy(each_surface_cell.vtk_cell)
        #         break
        # if uncracked_surface_vtk_cell is None:
        #     raise Exception('Cannot find uncracked surface!')
        #
        # # find which crack edge intersect with the uncracked surface
        # for sequence, each_crack_edge_vtk_cell in enumerate(edge_vtk_cell_list):
        #     if uncracked_surface_vtk_cell.IntersectWithCell(each_crack_edge_vtk_cell) == 1:
        #         vector_list.pop(sequence)
        #         edge_vtk_cell_list.pop(sequence)
        #
        # if len(vector_list) == 2:
        #     vector_0 = vector_list[0]
        #     vector_1 = vector_list[1]
        #     normal_vector = np.cross(vector_0, vector_1)
        # elif len(vector_list) == 3:
        #     # try to get the point used by two edges
        #     double_id_list = []
        #     for each_cell_id in range(u_grid.GetNumberOfCells()):
        #         temp_id_list = vtkIdList()
        #         temp_id_list.DeepCopy(u_grid.GetCell(each_cell_id).GetPointIds())
        #         for each_point_id in range(temp_id_list.GetNumberOfIds()):
        #             double_id_list.append(temp_id_list.GetId(each_point_id))
        #     single_id_list = [i for i in range(u_grid.GetNumberOfPoints())]
        #
        #     for each_point_id in single_id_list:
        #         double_id_list.remove(each_point_id)
        #     print('edge 3:', len(double_id_list))
        # else:
        #     raise Exception('edge number error!')
    else:
        raise Exception('edge number error!')

    # elif 1 < len(edge_vtk_cell_list) < 4:
    #     vector_0 = vector_list[0]
    #     vector_1 = vector_list[1]
    #     normal_vector = np.cross(vector_0, vector_1)
    # else:
    #     raise Exception('edge number error!')

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
