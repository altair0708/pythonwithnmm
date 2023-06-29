import numpy as np
from copy import deepcopy

stiff_matrix = np.load('re002_singular_stiff_matrix.npy')
# stiff_matrix_0 = deepcopy(stiff_matrix)
# stiff_matrix_0 = stiff_matrix_0.T
# diag: np.ndarray = stiff_matrix.diagonal()
# diag = np.diag(diag)
# print(np.linalg.det(diag))
# M = np.linalg.inv(diag)
# print(np.linalg.cond(stiff_matrix))
# A0 = np.array(M, stiff_matrix)
# print(np.linalg.cond(A0))
# print(np.linalg.pinv(stiff_matrix))
print(np.linalg.matrix_rank(stiff_matrix))
print(stiff_matrix.shape)

# a = np.array([[1, 1, 1],
#               [1, 1, 0],
#               [0, 0, 1]])
# print(np.linalg.cond(a))
# s, v, d = np.linalg.svd(a)
# print(v)

