from NMM.GlobalVariable import DataStructure, Variable
from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from NMM.base.PropertyGetSetFunction import get_property
from NMM.base.CopyFunction import copy_polyhedron
from NMM.base.ModifyVtkCell import insert_a_cell
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron
from vtkmodules.vtkCommonCore import vtkPoints


def create_an_element(data_structure: DataStructure, element_id: int):
    temp_element = CrackedElement3D(id_value=element_id)
    temp_vtk_element: vtkUnstructuredGrid = data_structure.manifold_element.content

    # strain_total
    temp_element.strain_total = get_property(temp_vtk_element, 'strain_total', element_id)

    # vtk_cell
    vtk_cell = temp_vtk_element.GetCell(element_id)
    temp_u_grid: vtkUnstructuredGrid = data_structure.manifold_element.content
    temp_point_list: vtkPoints = temp_u_grid.GetPoints()
    temp_element.vtk_cell = copy_polyhedron(vtk_cell, temp_point_list)

    # cracked flag
    temp_cracked = get_property(temp_vtk_element, 'cracked', element_id)
    temp_cracked = int(*temp_cracked)
    temp_element.crack_new = False
    if temp_cracked == 0:
        temp_element.cracked = False
    elif temp_cracked == 1:
        temp_element.cracked = True
    else:
        raise Exception('cracked value error:{}!!!'.format(temp_cracked))
    return temp_element


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


