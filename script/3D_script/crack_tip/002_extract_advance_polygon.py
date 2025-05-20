from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyLine, vtkQuad
from vtkmodules.vtkFiltersModeling import vtkLinearSubdivisionFilter
from NMM.base.VTKBase import write_file
from build_quadratic_quad import build_quadratic_quad_grid_from_moved_polygon


def move_edge_contour_and_generate_quads(unstructured_grid, displacement_vectors):
    """
    将多边形轮廓的每个顶点沿向量偏移，并返回：
    - 移动后的轮廓线 (vtkUnstructuredGrid)
    - 由每条边构成的四边形面 (vtkUnstructuredGrid)
    """
    original_points = unstructured_grid.GetPoints()
    num_points = original_points.GetNumberOfPoints()

    if len(displacement_vectors) != num_points:
        raise ValueError("位移向量数量必须等于点数")

    # 创建新点（移动后的轮廓点）
    new_points = vtkPoints()
    new_points.SetDataTypeToDouble()
    for i in range(num_points):
        x, y, z = original_points.GetPoint(i)
        dx, dy, dz = displacement_vectors[i]
        new_points.InsertNextPoint(x + dx, y + dy, z + dz)

    # 生成移动后的轮廓线
    polyline = vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(num_points + 1)
    for i in range(num_points):
        polyline.GetPointIds().SetId(i, i)
    polyline.GetPointIds().SetId(num_points, 0)

    moved_grid = vtkUnstructuredGrid()
    moved_grid.SetPoints(new_points)
    moved_grid.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())

    # 合并原始点 + 新点用于构建四边形
    all_points = vtkPoints()
    all_points.SetDataTypeToDouble()
    for i in range(num_points):
        all_points.InsertNextPoint(original_points.GetPoint(i))  # 原始点
    for i in range(num_points):
        all_points.InsertNextPoint(new_points.GetPoint(i))       # 新点

    # 构建四边形面
    quad_grid = vtkUnstructuredGrid()
    quad_grid.SetPoints(all_points)

    for i in range(num_points):
        p0 = i
        p1 = (i + 1) % num_points
        q1 = p1 + num_points
        q0 = i + num_points

        quad = vtkQuad()
        quad.GetPointIds().SetId(0, p0)
        quad.GetPointIds().SetId(1, p1)
        quad.GetPointIds().SetId(2, q1)
        quad.GetPointIds().SetId(3, q0)

        quad_grid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    def smooth_non_planar_quads(quad_grid, subdivisions=2):
        subdivider = vtkLinearSubdivisionFilter()
        subdivider.SetInputData(quad_grid)
        subdivider.SetNumberOfSubdivisions(subdivisions)
        subdivider.Update()
        return subdivider.GetOutput()

    smooth_non_planar_quads(quad_grid)

    return moved_grid, quad_grid

# 示例：构造初始轮廓
def create_example_edge_contour():
    points = vtkPoints()
    points.SetDataTypeToDouble()
    coords = [
        (0, 0, 0),
        (1, 0, 0),
        (1, 1, 0),
        (0, 1, 0),
    ]
    for pt in coords:
        points.InsertNextPoint(*pt)

    polyline = vtkPolyLine()
    n = len(coords)
    polyline.GetPointIds().SetNumberOfIds(n + 1)
    for i in range(n):
        polyline.GetPointIds().SetId(i, i)
    polyline.GetPointIds().SetId(n, 0)

    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())

    return ugrid


# 运行示例
if __name__ == "__main__":
    original_grid = create_example_edge_contour()
    write_file(original_grid, 're002_origin_grid.vtu')
    displacement_vectors = [
        (-0.1, -0.1, -0.1),
        (0.1, -0.1, -0.1),
        (0.1, 0.1, 0.1),
        (-0.1, 0.1, 0.1)
    ]

    moved_grid, quad_grid = move_edge_contour_and_generate_quads(original_grid, displacement_vectors)
    quadratic_quad_grid = build_quadratic_quad_grid_from_moved_polygon(original_grid, moved_grid)
    write_file(moved_grid, 're002_moved_grid_01.vtu')
    write_file(quadratic_quad_grid, 're002_quad_grid_01.vtu')

    # 输出验证
    print("新轮廓顶点：")
    for i in range(moved_grid.GetNumberOfPoints()):
        print(f"Moved Point {i}: {moved_grid.GetPoint(i)}")

    print("\n四边形面总数：", quad_grid.GetNumberOfCells())
