import pickle
from sympy import *

with open('stiff_matrix.bin', 'rb') as f:
    matrix: MutableDenseMatrix = pickle.load(f)

row = matrix.shape[0]
col = matrix.shape[1]

with open('stiff_matrix.txt', 'w') as f:
    for each_row in range(row):
        for each_col in range(col):
            f.write('S[{a}, {b}]'.format(a=each_row, b=each_col))
            f.write(' = ')
            f.write(str(matrix[each_row, each_col]))
            f.write('\n')
