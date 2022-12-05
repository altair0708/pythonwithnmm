from numpy.linalg import eigh
import numpy as np

a = np.matrix([[2, 2, -2],
               [2, 5, -4],
               [-2, -4, 5]])

w, u = eigh(a)
print(w)
print(u[:, 0])
print(u[:, 1])
print(u[:, 2])
