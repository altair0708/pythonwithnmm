from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex
from vtkmodules.vtkCommonCore import vtkIntArray
from NMM.base.VTKBase.new_a_grid import new_a_grid


def generate_point_grid(vtk_model: vtkUnstructuredGrid):
    target_grid = new_a_grid()
    target_grid.GetPoints().DeepCopy(vtk_model.GetPoints())

    array = vtkIntArray()
    array.SetName('cell_id')
    array.SetNumberOfComponents(1)

    for each_id in range(vtk_model.GetNumberOfPoints()):
        vertex = vtkVertex()
        vertex.GetPointIds().SetId(0, each_id)
        target_grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

        array.InsertNextTuple((each_id, ))

    target_grid.GetCellData().AddArray(array)

    return target_grid
