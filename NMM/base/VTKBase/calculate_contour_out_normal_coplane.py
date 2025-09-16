import numpy as np
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def compute_outer_normal(ugrid: vtkUnstructuredGrid, point_id: int):
    """
    计算闭合共面曲线某点处的外法线方向

    参数:
        ugrid : vtkUnstructuredGrid
            包含一段首尾相接的共面 vtkLine，形成闭合曲线
        point_id : int
            要计算外法线方向的点的 ID 值

    返回:
        numpy.ndarray, shape=(3,)
            该点处的外法线单位向量
    """

    # 提取所有点
    num_points = ugrid.GetNumberOfPoints()
    points = np.array([ugrid.GetPoint(i) for i in range(num_points)])

    # 计算质心
    center = points.mean(axis=0)

    # 用 SVD 拟合曲线所在平面法向量
    X = points - center
    _, _, Vt = np.linalg.svd(X)
    plane_normal = Vt[-1] / np.linalg.norm(Vt[-1])

    # 前后点索引（循环）
    im = (point_id - 1) % num_points
    ip = (point_id + 1) % num_points

    # 切向量
    t = points[ip] - points[im]
    t = t / np.linalg.norm(t)

    # 在平面内的候选法线（plane_normal × tangent）
    n_cand = np.cross(plane_normal, t)
    n_cand = n_cand / np.linalg.norm(n_cand)

    # 判断内外：外法线应该指向远离质心
    if np.dot(points[point_id] - center, n_cand) < 0:
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
