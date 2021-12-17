import pytest
import sqlite3
from NMM.fem.ElementWithDataBase import *


def test_get_element_number():
    for database_id in range(1, 16):
        database_name = '../data/test{database_id}.db'.format(database_id=str(database_id).rjust(2, '0'))
        with sqlite3.connect(database_name) as database_connect:
            database_cursor = database_connect.cursor()
            total = database_cursor.execute('SELECT MAX(ID) FROM ElementJoints')
            total = total.fetchall()[0][0]

            temp_joint_number = 0
            for each_element in range(get_element_number(database_cursor)):

                total_joint = get_element_joint_number(each_element + 1, database_cursor)
                temp_joint_number = temp_joint_number + total_joint
                joint_number = get_one_element_joint(each_element + 1, database_cursor)
                assert total_joint == len(joint_number)

                patch_number = get_one_element_patch(each_element + 1, database_cursor)
                assert len(patch_number) == 3

            assert total == temp_joint_number


def test_get_special_point():
    for database_id in range(1, 16):
        database_name = '../data/test{database_id}.db'.format(database_id=str(database_id).rjust(2, '0'))
        with sqlite3.connect(database_name) as database_connect:
            database_cursor = database_connect.cursor()
            total = database_cursor.execute('SELECT MAX(ID) FROM SpecialPoints')
            total = total.fetchall()[0][0]

            temp_special_point = 0
            for each_element in range(1, get_element_number(database_cursor) + 1):
                result = get_one_special_point(id_value=each_element, cursor=database_cursor)
                if len(result) != 0:
                    temp_special_point = temp_special_point + len(result)
            try:
                assert total == temp_special_point
            except AssertionError:
                print(f'{database_name}')
                raise AssertionError

