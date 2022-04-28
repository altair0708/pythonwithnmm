import numpy as np


def GetClockAngle(v1, v2):
    # 2个向量模的乘积
    TheNorm = np.linalg.norm(v1)*np.linalg.norm(v2)
    # 叉乘
    rho = np.rad2deg(np.arcsin(np.cross(v1, v2)/TheNorm))
    # 点乘
    theta = np.rad2deg(np.arccos(np.dot(v1, v2)/TheNorm))
    if rho < 0:
        return theta
    else:
        return 360 - theta


a = [0, 1]
b = [1, 0]
c = [-1, 0]
d = [-0.01, -1]
e = [-1, -1]
f = [1, -1]
g = [1, 1]
h = [-1, 1]
print(GetClockAngle(a,g), GetClockAngle(a,b), GetClockAngle(a,f), GetClockAngle(a,d), \
      GetClockAngle(a,e), GetClockAngle(a,c), GetClockAngle(a,h))