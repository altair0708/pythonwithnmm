from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkQuadraticQuad, vtkPolyLine
import numpy as np
from NMM.base.VTKBase import write_file


def move_contour_and_generate_quadratic_quads(unstructured_grid, displacement_vectors):
    points = unstructured_grid.GetPoints()
    num_points = points.GetNumberOfPoints()
    assert num_points == len(displacement_vectors), "向量数量必须与多边形顶点数一致"

    # 原始与前进后的点坐标
    original_points = np.array([points.GetPoint(i) for i in range(num_points)])
    displacements = np.array(displacement_vectors)
    moved_points = original_points + displacements

    # 创建新轮廓 polyline（前进后）
    new_polyline_points = vtkPoints()
    for pt in moved_points:
        new_polyline_points.InsertNextPoint(pt)

    polyline = vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(num_points + 1)  # 末尾闭合
    for i in range(num_points):
        polyline.GetPointIds().SetId(i, i)
    polyline.GetPointIds().SetId(num_points, 0)  # 闭合，尾点回到0

    polyline_grid = vtkUnstructuredGrid()
    polyline_grid.SetPoints(new_polyline_points)
    polyline_grid.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())

    # 创建 quadratic quads
    quad_grid = vtkUnstructuredGrid()
    quad_points = vtkPoints()
    point_id_map = {}

    # 插入所有顶点（原始 + 变形）
    for i in range(num_points):
        pid = quad_points.InsertNextPoint(original_points[i])
        point_id_map[f"o{i}"] = pid
    for i in range(num_points):
        pid = quad_points.InsertNextPoint(moved_points[i])
        point_id_map[f"m{i}"] = pid

    # 插入每个四边形对应的10个点
    for i in range(num_points):
        i0 = i
        i1 = (i + 1) % num_points

        o0 = original_points[i0]
        o1 = original_points[i1]
        m0 = moved_points[i0]
        m1 = moved_points[i1]

        # 四个角点
        pid0 = point_id_map[f"o{i0}"]
        pid1 = point_id_map[f"o{i1}"]
        pid2 = point_id_map[f"m{i1}"]
        pid3 = point_id_map[f"m{i0}"]

        # 四个边中点（用坐标平均）
        mid01 = (o0 + o1) / 2
        mid12 = (o1 + m1) / 2
        mid23 = (m1 + m0) / 2
        mid30 = (m0 + o0) / 2

        mid_ids = []
        for mid in [mid01, mid12, mid23, mid30]:
            mid_ids.append(quad_points.InsertNextPoint(mid))

        # 构造 vtkQuadraticQuad
        quad = vtkQuadraticQuad()
        for j, pid in enumerate([pid0, pid1, pid2, pid3] + mid_ids):
            quad.GetPointIds().SetId(j, pid)

        quad_grid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    quad_grid.SetPoints(quad_points)

    return polyline_grid, quad_grid

# 示例：正方形轮廓
def create_sample_square():
    points = vtkPoints()
    coords = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    for x, y, z in coords:
        points.InsertNextPoint(x, y, z)

    polyline = vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(coords) + 1)

    for i in range(len(coords) + 1):
        polyline.GetPointIds().SetId(i, i % len(coords))

    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    grid.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())
    return grid


if __name__ == "__main__":
    input_grid = create_sample_square()
    displacement_vectors = [(-0.1, -0.1, -0.1),
                            (0.1, -0.1, 0.1),
                            (0.1, 0.1, -0.1),
                            (-0.1, 0.1, 0.1)]
    write_file(input_grid, 're003_input_grid.vtu')
    polyline_result, quad_result = move_contour_and_generate_quadratic_quads(input_grid, displacement_vectors)
    write_file(polyline_result, 're003_polyline_result.vtu')
    write_file(quad_result, 're003_quad_result.vtu')
