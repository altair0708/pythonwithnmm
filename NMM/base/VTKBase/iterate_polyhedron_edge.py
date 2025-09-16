from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkLine, VTK_POLYHEDRON, vtkCellArray


def iterate_polyhedron_edges(input_ugrid):
    """
    从一个包含单个 vtkPolyhedron 的 vtkUnstructuredGrid 中迭代输出所有棱，
    每次返回一个只包含一条 vtkLine 的 vtkUnstructuredGrid。

    不使用 GetFaces，而是使用 Triangulate 方法获取边信息。

    Parameters:
        input_ugrid (vtkUnstructuredGrid): 包含一个 vtkPolyhedron 单元

    Yields:
        vtkUnstructuredGrid: 每次一个只包含一条 vtkLine 的网格
    """
    if input_ugrid.GetNumberOfCells() != 1:
        raise ValueError("输入必须包含一个 vtkPolyhedron 单元")

    polyhedron = input_ugrid.GetCell(0)
    if polyhedron.GetCellType() != VTK_POLYHEDRON:
        raise ValueError("该单元不是 vtkPolyhedron 类型")

    points = input_ugrid.GetPoints()
    edge_set = set()

    for face_id in range(polyhedron.GetNumberOfFaces()):
        face = polyhedron.GetFace(face_id)  # vtkPolygon 或其他多边形
        n_edges = face.GetNumberOfEdges()
        for j in range(n_edges):
            edge = face.GetEdge(j)  # vtkLine
            id0 = edge.GetPointId(0)
            id1 = edge.GetPointId(1)
            a, b = sorted((id0, id1))
            edge_set.add((a, b))  # 去重

    # 逐条输出棱
    for a, b in edge_set:
        p0 = points.GetPoint(a)
        p1 = points.GetPoint(b)

        pts = vtkPoints()
        pts.InsertNextPoint(p0)
        pts.InsertNextPoint(p1)

        line = vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)

        ugrid = vtkUnstructuredGrid()
        ugrid.SetPoints(pts)
        ugrid.InsertNextCell(line.GetCellType(), line.GetPointIds())

        yield ugrid


if __name__ == '__main__':
    from NMM.base.VTKBase.test_example import generate_tetra_polyhedron

    _, _, _, polyhedron_ugrid = generate_tetra_polyhedron()

    for i, edge_grid in enumerate(iterate_polyhedron_edges(polyhedron_ugrid)):
        print(f"第 {i} 条棱，点数量: {edge_grid.GetNumberOfPoints()}")
        p0 = edge_grid.GetPoint(0)
        p1 = edge_grid.GetPoint(1)
        print(f"  点0: {p0}, 点1: {p1}")

