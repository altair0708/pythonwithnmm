import numpy as np


def once_integration(point_list: np.ndarray):
    if point_list.shape != (4, 3):
        raise Exception('please input a 3 rows 2 columns matrix')
    jacobi = np.c_[np.ones((4, 1)), point_list]
    jacobi = np.matrix(jacobi)
    jacobi = np.linalg.det(jacobi)
    S = (1 / 6) * jacobi
    xS = (1 / 24) * jacobi * (np.sum(point_list[:, 0]))
    yS = (1 / 24) * jacobi * (np.sum(point_list[:, 1]))
    zS = (1 / 24) * jacobi * (np.sum(point_list[:, 2]))
    return S, xS, yS, zS


def twice_integration(point_list: np.ndarray):
    if point_list.shape != (4, 3):
        raise Exception('please input a 3 rows 2 columns matrix')
    x0 = point_list[0, 0]
    y0 = point_list[0, 1]
    z0 = point_list[0, 2]

    x1 = point_list[1, 0]
    y1 = point_list[1, 1]
    z1 = point_list[1, 2]

    x2 = point_list[2, 0]
    y2 = point_list[2, 1]
    z2 = point_list[2, 2]

    x3 = point_list[3, 0]
    y3 = point_list[3, 1]
    z3 = point_list[3, 2]
    jacobi = np.c_[np.ones((4, 1)), point_list]
    jacobi = np.matrix(jacobi)
    jacobi = np.linalg.det(jacobi)
    xxS = (1 / 120) * jacobi * (2 * x0 * x0 + x0 * x1 + x0 * x2 + x0 * x3 +
                                x1 * x0 + 2 * x1 * x1 + x1 * x2 + x1 * x3 +
                                x2 * x0 + x2 * x1 + 2 * x2 * x2 + x2 * x3 +
                                x3 * x0 + x3 * x1 + x3 * x2 + 2 * x3 * x3)
    yyS = (1 / 120) * jacobi * (2 * y0 * y0 + y0 * y1 + y0 * y2 + y0 * y3 +
                                y1 * y0 + 2 * y1 * y1 + y1 * y2 + y1 * y3 +
                                y2 * y0 + y2 * y1 + 2 * y2 * y2 + y2 * y3 +
                                y3 * y0 + y3 * y1 + y3 * y2 + 2 * y3 * y3)
    zzS = (1 / 120) * jacobi * (2 * z0 * z0 + z0 * z1 + z0 * z2 + z0 * z3 +
                                z1 * z0 + 2 * z1 * z1 + z1 * z2 + z1 * z3 +
                                z2 * z0 + z2 * z1 + 2 * z2 * z2 + z2 * z3 +
                                z3 * z0 + z3 * z1 + z3 * z2 + 2 * z3 * z3)
    xyS = (1 / 120) * jacobi * (2 * x0 * y0 + x0 * y1 + x0 * y2 + x0 * y3 +
                                x1 * y0 + 2 * x1 * y1 + x1 * y2 + x1 * y3 +
                                x2 * y0 + x2 * y1 + 2 * x2 * y2 + x2 * y3 +
                                x3 * y0 + x3 * y1 + x3 * y2 + 2 * x3 * y3)
    xzS = (1 / 120) * jacobi * (2 * x0 * z0 + x0 * z1 + x0 * z2 + x0 * z3 +
                                x1 * z0 + 2 * x1 * z1 + x1 * z2 + x1 * z3 +
                                x2 * z0 + x2 * z1 + 2 * x2 * z2 + x2 * z3 +
                                x3 * z0 + x3 * z1 + x3 * z2 + 2 * x3 * z3)
    yzS = (1 / 120) * jacobi * (2 * y0 * z0 + y0 * z1 + y0 * z2 + y0 * z3 +
                                y1 * z0 + 2 * y1 * z1 + y1 * z2 + y1 * z3 +
                                y2 * z0 + y2 * z1 + 2 * y2 * z2 + y2 * z3 +
                                y3 * z0 + y3 * z1 + y3 * z2 + 2 * y3 * z3)

    return xxS, yyS, zzS, xyS, xzS, yzS
