from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolygon, vtkUnstructuredGrid
import numpy as np
import math

TOLERANCE = 0.000001

def rounded_key(p):
    return tuple(round(coord / TOLERANCE) for coord in p)

def are_points_close(p1, p2, tol=TOLERANCE):
    return math.dist(p1, p2) < tol

def normalize_edge_for_compare(p1, p2):
    return tuple([rounded_key(p1), rounded_key(p2)])


def get_edges_with_original_coords(polygon: vtkPolygon, reverse=False):
    points = polygon.GetPoints()
    n = points.GetNumberOfPoints()

    edge_dict = {}
    edge_list = []

    for i in range(n):
        if reverse is True:
            p1 = points.GetPoint((n - 1) - i)
            p2 = points.GetPoint((n - 1) - (i + 1) % n)
        else:
            p1 = points.GetPoint(i)
            p2 = points.GetPoint((i + 1) % n)

        key = normalize_edge_for_compare(p1, p2)
        edge_dict[key] = (p1, p2)  # 保存原始边坐标
        edge_list.append((p1, p2))
    return edge_dict, edge_list


def get_vector(points):
    return np.array(points[0]) - np.array(points[1])


def calculate_polygon_angle(vtk_model_0: vtkUnstructuredGrid, vtk_model_1: vtkUnstructuredGrid):

    poly_0: vtkPolygon = vtk_model_0.GetCell(0)
    poly_1: vtkPolygon = vtk_model_1.GetCell(0)

    edges0, edges_list_0 = get_edges_with_original_coords(poly_0)
    edges1, edges_list_1 = get_edges_with_original_coords(poly_1)

    shared_keys = set(edges0.keys()) & set(edges1.keys())
    shared_edge = [edges0[k] for k in shared_keys]

    if len(shared_edge) == 0:
        edges0, edges_list_0 = get_edges_with_original_coords(poly_0, reverse=True)

        shared_keys = set(edges0.keys()) & set(edges1.keys())
        shared_edge = [edges0[k] for k in shared_keys]

    assert len(shared_edge) == 1

    vector_0 = get_vector(edges_list_0[0])
    vector_1 = get_vector(edges_list_0[1])

    normal_0 = np.cross(vector_0, vector_1) / np.linalg.norm(np.cross(vector_0, vector_1))

    vector_0 = get_vector(edges_list_1[0])
    vector_1 = get_vector(edges_list_1[1])

    normal_1 = np.cross(vector_0, vector_1) / np.linalg.norm(np.cross(vector_0, vector_1))

    angle = np.arccos(np.dot(normal_0, normal_1))
    degree = np.degrees(angle)

    return degree


if __name__ == '__main__':

    # 🔧 示例创建 vtkPolygon
    def create_polygon(points):
        poly = vtkPolygon()
        poly.GetPoints().SetNumberOfPoints(len(points))
        poly.GetPointIds().SetNumberOfIds(len(points))
        for i, pt in enumerate(points):
            poly.GetPoints().SetPoint(i, pt)
            poly.GetPointIds().SetId(i, i)

        u_grid = vtkUnstructuredGrid()
        u_grid.InsertNextCell(poly.GetCellType(), poly.GetPointIds())
        u_grid.SetPoints(poly.GetPoints())
        return u_grid


    # 🧪 示例数据
    polygon1 = create_polygon([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    polygon2 = create_polygon([(1, 0, 0.0000000001), (3, 0, 2), (3, 1, 2), (1.000000002, 1, 0)])

    angle = calculate_polygon_angle(polygon1, polygon2)
    print(f'angle is: {angle}')

