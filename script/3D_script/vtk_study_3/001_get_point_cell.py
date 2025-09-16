from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.base.VTKBase.write_file import write_file
from NMM.base.VTKBase.load_a_grid import load_a_grid


def extract_cells_containing_point(unstructured_grid, point_id):
    """
    提取包含给定点ID的所有cell，并构建一个新的vtkUnstructuredGrid返回。
    """
    cell_ids = vtkIdList()
    unstructured_grid.GetPointCells(point_id, cell_ids)

    new_grid = vtkUnstructuredGrid()
    points = vtkPoints()
    point_map = {}

    for i in range(cell_ids.GetNumberOfIds()):
        cell_id = cell_ids.GetId(i)
        cell = unstructured_grid.GetCell(cell_id)
        point_ids = cell.GetPointIds()

        new_cell_point_ids = vtkIdList()
        for j in range(point_ids.GetNumberOfIds()):
            pid = point_ids.GetId(j)
            if pid not in point_map:
                coord = unstructured_grid.GetPoint(pid)
                new_pid = points.InsertNextPoint(coord)
                point_map[pid] = new_pid
            new_cell_point_ids.InsertNextId(point_map[pid])

        new_grid.InsertNextCell(cell.GetCellType(), new_cell_point_ids)

    new_grid.SetPoints(points)
    return new_grid


if __name__ == "__main__":
    vtk_grid = load_a_grid('crack_tip.vtu')
    edge_grid = extract_cells_containing_point(vtk_grid, 9)
    write_file(edge_grid, 're001_edge_grid.vtu')

