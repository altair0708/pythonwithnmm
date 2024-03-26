# calculate minimum distance plane from given four points use least square.

from scipy.optimize import leastsq
from typing import List
import numpy as np


def min_distance_plane(points_list: List):
    point_0 = np.array([points_list[0]])
    point_1 = np.array([points_list[1]])
    point_2 = np.array([points_list[2]])
    point_3 = np.array([points_list[3]])
    points = np.row_stack((point_0, point_1, point_2, point_3))
    # print(points)

    # 定义目标函数（平面方程）
    def plane_func(p, points):
        a, b, c, d = p
        x, y, z = points.T
        return a * x + b * y + c * z + d

    # 定义残差函数
    def residuals(p, points):
        a, b, c, d = p
        x, y, z = points.T
        distance = (a * x + b * y + c * z + d)**2 / (a**2 + b**2 + c**2)
        return distance

    # 提供初始参数估计
    p0 = [1, 1, 1, 1]

    # 使用leastsq函数进行拟合
    params_fit, success = leastsq(residuals, p0, args=(points,))

    # 获取拟合结果
    a_fit, b_fit, c_fit, d_fit = params_fit

    # print("拟合结果：")
    # print("a =", a_fit)
    # print("b =", b_fit)
    # print("c =", c_fit)
    # print("d =", d_fit)

    normal_vector = np.array([a_fit, b_fit, c_fit])
    normalize_vector = normal_vector / np.linalg.norm(normal_vector)
    # print(normalize_vector)

    z = -(d_fit / c_fit)
    origin_point = (0, 0, z)
    # print(origin_point)

    return origin_point, normalize_vector

