from scipy.interpolate import interpn, LinearNDInterpolator, griddata
from shapely.geometry import Polygon
from shapely.affinity import scale
import numpy as np
import matplotlib.pyplot as plt

point_1 = np.array([0, 0])
point_2 = np.array([0, 1])
point_3 = np.array([1, 1])
point_4 = np.array([1, 1])
points = np.array([point_1, point_2, point_3])
z = np.array([[1, 1],
              [2, 2],
              [3, 3]])

point = np.array([[-0.01, 0.5],
                  [-0.01, 0],
                  [1.001, 1.001]])
fig = plt.figure()
axes = fig.add_subplot(111)
axes.triplot(point[:, 0], point[:, 1], linestyle='dashed')
polygon_a = Polygon(point)
polygon_a = scale(polygon_a, 0.97, 0.97, origin='centroid')
x, y = polygon_a.exterior.xy
x = np.array(x)
y = np.array(y)
axes.triplot(x, y)
fig.show()

x = x.reshape((-1, 1))
y = y.reshape((-1, 1))
point = np.c_[x, y]
print(point)
result = griddata(points, z, point)
print(result)
