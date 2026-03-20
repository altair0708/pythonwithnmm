# import numpy as np
# from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
#
#
# def compute_outer_normal(ugrid: vtkUnstructuredGrid, point_id: int):
#     """
#     计算闭合共面曲线某点处的外法线方向
#
#     参数:
#         ugrid : vtkUnstructuredGrid
#             包含一段首尾相接的共面 vtkLine，形成闭合曲线
#         point_id : int
#             要计算外法线方向的点的 ID 值
#
#     返回:
#         numpy.ndarray, shape=(3,)
#             该点处的外法线单位向量
#     """
#
#     # 提取所有点
#     num_points = ugrid.GetNumberOfPoints()
#     points = np.array([ugrid.GetPoint(i) for i in range(num_points)])
#
#     # 计算质心
#     center = points.mean(axis=0)
#
#     # 用 SVD 拟合曲线所在平面法向量
#     X = points - center
#     _, _, Vt = np.linalg.svd(X)
#     plane_normal = Vt[-1] / np.linalg.norm(Vt[-1])
#
#     # 前后点索引（循环）
#     im = (point_id - 1) % num_points
#     ip = (point_id + 1) % num_points
#
#     # 切向量
#     t = points[ip] - points[im]
#     t = t / np.linalg.norm(t)
#
#     # 在平面内的候选法线（plane_normal × tangent）
#     n_cand = np.cross(plane_normal, t)
#     n_cand = n_cand / np.linalg.norm(n_cand)
#
#     # 判断内外：外法线应该指向远离质心
#     if np.dot(points[point_id] - center, n_cand) < 0:
#         n_cand = -n_cand
#
#     return n_cand

import numpy as np
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def compute_outer_normal(ugrid: vtkUnstructuredGrid, point_id: int):
    """
    计算闭合共面曲线某点处的外法线方向（在平面内，指向外侧）
    支持：ugrid 中包含多个互不相交的闭合环（每个环为凸多边形）
    """
    eps = 1e-12

    # ------------------------
    # 0) 基本信息
    # ------------------------
    num_points = ugrid.GetNumberOfPoints()
    if num_points < 3:
        raise ValueError("Need at least 3 points.")
    if point_id < 0 or point_id >= num_points:
        raise IndexError(f"point_id {point_id} out of range [0, {num_points - 1}]")

    points = np.array([ugrid.GetPoint(i) for i in range(num_points)], dtype=float)

    # ------------------------
    # 1) 从 vtkLine 单元构建邻接
    # ------------------------
    nbrs = [[] for _ in range(num_points)]
    num_cells = ugrid.GetNumberOfCells()
    for cid in range(num_cells):
        cell = ugrid.GetCell(cid)
        if cell is None:
            continue
        if cell.GetNumberOfPoints() != 2:
            # 不是线段则跳过
            continue
        a = cell.GetPointId(0)
        b = cell.GetPointId(1)
        nbrs[a].append(b)
        nbrs[b].append(a)

    # 目标点必须在某个环上（凸闭环 => 每点度数应为2）
    if len(nbrs[point_id]) != 2:
        raise ValueError(
            f"Point {point_id} has {len(nbrs[point_id])} neighbors; "
            "expected 2 for a closed polygonal loop."
        )

    # ------------------------
    # 2) 找到 point_id 所在“连通分量”（即所在那一环的点集合）
    # ------------------------
    visited = set()
    stack = [point_id]
    visited.add(point_id)

    while stack:
        cur = stack.pop()
        for nb in nbrs[cur]:
            if nb not in visited:
                visited.add(nb)
                stack.append(nb)

    loop_ids = sorted(visited)  # 该环包含的点 ID
    if len(loop_ids) < 3:
        raise ValueError("The connected component has fewer than 3 points; not a valid polygon loop.")

    # 可选：检查该连通分量是否为“纯环”（所有点度数=2）
    bad = [pid for pid in loop_ids if len(nbrs[pid]) != 2]
    if bad:
        raise ValueError(
            f"The component containing point {point_id} is not a simple loop. "
            f"These points do not have degree 2: {bad[:10]}{'...' if len(bad) > 10 else ''}"
        )

    loop_pts = points[loop_ids]
    center = loop_pts.mean(axis=0)  # 注意：用该环质心（凸多边形下判外稳定）

    # ------------------------
    # 3) 用该环的点拟合平面法向（SVD）
    # ------------------------
    X = loop_pts - center
    _, _, Vt = np.linalg.svd(X, full_matrices=False)
    plane_normal = Vt[-1]
    nlen = np.linalg.norm(plane_normal)
    if nlen < eps:
        raise ValueError("Degenerate plane normal (component points may be nearly collinear).")
    plane_normal = plane_normal / nlen

    # ------------------------
    # 4) 取该点的两个拓扑邻点，算切向
    # ------------------------
    im, ip = nbrs[point_id][0], nbrs[point_id][1]

    t = points[ip] - points[im]
    tlen = np.linalg.norm(t)
    if tlen < eps:
        raise ValueError("Degenerate tangent: neighbor points are too close or identical.")
    t = t / tlen

    # ------------------------
    # 5) 平面内候选外法线：plane_normal × tangent
    # ------------------------
    n_cand = np.cross(plane_normal, t)
    nlen2 = np.linalg.norm(n_cand)
    if nlen2 < eps:
        raise ValueError("Degenerate normal candidate: plane_normal is parallel to tangent.")
    n_cand = n_cand / nlen2

    # ------------------------
    # 6) 判内外（凸环：用“该环质心”即可）
    # 外法线应该指向远离该环质心
    # ------------------------
    if np.dot(points[point_id] - center, n_cand) < 0.0:
        n_cand = -n_cand

    return n_cand

# ========== 示例用法 ==========
if __name__ == "__main__":
    # 假设已经有一个 vtkUnstructuredGrid 对象 ugrid
    # 例如从文件读取：
    # reader = vtk.vtkUnstructuredGridReader()
    # reader.SetFileName("your_curve.vtk")
    # reader.Update()
    # ugrid = reader.GetOutput()

    # 演示：假设 ugrid 已经存在
    # 计算 point_id = 0 的外法线方向
    # normal = compute_outward_normal(ugrid, 0)
    # print("外法线方向:", normal)
    pass
