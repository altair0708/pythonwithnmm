from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCellArray, VTK_POLYGON, vtkUnstructuredGrid, VTK_LINE
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLUnstructuredGridWriter
import numpy as np


def subdivide_polygon_edges_to_lines(ugrid, max_length=1.0):
    new_points = vtkPoints()
    new_cells = vtkCellArray()
    point_map = {}  # 避免重复点
    point_id_lookup = {}  # 存储已经插入的点编号

    def insert_point(p):
        key = tuple(np.round(p, 6))
        if key in point_map:
            return point_map[key]
        pid = new_points.InsertNextPoint(p)
        point_map[key] = pid
        return pid

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

                pid0 = insert_point(pt0)
                pid1 = insert_point(pt1)

                line = vtkIdList()
                line.InsertNextId(pid0)
                line.InsertNextId(pid1)
                new_cells.InsertNextCell(line)

    # 构建新的 UnstructuredGrid，类型为线段
    output = vtkUnstructuredGrid()
    output.SetPoints(new_points)
    for i in range(new_cells.GetNumberOfCells()):
        id_list = vtkIdList()
        new_cells.GetNextCell(id_list)
        output.InsertNextCell(VTK_LINE, id_list)

    return output

# 示例：读取输入 UnstructuredGrid
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName("initial_crack.vtu")
reader.Update()
input_ugrid = reader.GetOutput()

# 执行边细分并生成轮廓线
output_lines = subdivide_polygon_edges_to_lines(input_ugrid, max_length=0.1)

# 保存输出（可视化时可用）
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName("re000_crack_tip.vtu")
writer.SetInputData(output_lines)
writer.Write()
