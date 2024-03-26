from scipy.optimize import leastsq
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkVertex, vtkPlane, vtkUnstructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
import numpy as np

# 已知四个点的坐标
# points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
# points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
point_0 = np.array([[0, 0, 0]])
point_1 = np.array([[1, 0, 0]])
point_2 = np.array([[0, 1, 0]])
point_3 = np.array([[0, 0, 1]])
points = np.row_stack((point_0, point_1, point_2, point_3))
print(points)

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

print("拟合结果：")
print("a =", a_fit)
print("b =", b_fit)
print("c =", c_fit)
print("d =", d_fit)

normal_vector = np.array([a_fit, b_fit, c_fit])
normalize_vector = normal_vector / np.linalg.norm(normal_vector)
print(normalize_vector)
z = -(d_fit / c_fit)
origin_point = (0, 0, z)
print(origin_point)

vertex_points = vtkPoints()
vertex_points.InsertNextPoint(point_0[0])
vertex_points.InsertNextPoint(point_1[0])
vertex_points.InsertNextPoint(point_2[0])
vertex_points.InsertNextPoint(point_3[0])

vertex_0 = vtkVertex()
vertex_0.GetPointIds().SetId(0, 0)
vertex_1 = vtkVertex()
vertex_1.GetPointIds().SetId(0, 1)
vertex_2 = vtkVertex()
vertex_2.GetPointIds().SetId(0, 2)
vertex_3 = vtkVertex()
vertex_3.GetPointIds().SetId(0, 3)

vertex_grid = vtkUnstructuredGrid()
vertex_grid.InsertNextCell(vertex_0.GetCellType(), vertex_0.GetPointIds())
vertex_grid.InsertNextCell(vertex_1.GetCellType(), vertex_1.GetPointIds())
vertex_grid.InsertNextCell(vertex_2.GetCellType(), vertex_2.GetPointIds())
vertex_grid.InsertNextCell(vertex_3.GetCellType(), vertex_3.GetPointIds())

vertex_grid.SetPoints(vertex_points)

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('re006_vertex.vtu')
writer.SetInputData(vertex_grid)
writer.Write()

print(vertex_grid.GetPoints().GetPoint(0))


