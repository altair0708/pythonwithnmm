from scipy.sparse import *
from scipy.sparse.linalg import spsolve
import numpy as np

a = np.array([1, 1, 1, 1])
b = np.array([0, 1, 2, 3], dtype=np.int32)
c = np.array([0, 1, 2, 3], dtype=np.int32)
d = coo_matrix((a, (b, c)))
d = d.tocsc()
e = np.array([3, 4, 5, 6])
f = spsolve(d, e)
f = f.reshape((-1, 2))
print(f)
