from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyLine, vtkUnstructuredGrid
from NMM.base.VTKBase import write_file

def move_edge_contour(unstructured_grid, displacement_vectors):
    """
    将一个由 edge 构成的多边形轮廓中的每个顶点依照向量偏移，返回新的 edge 构成的轮廓。

    Parameters:
        unstructured_grid (vtkUnstructuredGrid): 输入的轮廓网格，含一个闭合 polyline（edge）
        displacement_vectors (list of list or np.ndarray): 位移向量，每个点一个

    Returns:
        vtkUnstructuredGrid: 新的轮廓（由 vtkPolyLine 表示），作为 unstructured grid 返回
    """
    original_points = unstructured_grid.GetPoints()
    num_points = original_points.GetNumberOfPoints()

    if len(displacement_vectors) != num_points:
        raise ValueError("位移向量数量必须等于顶点数量")

    # 创建新的点集
    new_points = vtkPoints()
    new_points.SetDataTypeToDouble()
    for i in range(num_points):
        x, y, z = original_points.GetPoint(i)
        dx, dy, dz = displacement_vectors[i]
        new_points.InsertNextPoint(x + dx, y + dy, z + dz)

    # 创建闭合的 polyline（线性轮廓）
    polyline = vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(num_points + 1)  # 加1闭合

    for i in range(num_points):
        polyline.GetPointIds().SetId(i, i)
    polyline.GetPointIds().SetId(num_points, 0)  # 闭合：最后一个点指向第一个点

    # 构建新网格
    new_grid = vtkUnstructuredGrid()
    new_grid.SetPoints(new_points)
    new_grid.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())

    return new_grid


# 测试函数
def create_example_edge_contour():
    """
    构造一个闭合五边形轮廓（仅边，不填充）
    """
    points = vtkPoints()
    points.SetDataTypeToDouble()
    coords = [
        (0, 0, 0),
        (1, 0, 0),
        (1.5, 1, 0),
        (0.5, 2, 0),
        (-0.5, 1, 0)
    ]
    for pt in coords:
        points.InsertNextPoint(*pt)

    polyline = vtkPolyLine()
    n = len(coords)
    polyline.GetPointIds().SetNumberOfIds(n + 1)
    for i in range(n):
        polyline.GetPointIds().SetId(i, i)
    polyline.GetPointIds().SetId(n, 0)  # 闭合边

    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())

    return ugrid


# 示例执行
if __name__ == "__main__":
    # 创建原始轮廓
    edge_grid = create_example_edge_contour()
    write_file(edge_grid, 're001_origin_grid.vtu')

    # 位移向量
    displacement_vectors = [
        (0.1, 0.0, 0.0),
        (0.1, 0.0, 0.0),
        (0.0, 0.1, 0.0),
        (-0.1, 0.0, 0.0),
        (-0.1, 0.0, 0.0),
    ]

    new_edge_grid = move_edge_contour(edge_grid, displacement_vectors)
    write_file(new_edge_grid, 're001_result.vtu')

    # 输出验证
    print("新轮廓顶点：")
    for i in range(new_edge_grid.GetNumberOfPoints()):
        print(f"Point {i}: {new_edge_grid.GetPoint(i)}")
