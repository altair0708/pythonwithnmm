from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkLine, VTK_LINE
from NMM.base.VTKBase.get_cell_point_id import get_cell_point_id
import numpy as np


def add_crack_point(vtk_model: vtkUnstructuredGrid, cell_id: int):
    if vtk_model.GetCellType(cell_id) != VTK_LINE:
        raise Exception('Request cell type: VTK_LINE')

    point_id = get_cell_point_id(vtk_model, cell_id)

    coordinate_0 = vtk_model.GetPoint(point_id[0])
    coordinate_1 = vtk_model.GetPoint(point_id[1])

    coordinate = (np.array(coordinate_0, dtype=np.float64) + np.array(coordinate_1, dtype=np.float64)) / 2

    # insert new crack point
    vtk_model.GetPoints().InsertNextPoint(coordinate)

    # new id of crack point
    new_id = vtk_model.GetNumberOfPoints()

    # new crack tip 0
    line_0 = vtkLine()
    line_0.GetPointIds().SetId(0, point_id[0])
    line_0.GetPointIds().SetId(1, new_id)
    vtk_model.InsertNextCell(line_0.GetCellType(), line_0.GetPointIds())

    # new crack tip 1
    line_1 = vtkLine()
    line_1.GetPointIds().SetId(0, new_id)
    line_1.GetPointIds().SetId(1, point_id[1])
    vtk_model.InsertNextCell(line_1.GetCellType(), line_1.GetPointIds())

    # delete old crack tip
    vtk_model.GetCellTypesArray().SetValue(cell_id, 0)
