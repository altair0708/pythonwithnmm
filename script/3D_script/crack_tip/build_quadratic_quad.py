from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkQuadraticQuad
from vtkmodules.vtkCommonCore import vtkPoints

def build_quadratic_quad_grid_from_moved_polygon(original_points, moved_points):
    """
    original_points: List of (x, y, z) tuples for the original polygon
    moved_points: List of (x, y, z) tuples for the moved polygon
    Returns: vtkUnstructuredGrid containing vtkQuadraticQuad cells
    """
    n = original_points.GetNumberOfPoints()
    all_points = vtkPoints()
    all_points.SetDataTypeToDouble()

    quad_grid = vtkUnstructuredGrid()

    for i in range(n):
        # 顶点编号
        i0 = i
        i1 = (i + 1) % n

        # 四边形角点（原边 + 移动后边）
        p0 = original_points[i0]
        p1 = original_points[i1]
        p2 = moved_points[i1]
        p3 = moved_points[i0]

        # 插入角点（共4个）
        id0 = all_points.InsertNextPoint(p0)
        id1 = all_points.InsertNextPoint(p1)
        id2 = all_points.InsertNextPoint(p2)
        id3 = all_points.InsertNextPoint(p3)

        # 计算4个边的中点
        def midpoint(a, b):
            return [(a[j] + b[j]) / 2.0 for j in range(3)]

        m01 = midpoint(p0, p1)
        m12 = midpoint(p1, p2)
        m23 = midpoint(p2, p3)
        m30 = midpoint(p3, p0)

        id4 = all_points.InsertNextPoint(m01)
        id5 = all_points.InsertNextPoint(m12)
        id6 = all_points.InsertNextPoint(m23)
        id7 = all_points.InsertNextPoint(m30)

        # 创建 vtkQuadraticQuad 单元
        quad = vtkQuadraticQuad()
        ids = [id0, id1, id2, id3, id4, id5, id6, id7]
        for j, pid in enumerate(ids):
            quad.GetPointIds().SetId(j, pid)

        # 插入单元
        quad_grid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    quad_grid.SetPoints(all_points)
    return quad_grid
