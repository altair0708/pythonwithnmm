from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex
from vtkmodules.vtkCommonCore import vtkIntArray, vtkIdList
from NMM.base.VTKBase.new_a_grid import new_a_grid
from NMM.base.CacheBase import relationship_cache


def generate_point_grid(vtk_model: vtkUnstructuredGrid):
    target_grid = new_a_grid()
    target_grid.GetPoints().DeepCopy(vtk_model.GetPoints())

    array = vtkIntArray()
    array.SetName('cell_id')
    array.SetNumberOfComponents(1)

    for each_point_id in range(vtk_model.GetNumberOfPoints()):
        vertex = vtkVertex()
        vertex.GetPointIds().SetId(0, each_point_id)
        target_grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

        array.InsertNextTuple((each_point_id, ))

        # add relationship cache of cover-element
        cell_id_list = vtkIdList()
        vtk_model.GetPointCells(each_point_id, cell_id_list)
        for each_id in range(cell_id_list.GetNumberOfIds()):
            each_cell_id = cell_id_list.GetId(each_id)
            relationship_cache.add_item('cover', each_point_id, 'element', each_cell_id)

    target_grid.GetCellData().AddArray(array)

    return target_grid
