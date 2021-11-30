import pytest
import sqlite3
from NMM.base.DataBase import insert_a_rows, query_by_id, delete_all_tables


class TestDataBase(object):
    def test_insert_query(self):
        data_list = [1, 2, 3, 4, 5]
        table_name1 = 'test'
        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE test('
                       'ID        INT  PRIMARY KEY          NOT NULL,'
                       'xValue    INT  DEFAULT 0            NOT NULL,'
                       'yValue    INT  DEFAULT 0            NOT NULL,'
                       'zValue    INT  DEFAULT 0            NOT NULL,'
                       'elementID INT  DEFAULT 0            NOT NULL);')
        insert_a_rows(table_name1, data_list, cursor)
        a = query_by_id(table_name1, 1, cursor)
        connection.close()
        assert a[0] == tuple(data_list)

    def test_delete_all_tables(self):
        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE SpecialPoints('
                       'ID        INT  PRIMARY KEY          NOT NULL,'
                       'xValue    REAL DEFAULT 0            NOT NULL,'
                       'yValue    REAL DEFAULT 0            NOT NULL,'
                       'elementID INT  DEFAULT 0            NOT NULL);')
        cursor.execute('CREATE TABLE SpecialPoint1('
                       'ID        INT  PRIMARY KEY          NOT NULL,'
                       'xValue    REAL DEFAULT 0            NOT NULL,'
                       'yValue    REAL DEFAULT 0            NOT NULL,'
                       'elementID INT  DEFAULT 0            NOT NULL);')
        a = cursor.execute('SELECT name FROM sqlite_master;')
        a = a.fetchall()
        delete_all_tables(cursor)
        a = cursor.execute('SELECT name FROM sqlite_master;')
        a = a.fetchall()
        connection.close()
        assert a == []


if __name__ == '__main__':
    pytest.main()
