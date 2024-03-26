import numpy as np

# 输入四个点的坐标
x1, y1, z1 = map(float, input("请输入第一个点的坐标(x,y,z):").split(","))
x2, y2, z2 = map(float, input("请输入第二个点的坐标(x,y,z):").split(","))
x3, y3, z3 = map(float, input("请输入第三个点的坐标(x,y,z):").split(","))
x4, y4, z4 = map(float, input("请输入第四个点的坐标(x,y,z):").split(","))

# 将点的坐标存入矩阵A
A = np.array([[x1, y1, 1],
              [x2, y2, 1],
              [x3, y3, 1],
              [x4, y4, 1]])

# 将点的z坐标存入向量b
b = np.array([z1, z2, z3, z4])

# 使用最小二乘法求解平面方程
x, y, c = np.linalg.lstsq(A, b, rcond=None)[0]

print(f"最优平面方程为: z = {x:.2f}x + {y:.2f}y + {c:.2f}")