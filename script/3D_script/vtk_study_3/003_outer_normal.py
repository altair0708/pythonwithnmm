import numpy as np
from numpy.linalg import norm, svd
from vtkmodules.vtkCommonDataModel import VTK_LINE
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.base.VTKBase import load_a_grid, write_file
from NMM.base.VTKBase.add_attribute.add_point_attribute import AddPointAttribute
from NMM.base.VTKBase.set_attribute.set_attribute import set_point_attribute
from collections import defaultdict, deque

def extract_all_polygons(grid):
    """提取所有闭合多边形轮廓，返回每个轮廓的点坐标和点 ID 有序列表"""
    num_cells = grid.GetNumberOfCells()
    edges = []

    for i in range(num_cells):
        cell = grid.GetCell(i)
        if cell.GetCellType() == VTK_LINE:
            pt0 = cell.GetPointId(0)
            pt1 = cell.GetPointId(1)
            edges.append((pt0, pt1))

    # 构建点连接图
    edge_map = defaultdict(list)
    for a, b in edges:
        edge_map[a].append(b)
        edge_map[b].append(a)

    visited = set()
    polygons = []

    for start in edge_map:
        if start in visited:
            continue
        # 找一个轮廓
        current = start
        polygon_ids = []
        prev = None

        while True:
            polygon_ids.append(current)
            visited.add(current)
            neighbors = edge_map[current]
            next_pts = [pt for pt in neighbors if pt != prev and pt not in visited]
            if not next_pts:
                break
            prev = current
            current = next_pts[0]
            if current == start:
                break

        # 处理闭环
        if polygon_ids[0] != polygon_ids[-1]:
            polygon_ids.append(polygon_ids[0])

        polygon_points = [np.array(grid.GetPoint(pid)) for pid in polygon_ids]
        polygons.append((polygon_points, polygon_ids))

    return polygons

def estimate_plane_normal(points):
    """SVD 拟合平面，返回法向量"""
    pts = np.array(points)
    centroid = pts.mean(axis=0)
    centered = pts - centroid
    _, _, vh = svd(centered)
    normal = vh[2]
    return normal / norm(normal), centroid

def compute_outer_normal_at_vertex_3d(points, ids, target_id, plane_normal):
    n = len(points)
    try:
        idx = ids.index(target_id)
    except ValueError:
        raise ValueError("target_id not in polygon")

    # 若存在重复首尾点，去除末尾点
    if np.allclose(points[0], points[-1]):
        points = points[:-1]
        ids = ids[:-1]
        n -= 1
        idx = ids.index(target_id)

    prev_pt = points[(idx - 1) % n]
    curr_pt = points[idx]
    next_pt = points[(idx + 1) % n]

    v1 = curr_pt - prev_pt
    v2 = next_pt - curr_pt
    tangent = (v1 + v2) / 2.0
    tangent /= norm(tangent)

    # 投影到平面
    tangent_proj = tangent - np.dot(tangent, plane_normal) * plane_normal
    tangent_proj /= norm(tangent_proj)

    # 外法线：右手规则
    outward_normal = np.cross(plane_normal, tangent_proj)
    outward_normal /= norm(outward_normal)

    return outward_normal

def compute_outer_normal(grid, target_point_id):
    polygons = extract_all_polygons(grid)

    for poly_points, poly_ids in polygons:
        if target_point_id in poly_ids:
            plane_normal, _ = estimate_plane_normal(poly_points)
            return compute_outer_normal_at_vertex_3d(poly_points, poly_ids, target_point_id, plane_normal)

    raise ValueError("Target point ID not found in any polygon.")


if __name__ == '__main__':
    grid = load_a_grid('crack_tip.vtu')
    AddPointAttribute.add_float_array(grid, 'out_normal', 3, False)
    for each_point_id in range(grid.GetNumberOfPoints()):
        normal = compute_outer_normal(grid, each_point_id)
        set_point_attribute(grid, 'out_normal', each_point_id, normal)
        print("Outer normal at vertex", each_point_id, ":", normal)

    write_file(grid, 're003_out_normal.vtu')
