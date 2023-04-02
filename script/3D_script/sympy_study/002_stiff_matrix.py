from sympy import *

x_s = symbols('x1:4')
y_s = symbols('y1:4')

e, v = symbols('e, v')


# u = a1 + b1 * x + c1 * y
# v = a2 + b2 * x + c2 * y

a = Matrix([[1, x_s[0], y_s[0]],
            [1, x_s[1], y_s[1]],
            [1, x_s[2], y_s[2]]])

f = (a**(-1)).T

B = Matrix([[f[0, 1],       0, f[1, 1],       0, f[2, 1],       0],
            [      0, f[0, 2],       0, f[1, 2],       0, f[2, 2]],
            [f[0, 2], f[0, 1], f[1, 2], f[1, 1], f[2, 2], f[2, 1]]])

E = Matrix([[1, v, 0],
            [v, 1, 0],
            [0, 0, (1 - v) / 2]])

print(B.T * E * B)
# result = B.T * E * B
#
# print(det(result))

