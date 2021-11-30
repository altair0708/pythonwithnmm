import sqlite3

cv_filename = 'cv04'
mf_filename = 'mf04'
database_name = 'test.db'
work_path = '../data/'

mysql = sqlite3.connect(work_path+database_name)
c = mysql.cursor()
# c.execute('DROP TABLE point;')
c.execute('CREATE TABLE point('
          'ID     INT PRIMARY KEY NOT NULL,'
          'XVALUE INT             NOT NULL,'
          'YVALUE INT             NOT NULL);')
c.execute('INSERT INTO point (ID, XVALUE, YVALUE)'
          'VALUES (1, 1, 3);')
mysql.commit()
mysql.close()
