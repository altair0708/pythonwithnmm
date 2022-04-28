import numpy as np
import matplotlib.pyplot as plt
a = np.array([[1.2, 1.11], [1.392593, 1.24], [1.2, 1.24]])
d = np.array([[0.458750, 1.24], [2.67525, 1.24], [1.567, 2.945]])
plt.triplot(a[:, 0], a[:, 1])
plt.triplot(d[:, 0], d[:, 1])
plt.show()
