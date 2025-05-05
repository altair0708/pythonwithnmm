import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def fit_plane(points):
    points = np.array(points)
    centroid = np.mean(points, axis=0)
    centered = points - centroid
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    normal = eigvecs[:, np.argmin(eigvals)]
    d = -np.dot(normal, centroid)
    return normal, d, centroid

# 示例点
points = np.array([
    [1.0, 2.0, 6.0],
    [2.0, 3.0, 4.0],
    [3.0, 4.0, 5.0],
    [4.0, 5.0, 5.8],
    [2.5, 3.2, 3.9]
])

# 拟合平面
normal, d, centroid = fit_plane(points)

# 构造平面网格用于绘图
xx, yy = np.meshgrid(
    np.linspace(points[:,0].min()-1, points[:,0].max()+1, 10),
    np.linspace(points[:,1].min()-1, points[:,1].max()+1, 10)
)

# 由平面方程 ax + by + cz + d = 0 解出 z
a, b, c = normal
zz = (-a * xx - b * yy - d) / c

# 可视化
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制原始点
ax.scatter(points[:,0], points[:,1], points[:,2], color='blue', label='Points')

# 绘制质心
ax.scatter(*centroid, color='red', s=50, label='Centroid')

# 绘制拟合平面
ax.plot_surface(xx, yy, zz, alpha=0.5, color='orange', label='Fitted Plane')

# 坐标轴与图例
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.title("Least Squares Plane Fitting")
plt.show()
