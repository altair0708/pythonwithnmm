import sys
import math
import numpy as np
from NMM.GlobalVariable import Variable, CrackList, CONST
from NMM.base.CalculateArea import calculate_area
from NMM.base.CopyFunction import copy_vtk_cell
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.base.CheckDihedralAngle import check_dihedral_angle, generate_vector, check_dihedral_angle_0
from NMM.crack_3D.ElementBase3D import Element3D, schmidt_orthogonalization
from NMM.crack_3D.SurfaceBase3D import Surface3D
from NMM.crack_3D.CrackSurfaceBase3D import CrackSurface3D
from NMM.crack_3D.CrackEdgeBase3D import CrackEdge3D
from NMM.base.CheckPointInPolygon import check_point_in_polygon
from NMM.base.WriteErrorVTU import write_error_vtu
from typing import List
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkGenericCell, vtkCell, vtkTetra, VTK_TETRA, VTK_TRIANGLE
from vtkmodules.vtkCommonCore import vtkPoints


def clip_an_element(element: Element3D):

    max_strain = element.strain.max_component_vector[1]

    # crack edge in element surface
    crack_edge_cell_list = []
    for each_surface_cell in element.surface_cell_list:
        each_surface_cell: Surface3D = each_surface_cell

        if each_surface_cell.cracked > 0:
            crack_edge_cell: CrackEdge3D = each_surface_cell.crack_edge_cell_list[0]
            # try:
            #     vector_0 = crack_edge_cell.vector
            # except AttributeError:
            #     print(each_surface_cell.crack_edge_cell_list)
            #     print(each_surface_cell.crack_edge_id)
            #     print(each_surface_cell.cracked)
            #     print(each_surface_cell.id)
            #     sys.exit()
            crack_edge_cell_list.append(crack_edge_cell)

    if element.id == 3258:
        print('crack edge number: ', len(crack_edge_cell_list))

    if len(crack_edge_cell_list) == 1:

        crack_edge_cell = crack_edge_cell_list[0]
        vector_0 = crack_edge_cell.vector
        origin_point = crack_edge_cell.point_0

        # assert crack edge only relate one crack surface
        assert crack_edge_cell.crack_surface_id[1] == -1

        # specify propagation direction
        # project: crack_module_study
        # normal_vector = schmidt_orthogonalization(vector_0, (0, 1, 0))

        # project: crack_generate_direction
        # normal_vector = schmidt_orthogonalization(vector_0, (0, 0, 1))

        # don't specify propagation direction
        # max_strain = schmidt_orthogonalization(max_strain, (0, 1, 0))
        normal_vector = schmidt_orthogonalization(vector_0, max_strain)
        try:
            new_crack_surface_vtk_cell, _, _ = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
        except AssertionError:
            return None

        # ensure the area of crack surface > 0
        temp_points = vtkPoints()
        temp_points.DeepCopy(new_crack_surface_vtk_cell.GetPoints())
        area_0 = calculate_area(temp_points)
        # if math.isnan(calculate_area(temp_points)):
        #     return None
        if not area_0 > 0.001:
            return None

        # check if the dihedral angle of two crack is Acute Angle
        assert crack_edge_cell.crack_surface_id[0] != -1
        crack_surface_cell: CrackSurface3D = crack_edge_cell.crack_surface_cell_list[0]

        crack_surface_vtk_cell: vtkCell = crack_surface_cell.vtk_cell
        # crack_surface_vtk_cell = copy_vtk_cell(crack_surface_vtk_cell, crack_surface_vtk_cell.GetPoints())

        crack_surface_vtk_cell_0 = vtkGenericCell()
        crack_surface_vtk_cell_0.SetCellType(crack_surface_vtk_cell.GetCellType())
        crack_surface_vtk_cell_0.DeepCopy(crack_surface_vtk_cell)

        crack_surface_vtk_cell_1 = vtkGenericCell()
        crack_surface_vtk_cell_1.SetCellType(new_crack_surface_vtk_cell.GetCellType())
        crack_surface_vtk_cell_1.DeepCopy(new_crack_surface_vtk_cell)

        test_grid = vtkUnstructuredGrid()
        insert_a_cell_0(test_grid, crack_surface_vtk_cell_0)
        insert_a_cell_0(test_grid, crack_surface_vtk_cell_1)
        # insert_a_cell_0(test_grid, edge_vtk_cell_list[0])

        assert test_grid.GetNumberOfCells() == 2
        # if element.id == 1302 or element.id == 2609:
        #     print('1:', check_dihedral_angle(test_grid))
        #     write_error_vtu(test_grid, element.id)
        try:
            if check_dihedral_angle_0(test_grid) is False:
                # print('before:', normal_vector)
                # normal_vector = schmidt_orthogonalization(vector_0, -max_strain)

                # nx = vector_0[0]
                # ny = vector_0[1]
                # nz = vector_0[2]
                # thet = 185
                # costhet = np.math.cos((thet/180)*np.pi)
                # sinthet = np.math.sin((thet/180)*np.pi)
                # rotation_matrix = np.array([[nx**2*(1-costhet) + costhet, nx*ny*(1-costhet) - nz*sinthet, nx*nz*(1-costhet) + ny*sinthet],
                #                             [nx*ny*(1-costhet) + nz*sinthet, ny**2*(1-costhet) + costhet, ny*nz*(1-costhet) - nx*sinthet],
                #                             [nx*nz*(1-costhet) - ny*sinthet, ny*nz*(1-costhet) + nx*sinthet, nz**2*(1-costhet) + costhet]])
                #
                # normal_vector = np.dot(np.array(normal_vector).reshape((1, 3)), rotation_matrix)
                #
                # # print('after:', normal_vector)
                # try:
                #     new_crack_surface_vtk_cell, _, _ = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
                # except AssertionError:
                #     return None
                return None

                # insert_a_cell_0(test_grid, new_crack_surface_vtk_cell)
                # write_error_vtu(test_grid, element.id + 1)
        except AssertionError:
            print('area 0:', area_0)
            sys.exit()

        generate_crack_surface_cell(new_crack_surface_vtk_cell, element)

    elif len(crack_edge_cell_list) == 2:

        crack_edge_grid = vtkUnstructuredGrid()
        for each_crack_edge_cell in crack_edge_cell_list:
            temp_edge = vtkGenericCell()
            temp_edge.SetCellType(each_crack_edge_cell.vtk_cell.GetCellType())
            temp_edge.DeepCopy(each_crack_edge_cell.vtk_cell)
            insert_a_cell_0(crack_edge_grid, temp_edge)

        # actual point number is 3, 4 is include (0, 0, 0)
        if crack_edge_grid.GetNumberOfPoints() == 4:
            vector_0 = crack_edge_cell_list[0].vector
            vector_1 = crack_edge_cell_list[1].vector

            normal_vector = np.cross(vector_0, vector_1)
            origin_point = crack_edge_cell_list[0].point_0
            try:
                new_crack_surface_vtk_cell, _, _ = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
            except AssertionError:
                return None

            # ensure the area of crack surface > 0
            temp_points = vtkPoints()
            temp_points.DeepCopy(new_crack_surface_vtk_cell.GetPoints())
            if not calculate_area(temp_points) > 0.001:
                return None

            generate_crack_surface_cell(new_crack_surface_vtk_cell, element)

        elif crack_edge_grid.GetNumberOfPoints() == 5:

            new_crack_surface_vtk_cell = vtkTetra()
            new_crack_surface_vtk_cell.GetPointIds().SetId(0, 1)
            new_crack_surface_vtk_cell.GetPointIds().SetId(1, 2)
            new_crack_surface_vtk_cell.GetPointIds().SetId(2, 3)
            new_crack_surface_vtk_cell.GetPointIds().SetId(3, 4)

            crack_surface_vtk_cell = copy_vtk_cell(new_crack_surface_vtk_cell, crack_edge_grid.GetPoints())
            generate_crack_surface_cell(crack_surface_vtk_cell, element)

    elif len(crack_edge_cell_list) >= 3:

        crack_edge_grid = vtkUnstructuredGrid()
        for each_crack_edge_cell in crack_edge_cell_list:
            temp_edge = vtkGenericCell()
            temp_edge.SetCellType(each_crack_edge_cell.vtk_cell.GetCellType())
            temp_edge.DeepCopy(each_crack_edge_cell.vtk_cell)
            insert_a_cell_0(crack_edge_grid, temp_edge)

        if crack_edge_grid.GetNumberOfPoints() == 4:
            vector_0 = crack_edge_cell_list[0].vector
            vector_1 = crack_edge_cell_list[1].vector

            if element.id == 3258:
                print('crack point number: ', crack_edge_grid.GetNumberOfPoints())

            normal_vector = np.cross(vector_0, vector_1)
            origin_point = crack_edge_cell_list[0].point_0
            try:
                new_crack_surface_vtk_cell, _, _ = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
            except AssertionError:
                return None

            # ensure the area of crack surface > 0
            temp_points = vtkPoints()
            temp_points.DeepCopy(new_crack_surface_vtk_cell.GetPoints())
            if not calculate_area(temp_points) > 0.001:
                return None

            generate_crack_surface_cell(new_crack_surface_vtk_cell, element)

        # point number == 5, because there is an initial point == (0, 0, 0), actually there are 4 real points.
        if crack_edge_grid.GetNumberOfPoints() == 5:
            new_crack_surface_vtk_cell = vtkTetra()
            new_crack_surface_vtk_cell.GetPointIds().SetId(0, 1)
            new_crack_surface_vtk_cell.GetPointIds().SetId(1, 2)
            new_crack_surface_vtk_cell.GetPointIds().SetId(2, 3)
            new_crack_surface_vtk_cell.GetPointIds().SetId(3, 4)

            crack_surface_vtk_cell = copy_vtk_cell(new_crack_surface_vtk_cell, crack_edge_grid.GetPoints())
            generate_crack_surface_cell(crack_surface_vtk_cell, element)
        else:
            return None

    else:
        return None
        # raise Exception('edge number error: ', len(crack_edge_cell_list))


def generate_crack_surface_cell(crack_surface_vtk_cell: vtkCell, element: Element3D):
    # crack surface cell
    new_crack_surface_cell = CrackSurface3D(Variable.crack_surface_number)
    new_crack_surface_cell.vtk_cell = crack_surface_vtk_cell

    new_crack_surface_cell.element_id[0] = element.id
    new_crack_surface_cell.element_cell_list[0] = element

    # element
    element.cracked = 3
    element.crack_surface_id[0] = new_crack_surface_cell.id
    element.crack_surface_cell_list[0] = new_crack_surface_cell
    for i, each_surface_cell in enumerate(element.surface_cell_list):
        # Do not crack
        if each_surface_cell.cracked == 0:
            temp_crack_edge_cell = generate_crack_edge_cell(each_surface_cell, new_crack_surface_cell, Variable.crack_edge_number)
            if temp_crack_edge_cell is False:
                continue

            # surface
            each_surface_cell.cracked = 1
            each_surface_cell.crack_edge_id[0] = temp_crack_edge_cell.id
            each_surface_cell.crack_edge_cell_list[0] = temp_crack_edge_cell

            # new crack surface
            new_crack_surface_cell.crack_edge_id[i] = temp_crack_edge_cell.id
            new_crack_surface_cell.crack_edge_cell_list[i] = temp_crack_edge_cell

            # new crack edge
            CrackList.crack_edge_list.append(temp_crack_edge_cell)
            Variable.crack_edge_number += 1
        # cracked in this time step
        elif each_surface_cell.cracked == 1:
            temp_crack_edge_cell: CrackEdge3D = each_surface_cell.crack_edge_cell_list[0]
            new_crack_surface_cell.crack_edge_id[i] = temp_crack_edge_cell.id
            new_crack_surface_cell.crack_edge_cell_list[i] = temp_crack_edge_cell

        # cracked in previous step
        elif each_surface_cell.cracked == 2:
            temp_crack_edge_cell: CrackEdge3D = each_surface_cell.crack_edge_cell_list[0]
            new_crack_surface_cell.crack_edge_id[i] = temp_crack_edge_cell.id
            new_crack_surface_cell.crack_edge_cell_list[i] = temp_crack_edge_cell

    CrackList.crack_surface_list.append(new_crack_surface_cell)
    Variable.crack_surface_number += 1


def generate_crack_edge_cell(surface: Surface3D, crack_surface: CrackSurface3D, crack_edge_id: int):
    if crack_surface.type == VTK_TETRA:
        crack_surface_vtk_cell: vtkTetra = crack_surface.vtk_cell

        point_list = []
        for each_point_sequence in range(crack_surface_vtk_cell.GetNumberOfPoints()):
            temp_point = crack_surface_vtk_cell.GetPoints().GetPoint(each_point_sequence)
            if check_point_in_polygon(temp_point, surface.vtk_cell):
                point_list.append(temp_point)

        # if crack_surface.element_id[0] == 2835:
        #     print(point_list)
        #     print(len(point_list))

        if len(point_list) != 2:
            return False
        else:
            temp_edge_vtk_cell = vtkGenericCell()
            temp_edge_vtk_cell.SetCellTypeToLine()
            temp_edge_vtk_cell.GetPointIds().SetId(0, 0)
            temp_edge_vtk_cell.GetPointIds().SetId(1, 1)

            temp_points = vtkPoints()
            temp_points.InsertNextPoint(point_list[0])
            temp_points.InsertNextPoint(point_list[1])

            temp_grid = vtkUnstructuredGrid()
            temp_grid.InsertNextCell(temp_edge_vtk_cell.GetCellType(), temp_edge_vtk_cell.GetPointIds())
            temp_grid.SetPoints(temp_points)
            edge_vtk_cell = temp_grid.GetCell(0)

            # if crack_surface.element_id[0] == 2835:
            #     print(point_list)
            #     print(edge_vtk_cell)

    else:
        surface_vtk_cell = surface.vtk_cell
        origin_point = crack_surface.point_0
        normal_vector = crack_surface.normal_vector
        try:
            edge_vtk_cell, _, _ = clip_a_vtk_cell(surface_vtk_cell, origin_point, normal_vector)
        except AssertionError:
            # surface.cracked = 0
            return False

    crack_edge_cell = CrackEdge3D(crack_edge_id)
    crack_edge_cell.vtk_cell = edge_vtk_cell

    crack_edge_cell.surface_id[0] = surface.id
    crack_edge_cell.surface_cell_list[0] = surface

    crack_edge_cell.crack_surface_id[0] = crack_surface.id
    crack_edge_cell.crack_surface_cell_list[0] = crack_surface

    return crack_edge_cell


class ElementCracker3D(object):
    @staticmethod
    def crack_all_element(element_list: List[Element3D]):
        for each_element in element_list:
            ElementCracker3D.crack_an_element(each_element)

    @staticmethod
    def crack_an_element(element: Element3D):
        # element crack!!!

        # if element.strain.max_component[0] > 0.00001 and element.cracked == 2:
        if element.cracked == 2 and element.strain.max_component_vector[0] > 0.00001:
            element.cracked = 3

        # crack propagation anyway
        # if element.cracked == 2:
        #     element.cracked = 3

        if element.cracked == 3:
            # generate crack surface
            clip_an_element(element)

