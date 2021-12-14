from shapely.geometry import Polygon
import numpy as np

point_list = [[0, 0], [3, 0], [0, 1]]
a = Polygon(point_list)
print(a.area)
b = np.array([[3, 0], [0, 1]])
print(np.linalg.det(b))
