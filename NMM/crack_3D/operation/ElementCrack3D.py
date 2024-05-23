import sys
import numpy as np
from NMM.GlobalVariable import Variable, CrackList, CONST, CONFIG
from NMM.base.CalculateArea import calculate_area
from NMM.base.CopyFunction import copy_vtk_cell
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.base.ModifyVtkCell import insert_a_cell, insert_a_cell_0
from NMM.base.CheckDihedralAngle import check_dihedral_angle, generate_vector, check_dihedral_angle_0
from NMM.crack_3D.ElementBase3D import Element3D, schmidt_orthogonalization
from NMM.crack_3D.SurfaceBase3D import Surface3D
from NMM.crack_3D.CrackSurfaceBase3D import CrackSurface3D
from NMM.crack_3D.CrackEdgeBase3D import CrackEdge3D
from NMM.crack_3D.NewElementBase3D import NewElement3D, create_an_new_element
from NMM.base.CheckPointInPolygon import check_point_in_polygon
from NMM.base.WriteErrorVTU import write_error_vtu
from NMM.base.TensorBase import Tensor
from NMM.base.MohrFailure import mohr_failure
from typing import List
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkGenericCell, vtkCell, vtkTetra, VTK_TETRA, VTK_TRIANGLE
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.crack_3D.operation.CrackSurfaceOriginNormal.CrackTypeFactory import CrackTypeFactory


def clip_an_element_0(element: Element3D):
    origin_point, normal_vector, crack_type = calculate_origin_point_normal_vector(element)

    # Propagation with a certain direction.
    # normal_vector = (0, 1, 0)
    try:
        new_crack_surface_vtk_cell, new_element_grid_0, new_element_grid_1 = clip_a_vtk_cell(element.vtk_cell, origin_point, normal_vector)
    except AssertionError:
        return None
    generate_crack_surface_cell(new_crack_surface_vtk_cell, element)

    new_element_cell_0, new_element_cell_1 = generate_new_element_cell(new_element_grid_0,
                                                                       new_element_grid_1,
                                                                       element,
                                                                       Variable)

    CrackList.new_element_list.append(new_element_cell_0)
    CrackList.new_element_list.append(new_element_cell_1)


def calculate_origin_point_normal_vector(element: Element3D):
    max_strain = element.strain.max_component_vector[1]

    # crack edge in element surface
    crack_edge_cell_list = []
    for each_surface_cell in element.surface_cell_list:
        each_surface_cell: Surface3D = each_surface_cell

        if each_surface_cell.cracked > 0:
            crack_edge_cell: CrackEdge3D = each_surface_cell.crack_edge_cell_list[0]
            crack_edge_cell_list.append(crack_edge_cell)

    crack_edge_grid = vtkUnstructuredGrid()
    for each_crack_edge_cell in crack_edge_cell_list:
        temp_edge = vtkGenericCell()
        temp_edge.SetCellType(each_crack_edge_cell.vtk_cell.GetCellType())
        temp_edge.DeepCopy(each_crack_edge_cell.vtk_cell)
        insert_a_cell_0(crack_edge_grid, temp_edge)

    # flag of how many crack edges and crack points, first is crack edge number, second is crack point number.
    crack_type = -1

    if len(crack_edge_cell_list) == 1:
        crack_type = 12

    elif len(crack_edge_cell_list) == 2:

        # actual point number is 3, 4 is include (0, 0, 0)
        if crack_edge_grid.GetNumberOfPoints() == 4:
            crack_type = 23

        elif crack_edge_grid.GetNumberOfPoints() == 5:
            crack_type = 24

    elif len(crack_edge_cell_list) >= 3:

        if crack_edge_grid.GetNumberOfPoints() == 4:
            crack_type = 33

        # point number == 5, because there is an initial point == (0, 0, 0), actually there are 4 real points.
        elif crack_edge_grid.GetNumberOfPoints() == 5:
            crack_type = 34

        elif crack_edge_grid.GetNumberOfPoints() == 6:
            crack_type = 35

        elif crack_edge_grid.GetNumberOfPoints() == 7:
            crack_type = 36
    else:
        raise Exception('edge number error: ', len(crack_edge_cell_list))

    # origin point and normal vector of crack surface
    crack_type_factory = CrackTypeFactory.get_crack_type_factory(crack_type)
    origin_point, normal_vector = crack_type_factory.calculate_origin_point_normal_vector(crack_edge_cell_list, crack_edge_grid, max_strain)

    return origin_point, normal_vector, crack_type

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


def generate_new_element_cell(new_element_cell_grid_0: vtkUnstructuredGrid,
                              new_element_cell_grid_1: vtkUnstructuredGrid,
                              super_element: Element3D,
                              variable):

    cell_id_0 = variable.new_element_number
    cell_id_1 = variable.new_element_number + 1
    variable.new_element_number += 2

    new_element_cell_0, new_element_cell_1 = create_an_new_element(cell_id_0,
                                                                   cell_id_1,
                                                                   super_element,
                                                                   new_element_cell_grid_0,
                                                                   new_element_cell_grid_1)

    return new_element_cell_0, new_element_cell_1


class ElementCracker3D(object):
    @staticmethod
    def crack_all_element(element_list: List[Element3D]):
        for each_element in element_list:
            ElementCracker3D.crack_an_element(each_element)

    @staticmethod
    def crack_an_element(element: Element3D):
        # element crack!!!

        # max tensile strain
        # if element.strain.max_component[0] > 0.00001 and element.cracked == 2:
        # if element.cracked == 2 and element.strain.max_component_vector[0] > 0.00001:
        #     element.cracked = 3

        # # max tensile stress
        # if element.cracked == 2 and element.stress.max_component_vector[0] > 1000000:
        #     element.cracked = 3

        # # mohr criterion with tensile cutoff
        # with open('../../data_3D/material/material_coefficient.json') as f:
        #     material_json = json.load(f)
        #
        # material = json.dumps(material_json)
        #
        # assert type(element.stress) == Tensor
        # temp_stress = element.stress
        # result = mohr_failure(temp_stress, material)
        # if element.cracked == 2 and result > 0:
        #     element.cracked = 3

        # crack propagation anyway
        if element.cracked == 2:
            element.cracked = 3

        if element.cracked == 3:
            # generate crack surface
            clip_an_element_0(element)

