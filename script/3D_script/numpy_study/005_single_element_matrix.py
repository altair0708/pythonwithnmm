import numpy as np

a = np.matrix([[1, 0, 0],
               [1, 1, 0],
               [1, 0, 1]])
f = np.linalg.inv(a).T

e = np.matrix([[1, 0.2, 0],
               [0.2, 1, 0],
               [0, 0, 0.4]])
e = e * (10 / 0.96)

b = np.array([[-1,  0, 1, 0, 0, 0],
              [ 0, -1, 0, 0, 0, 1],
              [-1, -1, 0, 1, 1, 0]])

temp = np.dot(b.T, e)
temp = np.dot(temp, b)
stiff = 0.5 * temp

fixed = np.array([[100000, 0, 0, 0, 0, 0],
                  [0, 100000, 0, 0, 0, 0],
                  [0, 0, 100000, 0, 0, 0],
                  [0, 0, 0, 100000, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]])

total = stiff + fixed
force = np.array([[0],
                  [0],
                  [0],
                  [0],
                  [0],
                  [1]])

x = np.linalg.solve(total, force)

strain_1 = np.dot(b, x)

stress_1 = np.dot(e, strain_1)

initial_matrix = 0.5 * np.dot(b.T, stress_1)

force_1 = force - initial_matrix

x_1 = np.linalg.solve(total, force_1)
print(x)
print(x / 2)
