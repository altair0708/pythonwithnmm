import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
x, y = np.meshgrid(a, b, indexing='ij')
x = np.reshape(x, (1, -1))
y = np.reshape(y, (1, -1))
print(x)
print(y)
