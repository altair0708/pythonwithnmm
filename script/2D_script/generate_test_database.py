import sqlite3
import os
from NMM.preprocess.CvFileReader import CvFileReader


for id_value in range(1, 16):
    cv_file = 'cv{id_value}'.format(id_value=str(id_value).rjust(2,'0'))
    work_path = os.path.abspath('../../data') + '/'
    database_name = 'test{id_value}.db'.format(id_value=str(id_value).rjust(2, '0'))
    cv_reader = CvFileReader(cv_file_name=work_path + cv_file, data_base_name=work_path + database_name)
    cv_reader.run()
    cv_reader.close()

