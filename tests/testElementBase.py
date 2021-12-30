import numpy as np
from NMM.control.ElementCreator import create_an_element
from NMM.fem.ElementWithDataBase import *


def test_create_element():
    database_name = '../data/test.db'
    with sqlite3.connect(database_name) as connection:
        database_cursor = connection.cursor()
        element_number = get_element_number(database_cursor)
        for each_id in range(1, element_number + 1):
            temp_element = create_an_element(each_id, cursor=database_cursor)
            assert len(temp_element.patch_list) == 3
            assert len(temp_element.joint_list) == get_element_joint_number(each_id, cursor=database_cursor)
            assert temp_element.material_dict['body_force'] == [0, 1]


def test_element_weight_function():
    database_name = '../data/test.db'
    with sqlite3.connect(database_name) as connection:
        database_cursor = connection.cursor()
        element_number = get_element_number(database_cursor)
        for each_id in range(1, element_number + 1):
            temp_element = create_an_element(each_id, cursor=database_cursor)
            weight_matrix = lambda x, y: np.dot(temp_element.delta_matrix, np.array([[1], [x], [y]]))
            for each_point in temp_element.joint_list:
                assert np.dot(np.array([1, 1, 1]), weight_matrix(each_point[0], each_point[1])).all() == 1
                assert np.dot(np.array([1, 1, 1]), weight_matrix(each_point[0], each_point[1])).shape == (1, 1)

