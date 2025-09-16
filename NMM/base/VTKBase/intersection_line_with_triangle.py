from vtkmodules.vtkCommonDataModel import vtkTriangle, vtkLine, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import reference, vtkPoints


def intersect_line_with_triangle(line_ugrid, triangle_ugrid):
    """
    判断一个 vtkLine 是否与一个 vtkTriangle 相交，并返回交点（如有）。

    Parameters:
        line_ugrid (vtkUnstructuredGrid): 只包含一个 vtkLine
        triangle_ugrid (vtkUnstructuredGrid): 只包含一个 vtkTriangle

    Returns:
        tuple or None: 若相交，返回交点坐标 (x, y, z)，否则返回 None。
    """
    if line_ugrid.GetNumberOfCells() != 1 or triangle_ugrid.GetNumberOfCells() != 1:
        raise ValueError("两个输入网格必须各包含一个单元（vtkLine 和 vtkTriangle）")

    # 获取直线端点
    line = line_ugrid.GetCell(0)
    p0 = line_ugrid.GetPoint(line.GetPointId(0))
    p1 = line_ugrid.GetPoint(line.GetPointId(1))

    # 获取三角形顶点
    triangle = triangle_ugrid.GetCell(0)
    a = triangle_ugrid.GetPoint(triangle.GetPointId(0))
    b = triangle_ugrid.GetPoint(triangle.GetPointId(1))
    c = triangle_ugrid.GetPoint(triangle.GetPointId(2))

    # 构造 vtkTriangle
    tri = vtkTriangle()
    tri.GetPoints().SetPoint(0, a)
    tri.GetPoints().SetPoint(1, b)
    tri.GetPoints().SetPoint(2, c)

    # 相交检测
    tol = 1e-5
    t = reference(0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    subid = reference(0)

    if tri.IntersectWithLine(p0, p1, tol, t, x, pcoords, subid):
        return tuple(x)
    else:
        return None


if __name__ == '__main__':
    # 构建一个 vtkLine
    line_points = vtkPoints()
    line_points.InsertNextPoint(0, 0, -1)
    line_points.InsertNextPoint(0, 0, 1)

    line = vtkLine()
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 1)

    line_ugrid = vtkUnstructuredGrid()
    line_ugrid.SetPoints(line_points)
    line_ugrid.InsertNextCell(line.GetCellType(), line.GetPointIds())

    # 构建一个 vtkTriangle
    tri_points = vtkPoints()
    tri_points.InsertNextPoint(0.1, 0.1, 0)
    tri_points.InsertNextPoint(0, 1, 0)
    tri_points.InsertNextPoint(1, 0, 0)

    triangle = vtkTriangle()
    for i in range(3):
        triangle.GetPointIds().SetId(i, i)

    tri_ugrid = vtkUnstructuredGrid()
    tri_ugrid.SetPoints(tri_points)
    tri_ugrid.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())

    # 调用函数
    intersection = intersect_line_with_triangle(line_ugrid, tri_ugrid)
    if intersection:
        print("交点:", intersection)
    else:
        print("无交点")

