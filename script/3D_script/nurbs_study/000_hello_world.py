from geomdl import fitting
from geomdl.visualization import VisMPL as vis
import numpy as np
import matplotlib.pyplot as plt

# The NURBS Book Ex9.1
points = ((-2, -1.5), (0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3), (-2, -1.5))
degree = 3  # cubic curve

# Do global curve interpolation
curve = fitting.interpolate_curve(points, degree)
print(curve.ctrlpts)

# Prepare points
evalpts = np.array(curve.evalpts)
pts = np.array(points)

# Plot points together on the same graph
fig = plt.figure(figsize=(10, 8), dpi=96)
plt.plot(evalpts[:, 0], evalpts[:, 1])
plt.scatter(pts[:, 0], pts[:, 1], color="red")
plt.show()
