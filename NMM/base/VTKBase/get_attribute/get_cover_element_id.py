from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkIdList


def get_cover_element_relationship(vtk_model: vtkUnstructuredGrid, element_id: int):
    id_list = vtkIdList()
    vtk_model.GetCellPoints(element_id, id_list)

    relationship_list = []
    for each_id in range(id_list.GetNumberOfIds()):
        relationship_list.append({'cover': id_list.GetId(each_id), 'element': element_id})

    return relationship_list
