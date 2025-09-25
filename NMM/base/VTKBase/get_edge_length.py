from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_LINE
from NMM.base.VTKBase.get_cell_point_id import get_cell_point_id
import numpy as np


def get_edge_length(vtk_model: vtkUnstructuredGrid, cell_id: int):

    if vtk_model.GetCellType(cell_id) != VTK_LINE:
        raise Exception('Request cell type: VTK_LINE')

    point_id = get_cell_point_id(vtk_model, cell_id)

    coordinate_0 = vtk_model.GetPoint(point_id[0])
    coordinate_1 = vtk_model.GetPoint(point_id[1])

    length = np.linalg.norm(np.array(coordinate_0, dtype=np.float64) - np.array(coordinate_1, dtype=np.float64))

    return length

