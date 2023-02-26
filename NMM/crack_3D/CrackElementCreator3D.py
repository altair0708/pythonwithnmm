import deprecation
from typing import List
from NMM.GlobalVariable import DataStructure, Variable
from NMM.crack_3D.CrackElementBase3D import Element3D, Surface3D
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_polyhedron, copy_vtk_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList

# element
# surface
# crack surface
# edge


def create_a_surface(data_structure: DataStructure, surface_id: int):

    # vtk element surface model
    surface_grid: vtkUnstructuredGrid = data_structure.element_surface.content

    # vtk edge model
    edge_grid: vtkUnstructuredGrid = data_structure.crack_edge.content

    # assemble a surface
    surface_cell = Surface3D(surface_id)

    # cracked flag
    surface_cracked_flag = get_property(surface_grid, 'cracked', surface_id)
    surface_cell.cracked = int(*surface_cracked_flag)
    if surface_cell.cracked == 2 or surface_cell.cracked == 9:
        edge_id = get_property(surface_grid, 'edge_id', surface_id)
        edge_id = int(*edge_id)

        edge_vtk_cell = edge_grid.GetCell(edge_id)
        edge_vtk_cell = copy_vtk_cell(edge_vtk_cell, edge_grid.GetPoints())

        surface_cell.crack_edge = edge_vtk_cell

    # vtk_cell
    surface_vtk_cell: vtkCell = surface_grid.GetCell(surface_id)
    surface_grid_points: vtkPoints = surface_grid.GetPoints()
    surface_cell.vtk_cell = copy_vtk_cell(surface_vtk_cell, surface_grid_points)

    # element id
    element_id_list = get_property(surface_grid, 'element_id', surface_id)
    for i, each_element_id in enumerate(element_id_list):
        surface_cell.element_id[i] = int(each_element_id)

    return surface_cell


def create_an_element(data_structure: DataStructure, element_id: int):

    # vtk element model
    element_grid: vtkUnstructuredGrid = data_structure.manifold_element.content
    # vtk crack surface model
    crack_surface_grid: vtkUnstructuredGrid = data_structure.crack_surface.content

    # assemble a crack element
    element_cell = Element3D(id_value=element_id)

    # strain_total
    element_cell.strain_total = get_property(element_grid, 'strain_total', element_id)

    # vtk_cell
    element_vtk_cell: vtkCell = element_grid.GetCell(element_id)
    element_grid_points: vtkPoints = element_grid.GetPoints()
    element_cell.vtk_cell = copy_polyhedron(element_vtk_cell, element_grid_points)

    # element surface
    surface_id_list = get_property(element_grid, 'surface_id', element_id)
    for i, each_surface_id in enumerate(surface_id_list):
        element_cell.surface_id[i] = int(each_surface_id)

    # cracked flag
    element_cracked_flag = get_property(element_grid, 'cracked', element_id)
    element_cell.cracked = int(*element_cracked_flag)

    # crack surface
    if element_cell.cracked == 9 or element_cell.cracked == 4:
        crack_surface_id = get_property(element_grid, 'crack_surface_id', element_id)
        crack_surface_id = int(*crack_surface_id)

        crack_surface_vtk_cell = crack_surface_grid.GetCell(crack_surface_id)
        crack_surface_vtk_cell = copy_vtk_cell(crack_surface_vtk_cell, crack_surface_grid.GetPoints())
        element_cell.crack_surface = crack_surface_vtk_cell

    return element_cell


class CrackElementCreator3D:
    @staticmethod
    def create_all_element(data_structure: DataStructure):
        element_cell_list = []
        # temp_vtk_model = vtkUnstructuredGrid()
        for each_element_id in range(Variable.element_number):
            temp_element_cell = create_an_element(data_structure, each_element_id)
            element_cell_list.append(temp_element_cell)

        return element_cell_list

    @staticmethod
    def create_all_surface(data_structure: DataStructure):
        surface_cell_list = []
        for each_surface_id in range(Variable.surface_number):
            temp_surface_cell = create_a_surface(data_structure, each_surface_id)
            surface_cell_list.append(temp_surface_cell)

        return surface_cell_list

    @staticmethod
    def build_element_surface_link(element_cell_list: List[Element3D], surface_cell_list: List[Surface3D]):
        for each_element_cell in element_cell_list:
            for i, each_surface_id in enumerate(each_element_cell.surface_id):
                if each_surface_id == -1:
                    continue
                each_element_cell.surface_cell_list[i] = surface_cell_list[each_surface_id]

        for each_surface_cell in surface_cell_list:
            for i, each_element_id in enumerate(each_surface_cell.element_id):
                if each_element_id == -1:
                    continue
                each_surface_cell.element_cell_list[i] = element_cell_list[each_element_id]


@deprecation.deprecated()
def generate_face_dictionary(element_id: int, vtk_cell: vtkCell, vtk_model: vtkUnstructuredGrid):
    face_dictionary = []
    for each_face in range(vtk_cell.GetNumberOfFaces()):

        temp_face: vtkPolygon = vtk_cell.GetFace(each_face)
        temp_id_list = temp_face.GetPointIds()

        adjacent_cell_id_list = vtkIdList()
        vtk_model.GetCellNeighbors(element_id, temp_id_list, adjacent_cell_id_list)

        if adjacent_cell_id_list.GetNumberOfIds() == 0:
            continue

        assert adjacent_cell_id_list.GetNumberOfIds() == 1

        adjacent_cell_id = adjacent_cell_id_list.GetId(0)
        adjacent_face_points = vtkPoints()
        adjacent_face_points.DeepCopy(temp_face.GetPoints())

        face_dictionary.append({'face_id': each_face, 'adjacent_cell_id': adjacent_cell_id, 'face_points': adjacent_face_points})
    return face_dictionary


