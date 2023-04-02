import numpy as np


def f_function(point_0, point_1, point_2, point_3):

    assert len(point_0) == 3
    assert len(point_1) == 3
    assert len(point_2) == 3
    assert len(point_3) == 3

    x0 = point_0[0]
    y0 = point_0[1]
    z0 = point_0[2]

    x1 = point_1[0]
    y1 = point_1[1]
    z1 = point_1[2]

    x2 = point_2[0]
    y2 = point_2[1]
    z2 = point_2[2]

    x3 = point_3[0]
    y3 = point_3[1]
    z3 = point_3[2]

    f_0_0 = (-x1*y2*z3 + x1*y3*z2 + x2*y1*z3 - x2*y3*z1 - x3*y1*z2 + x3*y2*z1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_1_0 = (x0*y2*z3 - x0*y3*z2 - x2*y0*z3 + x2*y3*z0 + x3*y0*z2 - x3*y2*z0)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_2_0 = (-x0*y1*z3 + x0*y3*z1 + x1*y0*z3 - x1*y3*z0 - x3*y0*z1 + x3*y1*z0)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_3_0 = (x0*y1*z2 - x0*y2*z1 - x1*y0*z2 + x1*y2*z0 + x2*y0*z1 - x2*y1*z0)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_0_1 = (y1*z2 - y1*z3 - y2*z1 + y2*z3 + y3*z1 - y3*z2)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_1_1 = (-y0*z2 + y0*z3 + y2*z0 - y2*z3 - y3*z0 + y3*z2)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_2_1 = (y0*z1 - y0*z3 - y1*z0 + y1*z3 + y3*z0 - y3*z1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_3_1 = (-y0*z1 + y0*z2 + y1*z0 - y1*z2 - y2*z0 + y2*z1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_0_2 = (-x1*z2 + x1*z3 + x2*z1 - x2*z3 - x3*z1 + x3*z2)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_1_2 = (x0*z2 - x0*z3 - x2*z0 + x2*z3 + x3*z0 - x3*z2)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_2_2 = (-x0*z1 + x0*z3 + x1*z0 - x1*z3 - x3*z0 + x3*z1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_3_2 = (x0*z1 - x0*z2 - x1*z0 + x1*z2 + x2*z0 - x2*z1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_0_3 = (x1*y2 - x1*y3 - x2*y1 + x2*y3 + x3*y1 - x3*y2)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_1_3 = (-x0*y2 + x0*y3 + x2*y0 - x2*y3 - x3*y0 + x3*y2)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_2_3 = (x0*y1 - x0*y3 - x1*y0 + x1*y3 + x3*y0 - x3*y1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)
    f_3_3 = (-x0*y1 + x0*y2 + x1*y0 - x1*y2 - x2*y0 + x2*y1)/(x0*y1*z2 - x0*y1*z3 - x0*y2*z1 + x0*y2*z3 + x0*y3*z1 - x0*y3*z2 - x1*y0*z2 + x1*y0*z3 + x1*y2*z0 - x1*y2*z3 - x1*y3*z0 + x1*y3*z2 + x2*y0*z1 - x2*y0*z3 - x2*y1*z0 + x2*y1*z3 + x2*y3*z0 - x2*y3*z1 - x3*y0*z1 + x3*y0*z2 + x3*y1*z0 - x3*y1*z2 - x3*y2*z0 + x3*y2*z1)

    f_matrix = np.array([[f_0_0, f_0_1, f_0_2, f_0_3],
                         [f_1_0, f_1_1, f_1_2, f_1_3],
                         [f_2_0, f_2_1, f_2_2, f_2_3],
                         [f_3_0, f_3_1, f_3_2, f_3_3]])

    return f_matrix
