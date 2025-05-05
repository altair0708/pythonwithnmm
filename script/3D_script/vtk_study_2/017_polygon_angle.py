from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolygon, vtkUnstructuredGrid
import numpy as np
import math

def create_triangle(points_list):
    points = vtkPoints()
    polygon = vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(3)

    for i, pt in enumerate(points_list):
        points.InsertNextPoint(pt)
        polygon.GetPointIds().SetId(i, i)
    polygon.Initialize(points.GetNumberOfPoints(), points)

    u_grid = vtkUnstructuredGrid()
    u_grid.SetPoints(points)
    u_grid.InsertNextCell(polygon.GetCellType(), polygon.GetPointIds())

    return u_grid


def get_polygon_normal(vtk_model: vtkUnstructuredGrid):
    assert vtk_model.GetNumberOfCells() == 1
    polygon = vtk_model.GetCell(0)
    normal = [0.0, 0.0, 0.0]
    vtkPolygon.ComputeNormal(polygon.GetPoints(), normal)
    return np.array(normal)


def compute_consistent_angle(poly1, poly2, shared_edge):
    """计算两个多边形之间的夹角（0-180°），确保法向量方向一致"""
    n1 = get_polygon_normal(poly1)
    n2 = get_polygon_normal(poly2)

    n1 = n1 / np.linalg.norm(n1)
    n2 = n2 / np.linalg.norm(n2)

    # 公共边方向
    e = np.array(shared_edge[1]) - np.array(shared_edge[0])
    e = e / np.linalg.norm(e)

    # 统一法向量朝向：如果 n2 与 n1 的方向夹角 > 90°，则翻转 n2
    if np.dot(np.cross(n1, n2), e) < 0:
        n2 = -n2

    dot = np.clip(np.dot(n1, n2), -1.0, 1.0)
    angle_rad = np.arccos(dot)
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def main():
    # 三角形1: 平面A
    p0 = (0, 0, 0)
    p1 = (1, 0, 0)
    p2 = (0.5, 1, 0)

    # 三角形2: 平面B，共享边为 p0-p1
    p3 = (0.5, 1, 1.7)

    triangle1 = create_triangle([p0, p1, p2])
    triangle2 = create_triangle([p1, p0, p3])  # 注意顺序反转以形成向外法向

    shared_edge = (p0, p1)

    angle = compute_consistent_angle(triangle1, triangle2, shared_edge)

    print(f"两个多边形之间的夹角（0-180°）为: {angle:.2f}°")

if __name__ == "__main__":
    main()
