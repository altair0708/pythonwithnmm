from NMM.GlobalVariable import DataStructure, Variable
from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_polyhedron
from NMM.base.ModifyVtkCell import insert_a_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


def create_an_element(data_structure: DataStructure, element_id: int):
    temp_element = CrackedElement3D(id_value=element_id)
    temp_vtk_element: vtkUnstructuredGrid = data_structure.manifold_element.content

    # strain_total
    temp_element.strain_total = get_property(temp_vtk_element, 'strain_total', element_id)

    # vtk_cell
    vtk_cell: vtkCell = temp_vtk_element.GetCell(element_id)
    temp_u_grid: vtkUnstructuredGrid = data_structure.manifold_element.content
    temp_point_list: vtkPoints = temp_u_grid.GetPoints()
    temp_element.vtk_cell = copy_polyhedron(vtk_cell, temp_point_list)
    temp_element.adjacent_element = generate_face_dictionary(element_id, vtk_cell, temp_vtk_element)

    # cracked flag
    temp_cracked = get_property(temp_vtk_element, 'cracked', element_id)
    temp_element.cracked = int(*temp_cracked)
    if temp_element.cracked == 2 or temp_element.cracked == 1:
        temp_crack_point_1 = get_property(temp_vtk_element, 'crack_point_1', element_id)
        temp_crack_point_2 = get_property(temp_vtk_element, 'crack_point_2', element_id)
        temp_element.crack_edge.append(temp_crack_point_1)
        temp_element.crack_edge.append(temp_crack_point_2)
    return temp_element


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


class CrackElementCreator3D:
    @staticmethod
    def create_all_element(data_structure: DataStructure):
        temp_element_list = []
        temp_vtk_model = vtkUnstructuredGrid()
        for each_element_id in range(Variable.element_number):
            temp_element = create_an_element(data_structure, each_element_id)
            temp_element_list.append(temp_element)

            insert_a_cell(temp_vtk_model, temp_element.vtk_cell)

        # writer = vtkXMLUnstructuredGridWriter()
        # writer.SetInputData(temp_vtk_model)
        # writer.SetFileName('log.vtu')
        # writer.Write()

        return temp_element_list


