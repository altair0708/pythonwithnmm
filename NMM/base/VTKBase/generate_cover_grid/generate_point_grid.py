from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex
from NMM.base.VTKBase.new_a_grid import new_a_grid


def generate_point_grid(vtk_model: vtkUnstructuredGrid):
    target_grid = new_a_grid()
    pointNumber = vtk_model.GetNumberOfPoints()

    for each_id in range(pointNumber):
        vertex = vtkVertex()
        vertex.GetPointIds().SetId(0, each_id)
        target_grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

    target_grid.SetPoints(vtk_model.GetPoints())

    return target_grid
