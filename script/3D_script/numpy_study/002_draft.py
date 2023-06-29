import sys
import numpy as np
from scipy.linalg import hilbert, solve
from scipy.sparse.linalg import spsolve

num = 4
A: np.ndarray = hilbert(num)
# A = np.eye(num)
# print(np.linalg.cond(A))

'''
Tikhonov regularization
'''
# A0 = np.dot(A.T, A)
# A0 = A0 + 1 * np.eye(num)
# # print(np.linalg.cond(A0))
#
# x = np.random.random((num, 1))
# # print(x)
#
# b = np.dot(A, x)
#
# x0 = solve(A, b)
# # print(x0)
# print((np.linalg.norm(x0 - x, ord=2) / np.linalg.norm(x, ord=2)))
#
# b0 = np.dot(A.T, b)
# x1 = solve(A0, b0)
# # print(x1)
# print((np.linalg.norm(x1 - x, ord=2) / np.linalg.norm(x, ord=2)))

'''
'''

a = np.array([[2, 0, 0],
              [0, 1, 0],
              [0, 0, 0.000000000000001]])
s, v, d = np.linalg.svd(a)
b = np.linalg.eigvals(a)
print(np.linalg.inv(a))
print(np.linalg.det(a))
# print(np.linalg.pinv(a))
print(np.linalg.matrix_rank(a))

