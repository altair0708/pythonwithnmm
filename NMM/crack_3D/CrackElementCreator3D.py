import deprecation
from typing import List
from NMM.GlobalVariable import DataStructure, Variable
from NMM.crack_3D.ElementBase3D import Element3D, create_an_element
from NMM.crack_3D.CrackSurfaceBase3D import CrackSurface3D, create_a_crack_surface
from NMM.crack_3D.SurfaceBase3D import Surface3D, create_a_surface
from NMM.crack_3D.CrackEdgeBase3D import CrackEdge3D, create_a_crack_edge
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList

# element
# surface
# crack surface
# edge


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
    def create_all_crack_surface(data_structure: DataStructure):
        crack_surface_cell_list = []
        for crack_surface_id in range(Variable.crack_surface_number):
            temp_crack_surface_cell = create_a_crack_surface(data_structure, crack_surface_id)
            crack_surface_cell_list.append(temp_crack_surface_cell)
        return crack_surface_cell_list

    @staticmethod
    def create_all_crack_edge(data_structure: DataStructure):
        crack_edge_cell_list = []
        for each_crack_edge_id in range(Variable.crack_edge_number):
            temp_crack_edge_cell = create_a_crack_edge(data_structure, each_crack_edge_id)
            crack_edge_cell_list.append(temp_crack_edge_cell)
        return crack_edge_cell_list

    @staticmethod
    def build_all_link(element_cell_list: List[Element3D],
                       surface_cell_list: List[Surface3D],
                       crack_surface_cell_list: List[CrackSurface3D],
                       crack_edge_cell_list: List[CrackEdge3D]):
        # element and surface
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

                if each_surface_cell.cracked > 1:
                    if each_surface_cell.element_cell_list[i].cracked == 0:
                        each_surface_cell.element_cell_list[i].cracked = 2

        # element and crack surface
        for each_element_cell in element_cell_list:
            for i, each_crack_surface_id in enumerate(each_element_cell.crack_surface_id):
                if each_crack_surface_id == -1:
                    continue
                each_element_cell.crack_surface_cell_list[i] = crack_surface_cell_list[each_crack_surface_id]
        for each_crack_surface_cell in crack_surface_cell_list:
            for i, each_element_id in enumerate(each_crack_surface_cell.element_id):
                if each_element_id == -1:
                    continue
                each_crack_surface_cell.element_cell_list[i] = element_cell_list[each_element_id]

        # surface and crack edge
        for each_surface_cell in surface_cell_list:
            for i, each_crack_edge_id in enumerate(each_surface_cell.crack_edge_id):
                if each_crack_edge_id == -1:
                    continue
                each_surface_cell.crack_edge_cell_list[i] = crack_edge_cell_list[each_crack_edge_id]
        for each_crack_edge_cell in crack_edge_cell_list:
            for i, each_surface_id in enumerate(each_crack_edge_cell.surface_id):
                if each_surface_id == -1:
                    continue
                each_crack_edge_cell.surface_cell_list[i] = surface_cell_list[each_surface_id]

        # crack surface and crack edge
        for each_crack_surface_cell in crack_surface_cell_list:
            for i, each_crack_edge_id in enumerate(each_crack_surface_cell.crack_edge_id):
                if each_crack_edge_id == -1:
                    continue
                each_crack_surface_cell.crack_edge_cell_list[i] = crack_edge_cell_list[each_crack_edge_id]
        for each_crack_edge_cell in crack_edge_cell_list:
            for i, each_crack_surface_id in enumerate(each_crack_edge_cell.crack_surface_id):
                if each_crack_surface_id == -1:
                    continue
                each_crack_edge_cell.crack_surface_cell_list[i] = crack_surface_cell_list[each_crack_surface_id]


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


