from NMM.fem_3D.ElementBase_3D import calculate_integration
import numpy as np

point_list = np.array([(0, 0, 0),
                       (1, 0, 0),
                       (0, 1, 0),
                       (0, 0, 1)])

s, xs, ys, zs = calculate_integration(point_list)

print(s)
