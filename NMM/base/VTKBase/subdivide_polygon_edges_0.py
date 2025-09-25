from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCellArray, VTK_POLYGON, vtkUnstructuredGrid, VTK_LINE
from NMM.base.VTKBase.generate_line import generate_line
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell import insert_a_vtk_cell
from NMM.base.VTKBase.new_a_grid import new_a_grid
import numpy as np


def subdivide_polygon_edges_to_lines(ugrid, max_length=0.1):
    result = new_a_grid(allow_duplicate=False)

    for i in range(ugrid.GetNumberOfCells()):
        cell = ugrid.GetCell(i)
        if cell.GetCellType() != VTK_POLYGON:
            continue

        n_pts = cell.GetNumberOfPoints()
        orig_ids = [cell.GetPointId(j) for j in range(n_pts)]

        for j in range(n_pts):
            id1 = orig_ids[j]
            id2 = orig_ids[(j + 1) % n_pts]

            p1 = np.array(ugrid.GetPoint(id1))
            p2 = np.array(ugrid.GetPoint(id2))

            edge = p2 - p1
            length = np.linalg.norm(edge)
            n_segments = max(int(np.ceil(length / max_length)), 1)

            for k in range(n_segments):
                t0 = k / n_segments
                t1 = (k + 1) / n_segments
                pt0 = (1 - t0) * p1 + t0 * p2
                pt1 = (1 - t1) * p1 + t1 * p2

                temp_line = generate_line(pt0, pt1)
                insert_a_vtk_cell(temp_line, result)

    return result
