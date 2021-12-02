import sqlite3
from NMM.base.DataBase import insert_a_rows, delete_all_tables


class CvFileReader(object):
    _instance = None

    def __new__(cls, *args, **kwargs):  # Singleton, each item only have one CvFileReader
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, cv_file_name: str = 'cv04', data_base_name: str = 'test.db'):
        self.cv_filename = cv_file_name
        self.database_name = data_base_name
        self.database = sqlite3.connect(self.database_name)
        self.cursor = self.database.cursor()
        self.cv_file = open(self.cv_filename)
        self.manifold_element_number = 0
        self.fixed_point_number = 0
        self.loading_point_number = 0
        self.measured_point_number = 0
        self.joint_point_number = 0
        self.physical_patch_number = 0
        self.contact_loop_number = 0
        self.loop_vertexes_number = 0
        self.each_line = None
        self.id_generator = None
        self.sql_statement = ''

    def write_number_info(self):
        self.manifold_element_number, \
            self.fixed_point_number, \
            self.loading_point_number, \
            self.measured_point_number = self.cv_file.readline().split()
        self.joint_point_number, \
            self.physical_patch_number, \
            self.contact_loop_number, \
            self.loop_vertexes_number = self.cv_file.readline().split()
        # print(self.manifold_element_number)
        # print(self.fixed_point_number)
        # print(self.loading_point_number)
        # print(self.measured_point_number)
        # print(self.joint_point_number)
        # print(self.physical_patch_number)
        # print(self.contact_loop_number)
        # print(self.loop_vertexes_number)

    def build_table_structure(self):
        delete_all_tables(self.cursor)
        try:
            self.cursor.execute('CREATE TABLE SpecialPoints('
                                'ID        INT  PRIMARY KEY          NOT NULL,'
                                'xValue    REAL DEFAULT 0            NOT NULL,'
                                'yValue    REAL DEFAULT 0            NOT NULL,'
                                'elementID INT  DEFAULT 0            NOT NULL,'
                                "pointType TEXT DEFAULT 0            NOT NULL );")
        except sqlite3.OperationalError:
            print('SpecialPoints table is already existed')
        try:
            self.cursor.execute('CREATE TABLE ElementJoints('
                                'ID           INT  PRIMARY KEY          NOT NULL,'
                                'elementID    INT  DEFAULT 0            NOT NULL,'
                                'jointOrder   INT  DEFAULT 0            NOT NULL,'
                                'jointID      INT  DEFAULT 0            NOT NULL,'
                                'materialID   INT  DEFAULT 0            NOT NULL);')
        except sqlite3.OperationalError:
            print('ElementJoints table is already existed')
        try:
            self.cursor.execute('CREATE TABLE JointPoints('
                                'ID        INT  PRIMARY KEY          NOT NULL,'
                                'xValue    REAL DEFAULT 0            NOT NULL,'
                                'yValue    REAL DEFAULT 0            NOT NULL );')
        except sqlite3.OperationalError:
            print('JointPoints table is already existed')
        try:
            self.cursor.execute('CREATE TABLE PhysicalPatches('
                                'ID        INT  PRIMARY KEY          NOT NULL,'
                                'xValue    REAL DEFAULT 0            NOT NULL,'
                                'yValue    REAL DEFAULT 0            NOT NULL );')
        except sqlite3.OperationalError:
            print('PhysicalPatches table is already existed')
        try:
            self.cursor.execute('CREATE TABLE ElementPatches('
                                'ID           INT  PRIMARY KEY          NOT NULL,'
                                'elementID    INT  DEFAULT 0            NOT NULL,'
                                'patchOrder   INT  DEFAULT 0            NOT NULL,'
                                'patchID      INT  DEFAULT 0            NOT NULL);')
        except sqlite3.OperationalError:
            print('ElementJoints table is already existed')
        try:
            self.cursor.execute('CREATE TABLE ContactLoops('
                                'ID         INT  PRIMARY KEY          NOT NULL,'
                                'loopID     INT  DEFAULT 0            NOT NULL,'
                                'jointOrder INT  DEFAULT 0            NOT NULL,'
                                'jointID    INT  DEFAULT 0            NOT NULL,'
                                'materialID INT  DEFAULT 0            NOT NULL );')
        except sqlite3.OperationalError:
            print('ContactLoops table is already existed')

    def write_special_point_info(self):
        self.id_generator = id_generator()
        temp_count = 0

        for i in range(int(self.fixed_point_number)):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            self.each_line.insert(0, str(next(self.id_generator)))
            self.each_line.append('Fixed')
            try:
                insert_a_rows(table_name='SpecialPoints', data=self.each_line, database_cursor=self.cursor)
            except sqlite3.IntegrityError:
                temp_count = temp_count + 1
        print('Total of {} Fixed point, {} piece(s) of Fixed point are not inserted.'
              .format(self.fixed_point_number, temp_count))

        temp_count = 0
        for i in range(int(self.loading_point_number)):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            self.each_line.insert(0, str(next(self.id_generator)))
            self.each_line.append('Loading')
            try:
                insert_a_rows(table_name='SpecialPoints', data=self.each_line, database_cursor=self.cursor)
            except sqlite3.IntegrityError:
                temp_count = temp_count + 1
        print('Total of {} Loading point, {} piece(s) of Loading point are not inserted.'
              .format(self.loading_point_number, temp_count))

        temp_count = 0
        for i in range(int(self.measured_point_number)):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            self.each_line.insert(0, str(next(self.id_generator)))
            self.each_line.append('Measured')
            try:
                insert_a_rows(table_name='SpecialPoints', data=self.each_line, database_cursor=self.cursor)
            except sqlite3.IntegrityError:
                temp_count = temp_count + 1
        print('Total of {} Measured point, {} piece(s) of Measured point are not inserted.'
              .format(self.measured_point_number, temp_count))

        self.database.commit()
        self.id_generator = None

    def write_element_joint_info(self):
        temp_id_generator = id_generator()
        temp_count = 0
        for element_id in range(1, int(self.manifold_element_number) + 1):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            temp_start_id = int(self.each_line[0])
            temp_end_id = int(self.each_line[1])
            temp_material_id = int(self.each_line[2])
            temp_joint_order = 1
            for joint_id in range(temp_start_id, temp_end_id + 1):
                temp_list = [next(temp_id_generator), element_id, temp_joint_order, joint_id, temp_material_id]
                try:
                    insert_a_rows(table_name='ElementJoints', data=temp_list, database_cursor=self.cursor)
                except sqlite3.IntegrityError:
                    temp_count = temp_count + 1
                temp_joint_order = temp_joint_order + 1
        print('Total of {} Manifold element, total of {} pieces of data,'
              ' {} piece(s) of pieces of data not are not inserted.'
              .format(self.manifold_element_number, next(temp_id_generator) - 1, temp_count))

        self.database.commit()

    def write_joint_point_info(self):
        temp_id_generator = id_generator()
        temp_count = 0
        for i in range(int(self.joint_point_number)):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            self.each_line.insert(0, str(next(temp_id_generator)))
            try:
                insert_a_rows(table_name='JointPoints', data=self.each_line, database_cursor=self.cursor)
            except sqlite3.IntegrityError:
                temp_count = temp_count + 1
        print('Total of {} joint points, {} piece(s) of joint point are not inserted.'
              .format(self.joint_point_number, temp_count))
        self.database.commit()

    def write_physical_patch_info(self):
        temp_id_generator = id_generator()
        temp_count = 0
        for i in range(int(self.physical_patch_number)):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            self.each_line.insert(0, str(next(temp_id_generator)))
            try:
                insert_a_rows(table_name='PhysicalPatches', data=self.each_line, database_cursor=self.cursor)
            except sqlite3.IntegrityError:
                temp_count = temp_count + 1
        print('Total of {} Physical Patches, {} piece(s) of Physical Patch are not inserted.'
              .format(self.physical_patch_number, temp_count))
        self.database.commit()

    def write_element_patch_info(self):
        temp_id_generator = id_generator()
        temp_count = 0
        for element_id in range(1, int(self.manifold_element_number) + 1):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            temp_patch_order = 1
            for patch_id in self.each_line:
                temp_list = [next(temp_id_generator), element_id, temp_patch_order, patch_id]
                try:
                    insert_a_rows(table_name='ElementPatches', data=temp_list, database_cursor=self.cursor)
                except sqlite3.IntegrityError:
                    temp_count = temp_count + 1
                temp_patch_order = temp_patch_order + 1
        print('Total of {} Manifold element, total of {} pieces of data,'
              ' {} piece(s) of pieces of data not are not inserted.'
              .format(self.manifold_element_number, next(temp_id_generator) - 1, temp_count))
        self.database.commit()

    def write_contact_loop_info(self):
        temp_count = 0
        temp_id_generator = id_generator()
        temp_connect_loop_list = []
        for loop_number in range(int(self.contact_loop_number)):
            self.each_line = self.cv_file.readline()
            self.each_line = self.each_line.split()
            temp_connect_loop_list.append(self.each_line)
        for loop_id in range(1, int(self.contact_loop_number) + 1):
            loop_start = temp_connect_loop_list[loop_id - 1][0]
            loop_end = temp_connect_loop_list[loop_id - 1][1]
            for joint_order in range(1, int(loop_end) - int(loop_start) + 3):
                self.each_line = self.cv_file.readline()
                self.each_line = self.each_line.split()
                temp_joint_id = int(self.each_line[0])
                temp_material_id = int(self.each_line[1])
                temp_list = [next(temp_id_generator), loop_id, joint_order, temp_joint_id, temp_material_id]
                try:
                    insert_a_rows(table_name='ContactLoops', data=temp_list, database_cursor=self.cursor)
                except sqlite3.OperationalError:
                    temp_count = temp_count + 1
        print('Total of {} Contact Loop, total of {} pieces of data,'
              ' {} piece(s) of pieces of data not are not inserted.'
              .format(self.contact_loop_number, next(temp_id_generator) - 1, temp_count))
        self.database.commit()

    def run(self):
        self.write_number_info()
        self.build_table_structure()
        self.write_special_point_info()
        self.write_element_joint_info()
        self.write_joint_point_info()
        self.write_physical_patch_info()
        self.write_element_patch_info()
        self.write_contact_loop_info()

    def close(self):
        self.database.close()
        self.cv_file.close()


def id_generator():
    id_number = 1
    while True:
        yield id_number
        id_number += 1


if __name__ == '__main__':
    cv_filename = 'cv08'
    mf_filename = 'mf08'
    database_name = 'test.db'
    work_path = '../../data/'

    cv_reader = CvFileReader(cv_file_name=work_path + cv_filename, data_base_name=work_path + database_name)
    cv_reader.run()
    cv_reader.close()
