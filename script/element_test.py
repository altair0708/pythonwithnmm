import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from scipy.interpolate import griddata
from NMM.fem.ElementCreator import create_an_element
from NMM.fem.ElementWithDataBase import get_element_number

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_number = get_element_number(database_cursor)
    element = create_an_element(1, database_cursor)

    patch_coord = np.array(element.patch_list)
    patch_displacement = np.array(element.patch_displacement)
    joint_coord = np.array(element.joint_list)

    patch_x = patch_coord[:, 0]
    patch_y = patch_coord[:, 1]
    patch_u = patch_displacement[:, 0]
    patch_v = patch_displacement[:, 1]
    joint_x = joint_coord[:, 0]
    joint_y = joint_coord[:, 1]
    z = griddata(patch_coord, patch_displacement, joint_coord, method='cubic')
    print(z)
