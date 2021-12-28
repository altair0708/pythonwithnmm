import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from NMM.contact.ContactWithDatabase import get_loop_number


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


def plot_joint_displacement(cursor: sqlite3.Cursor):
    loop_number = get_loop_number(cursor)
    for loop_id in range(1, loop_number + 1):
        database_statement = 'SELECT xValue, yValue, uDis FROM JointPoints AS JP INNER JOIN ContactLoops AS CL on ' \
                             'JP.ID = CL.jointID WHERE loopID = {loop_id}'.format(loop_id=loop_id)
        result = cursor.execute(database_statement)
        result = result.fetchall()
        result = np.array(result)
        temp_x = result[:, 0]
        temp_y = result[:, 1]
        temp_u = result[:, 2]
        plt.tricontourf(temp_x, temp_y, temp_u, levels=500, cmap=cm.jet)
    plt.colorbar()
    plt.show()

    for loop_id in range(1, loop_number + 1):
        database_statement = 'SELECT xValue, yValue, vDis FROM JointPoints AS JP INNER JOIN ContactLoops AS CL on ' \
                             'JP.ID = CL.jointID WHERE loopID = {loop_id}'.format(loop_id=loop_id)
        result = cursor.execute(database_statement)
        result = result.fetchall()
        result = np.array(result)
        temp_x = result[:, 0]
        temp_y = result[:, 1]
        temp_v = result[:, 2]
        plt.tricontourf(temp_x, temp_y, temp_v, levels=500, cmap=cm.jet)
    plt.colorbar()
    plt.show()
