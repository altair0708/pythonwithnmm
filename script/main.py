from NMM.fem.ElementCreator import ElementCreator
from NMM.fem.PatchWithDataBase import get_patch_number, write_patch_displacement_into_database
from NMM.fem.MatrixAssembly import MatrixAssembler
from NMM.fem.ElementRefresh import ElementRefresher
from NMM.preprocess.CvFileReader import CvFileReader
from NMM.plot.PlotPatchDisplacement import plot_patch_displacement
from scipy.sparse.linalg import spsolve
import sqlite3

cv_filename = 'cv00'
database_name = 'test.db'
work_path = '../data/'

cv_reader = CvFileReader(cv_file_name=work_path + cv_filename, data_base_name=work_path + database_name)
cv_reader.run()
cv_reader.close()

database_name = '../data/test.db'
with sqlite3.connect(database_name) as connection:
    database_cursor = connection.cursor()
    element_creator = ElementCreator(database_cursor)
    patch_number = get_patch_number(database_cursor)
    temp_element_list = element_creator.start()

    for i in range(20):
        print('Step: {step}'.format(step=i + 1))
        stiff_matrix = MatrixAssembler.stiff_matrix(temp_element_list, patch_number)
        force_vector = MatrixAssembler.force_vector(temp_element_list, patch_number)
        print('########################')

        x = spsolve(stiff_matrix, force_vector)

        element_creator.clean(temp_element_list)
        ElementRefresher.refresh_patch_displacement(x, temp_element_list, database_cursor)
        ElementRefresher.refresh_joint_displacement(temp_element_list, database_cursor)
        raise Exception('stop')
    plot_patch_displacement(database_cursor)


