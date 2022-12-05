from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.base.PropertyGetSetFunction import get_property, set_property
from vtkmodules.vtkCommonDataModel import vtkTetra, vtkUnstructuredGrid, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIntArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from collections import Counter


def generate_element_surface(manifold_element_file: str, output_path: str):

    vtk_element_model: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(output_path+manifold_element_file)
    surface_id = vtkIntArray()
    surface_id.SetName('element_surface_id')
    surface_id.SetNumberOfComponents(4)
    vtk_element_model.GetCellData().AddArray(surface_id)

    vtk_surface_model = vtkUnstructuredGrid()
    element_id = vtkIntArray()
    element_id.SetName('element_id')
    element_id.SetNumberOfComponents(2)
    vtk_surface_model.GetCellData().AddArray(element_id)

    points = vtkPoints()
    points.DeepCopy(vtk_element_model.GetPoints())
    vtk_surface_model.SetPoints(points)

    element_number = vtk_element_model.GetNumberOfCells()
    element_set = set()
    element_list = []

    each_surface_id = 0
    # check_list = []
    for each_element_id in range(element_number):
        temp_element: vtkCell = vtk_element_model.GetCell(each_element_id)
        surface_id_list = []
        for each_id in range(temp_element.GetNumberOfFaces()):
            temp_surface = temp_element.GetFace(each_id)
            temp_id_list = temp_surface.GetPointIds()

            temp_set = []
            for each_point_id in range(temp_id_list.GetNumberOfIds()):
                temp_set.append(temp_id_list.GetId(each_point_id))
                temp_set.sort()
            temp_set = tuple(temp_set)

            if temp_set in element_set:
                temp_surface_id = element_list.index(temp_set)
                surface_id_list.append(temp_surface_id)

                other_element = get_property(vtk_surface_model, 'element_id', temp_surface_id)[0]
                temp_element_tuple = (other_element, each_element_id)
                set_property(vtk_surface_model, 'element_id', temp_surface_id, temp_element_tuple)

                # debug counter
                # check_list.append(check_id)
            else:
                element_set.add(temp_set)
                element_list.append(temp_set)
                surface_id_list.append(each_surface_id)

                temp_surface = vtkPolygon()
                temp_surface.GetPointIds().SetNumberOfIds(len(temp_set))
                for i, each_point_id in enumerate(temp_set):
                    temp_surface.GetPointIds().SetId(i, each_point_id)
                vtk_surface_model.InsertNextCell(temp_surface.GetCellType(), temp_surface.GetPointIds())
                set_property(vtk_surface_model, 'element_id', each_surface_id, (each_element_id, -1))

                each_surface_id += 1
        surface_id.InsertTuple(each_element_id, surface_id_list)
    # check_counter = Counter(check_list)
    # print(check_counter.most_common())

    writer = vtkXMLUnstructuredGridWriter()
    writer.SetInputData(vtk_element_model)
    writer.SetFileName(output_path + 'manifold_element.vtu')
    writer.Write()

    writer = vtkXMLUnstructuredGridWriter()
    writer.SetInputData(vtk_surface_model)
    writer.SetFileName(output_path + 'element_surface.vtu')
    writer.Write()
