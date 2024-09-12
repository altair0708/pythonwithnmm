from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolygon
from vtkmodules.vtkCommonCore import vtkIdList, vtkIntArray, vtkPoints
from NMM.base.CacheBase import relationship_cache


def generate_element_surface(vtk_model: vtkUnstructuredGrid):

    # element_surface.vtu
    vtk_surface_model = vtkUnstructuredGrid()
    points = vtkPoints()
    points.DeepCopy(vtk_model.GetPoints())
    vtk_surface_model.SetPoints(points)

    array = vtkIntArray()
    array.SetName('cell_id')
    array.SetNumberOfComponents(1)

    element_number = vtk_model.GetNumberOfCells()
    surface_point_list = []

    for each_element_id in range(element_number):
        temp_element: vtkCell = vtk_model.GetCell(each_element_id)
        for each_id in range(temp_element.GetNumberOfFaces()):
            temp_surface = temp_element.GetFace(each_id)
            temp_id_list: vtkIdList = temp_surface.GetPointIds()

            temp_point_set = set()
            for each_point_id in range(temp_id_list.GetNumberOfIds()):
                temp_point_set.add(temp_id_list.GetId(each_point_id))

            if temp_point_set in surface_point_list:
                temp_surface_id = surface_point_list.index(temp_point_set)

            else:
                temp_surface_id = len(surface_point_list)
                surface_point_list.append(temp_point_set)
                array.InsertNextTuple((temp_surface_id, ))

                temp_surface = vtkPolygon()
                temp_surface.GetPointIds().SetNumberOfIds(len(temp_point_set))
                for i, each_point_id in enumerate(temp_point_set):
                    temp_surface.GetPointIds().SetId(i, each_point_id)
                vtk_surface_model.InsertNextCell(temp_surface.GetCellType(), temp_surface.GetPointIds())

            relationship_cache.add_item('element', each_element_id, 'surface', temp_surface_id)

    vtk_surface_model.GetCellData().AddArray(array)

    return vtk_surface_model
