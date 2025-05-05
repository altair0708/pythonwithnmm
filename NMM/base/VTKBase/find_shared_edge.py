import math
from vtkmodules.vtkCommonDataModel import vtkPolygon, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints

TOLERANCE = 0.0001


def are_points_close(p1, p2, tol=TOLERANCE):
    """判断两个点是否在容差范围内"""
    return math.dist(p1, p2) < tol


def rounded_key(p):
    """生成用于比较的近似键"""
    return tuple(round(coord / TOLERANCE) for coord in p)


def normalize_edge_for_compare(p1, p2):
    """用于比较的标准化边（无方向，近似点）"""
    return tuple(sorted([rounded_key(p1), rounded_key(p2)]))


def get_edges_with_original_coords(vtk_model: vtkUnstructuredGrid):
    """返回一组边：每条边是原始坐标点对，但比较时用容差键"""

    assert vtk_model.GetNumberOfCells() == 1
    polygon = vtk_model.GetCell(0)

    points = polygon.GetPoints()
    n = points.GetNumberOfPoints()
    edge_dict = {}

    for i in range(n):
        p1 = points.GetPoint(i)
        p2 = points.GetPoint((i + 1) % n)

        key = normalize_edge_for_compare(p1, p2)
        edge_dict[key] = (p1, p2)  # 保存原始边坐标

    return edge_dict


def find_shared_edge(poly1, poly2):
    edges1 = get_edges_with_original_coords(poly1)
    edges2 = get_edges_with_original_coords(poly2)

    shared_keys = set(edges1.keys()) & set(edges2.keys())
    return [edges1[k] for k in shared_keys]




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
    polygon2 = create_polygon([(1, 0, 0.00001), (1, 0, 1), (1, 1, 1), (1.00002, 1, 0)])

    shared = find_shared_edge(polygon1, polygon2)
    print("共用边原始坐标：")
    for edge in shared:
        print(edge)

