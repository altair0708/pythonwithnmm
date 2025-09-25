from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkLine


def insert_a_line_with_point_id(target_grid: vtkUnstructuredGrid, id_0: int, id_1: int):

    line = vtkLine()
    line.GetPointIds().SetId(0, id_0)
    line.GetPointIds().SetId(1, id_1)

    # insert cell
    target_grid.InsertNextCell(line.GetCellType(), line.GetPointIds())
    target_grid.BuildLinks()
    target_grid.Modified()

    return target_grid.GetNumberOfCells()
