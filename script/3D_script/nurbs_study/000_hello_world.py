from geomdl import fitting
from geomdl.visualization import VisMPL as vis
import numpy as np
import matplotlib.pyplot as plt

# The NURBS Book Ex9.1
points = ((3, 4), (-1, 4), (-4, 0), (-4, -3))
points_1 = ((2, 2), (0, 2), (-2, -1), (-2, -3))
degree = 3  # cubic curve

# Do global curve interpolation
curve = fitting.interpolate_curve(points, degree)
curve_1 = fitting.interpolate_curve(points_1, degree)


# Prepare points
evalpts = np.array(curve.evalpts)
pts = np.array(points)

evalpts_1 = np.array(curve_1.evalpts)
pts_1 = np.array(points_1)

# Plot points together on the same graph
fig = plt.figure(figsize=(10, 8), dpi=96)

plt.plot(evalpts[:, 0], evalpts[:, 1])
plt.scatter(pts[:, 0], pts[:, 1], color="red")

plt.plot(evalpts_1[:, 0], evalpts_1[:, 1])
plt.scatter(pts_1[:, 0], pts_1[:, 1], color="blue")

plt.quiver([2, 0, -2, -2], [2, 2, -1, -3], [1, -1, -2, -2], [2, 2, 1, 0], color=(1, 0, 0, 0.3), angles='xy', scale_units='xy', scale=1)
plt.show()
