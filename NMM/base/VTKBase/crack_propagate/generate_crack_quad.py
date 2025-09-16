from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkQuadraticQuad, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints
from typing import List
import numpy as np


def generate_crack_polygon(origin_list: List, vector_list: List):
    vector_0 = vector_list[0]
    vector_1 = vector_list[1]

    magnitude_0 = np.linalg.norm(vector_0)
    magnitude_1 = np.linalg.norm(vector_1)

    if magnitude_0 == 0 and magnitude_1 == 0:
        return None
    elif magnitude_0 == 0 and magnitude_1 != 0:
        point_0 = np.array(origin_list[0])
        point_1 = np.array(origin_list[1])
        point_2 = np.array(origin_list[1]) + np.array(vector_list[1])
        return generate_crack_triangle(point_0, point_1, point_2)
    elif magnitude_0 != 0 and magnitude_1 == 0:
        point_0 = np.array(origin_list[0])
        point_1 = np.array(origin_list[1])
        point_2 = np.array(origin_list[0]) + np.array(vector_list[0])
        return generate_crack_triangle(point_0, point_1, point_2)
    elif magnitude_0 != 0 and magnitude_1 != 0:
        return generate_crack_quad(origin_list, vector_list)


def generate_crack_triangle(p0, p1, p2):

    points = vtkPoints()
    points.InsertNextPoint(p0)
    points.InsertNextPoint(p1)
    points.InsertNextPoint(p2)

    polygon = vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(3)
    polygon.GetPointIds().SetId(0, 0)
    polygon.GetPointIds().SetId(1, 1)
    polygon.GetPointIds().SetId(2, 2)

    u_grid = vtkUnstructuredGrid()
    u_grid.SetPoints(points)
    u_grid.InsertNextCell(polygon.GetCellType(), polygon.GetPointIds())

    return u_grid


def generate_crack_quad(origin_list: List, vector_list: List):
    # 四个顶点：两个原始点与两个新点
    new_p0 = np.array(origin_list[0]) + np.array(vector_list[0])
    new_p1 = np.array(origin_list[1]) + np.array(vector_list[1])

    points = vtkPoints()

    for pt in [origin_list[0], origin_list[1], new_p1.tolist(), new_p0.tolist()]:
        pid = points.InsertNextPoint(pt)

    # 计算边中点
    for i in range(4):
        p_start = np.array(points.GetPoint(i))
        p_end = np.array(points.GetPoint((i + 1) % 4))
        midpoint = (p_start + p_end) / 2.0
        points.InsertNextPoint(midpoint.tolist())

    # 创建 vtkQuadraticQuad（共8个点：4个角点 + 4个边中点）
    quad = vtkQuadraticQuad()
    for i in range(4):
        quad.GetPointIds().SetId(i, i)
    for i in range(4):
        quad.GetPointIds().SetId(i + 4, i + 4)  # 边中点依次是点4~7

    # 构建网格
    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    return ugrid
