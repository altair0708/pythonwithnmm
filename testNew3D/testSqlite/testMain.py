from NMM.base.SqliteBase import add_a_relationship, new_a_table, new_a_database
import sqlite3
import pytest


def test_add_a_relationship():
    new_a_database('test.db')
    new_a_table('test.db', 'a_b')
    for i in range(100):
        add_a_relationship('test.db', 'a_b', {'a': i, 'b': i + 1})


