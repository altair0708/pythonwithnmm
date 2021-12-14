import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

E = 5000
mu = 0.3
temp = E * (1 - 0.3 ** 2)
Elastic_matrix = np.array([[1, mu, 0],
                           [mu, 1, 0],
                           [0, 0, (1 - mu)]])
Elastic_matrix = temp * Elastic_matrix
point_list = [(0, 0), (1, 0), (1, 1), (0, 2)]
patch_list = [(0, 0), (2, 0), (0, 2)]
point_array = np.array(point_list)
patch_array = np.array(patch_list)
temp_array = np.ones((3, 1))
delta = np.c_[temp_array, patch_array]
delta = np.matrix(delta)

print(delta.I)
triangle = Delaunay(point_array)
for each_triangle in point_array[triangle.simplices]:
    plt.triplot(each_triangle[:, 0], each_triangle[:, 1])
plt.show()
