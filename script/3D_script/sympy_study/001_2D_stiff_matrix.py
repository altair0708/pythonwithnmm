from sympy import *
import numpy as np

x_s = symbols('x_0:4')
y_s = symbols('y_0:4')
z_s = symbols('z_0:4')

E, v = symbols('E v')
E_matrix = Matrix([[1, v, 0],
                   [v, 1, 0],
                   [0, 0, (1-v)/2]])

a = Matrix([[1, x_s[0], y_s[0]],
            [1, x_s[1], y_s[1]],
            [1, x_s[2], y_s[2]]])

f_0 = symbols('f_0_0:3')
f_1 = symbols('f_1_0:3')
f_2 = symbols('f_2_0:3')

b = Matrix([[f_0[0], f_0[1], f_0[2]],
            [f_1[0], f_1[1], f_1[2]],
            [f_2[0], f_2[1], f_2[2]]])

# c = Eq(a**(-1), b.T)

B_matrix = Matrix([[f_0[1],      0, f_1[1],      0, f_2[1],      0],
                   [     0, f_0[2],      0, f_1[2],      0, f_2[2]],
                   [f_0[2], f_0[1], f_1[2], f_1[1], f_2[2], f_2[1]]])

e_0 = symbols('e_0_0:3')
e_1 = symbols('e_1_0:3')
e_2 = symbols('e_2_0:3')
C_matrix = Matrix([[e_0[1],      0, e_1[1],      0, e_2[1],      0],
                   [     0, e_0[2],      0, e_1[2],      0, e_2[2]],
                   [e_0[2], e_0[1], e_1[2], e_1[1], e_2[2], e_2[1]]])

z = symbols('z')
D_matrix = Matrix([[1, 1, 1, 0, 0, 0],
                   [1, 1, 1, 1, 0, 0],
                   [1, 1, 1, 1, 1, 0]])

G_matrix = Matrix([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])

J_matrix = Matrix([[1, 1, 1],
                   [0, 2, 1],
                   [0, 0, 3]])
result = D_matrix.T * J_matrix * D_matrix

print(det(J_matrix))

D_matrix = np.array([[1, 1, 1, 0, 0, 0],
                     [1, 1, 1, 1, 0, 0],
                     [1, 1, 1, 1, 1, 0]])

J_matrix = np.array([[1, 1, 1],
                     [0, 2, 1],
                     [0, 0, 3]])

temp = np.dot(D_matrix.T, J_matrix)
temp = np.dot(temp, D_matrix)
print(np.linalg.det(temp))
