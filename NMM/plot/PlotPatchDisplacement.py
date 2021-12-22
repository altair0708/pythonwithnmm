import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def plot_patch_displacement(cursor: sqlite3.Cursor):
    database_statement = 'SELECT xValue, yValue, uDis, vDis FROM PhysicalPatches'
    result = cursor.execute(database_statement)
    result = result.fetchall()
    result = np.array(result)
    temp_x = result[:, 0]
    temp_y = result[:, 1]
    temp_u = result[:, 2]
    temp_v = result[:, 3]
    plt.tricontourf(temp_x, temp_y, temp_u, levels=500, cmap=cm.jet)
    plt.show()
    plt.tricontourf(temp_x, temp_y, temp_v, levels=500, cmap=cm.jet)
    plt.show()
