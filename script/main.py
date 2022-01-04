from NMM.control.ElementCreator import ElementCreator
from NMM.control.MatrixAssembly import MatrixAssembler
from NMM.control.ElementRefresh import ElementRefresher
from NMM.preprocess.CvFileReader import CvFileReader
from NMM.plot.PlotPatchDisplacement import plot_joint_displacement
from scipy.sparse.linalg import spsolve

cv_filename = 'cvUniaxialCompression01'
database_name = ':memory:'
work_path = '../data/'

cv_reader = CvFileReader(cv_file_name=work_path+cv_filename, data_base_name=database_name)
cv_reader.run()
database_cursor = cv_reader.cursor

element_creator = ElementCreator(database_cursor)
temp_element_list = element_creator.start()

for i in range(10):
    print('Step: {step}'.format(step=i + 1))
    stiff_matrix = MatrixAssembler.stiff_matrix(temp_element_list, database_cursor)
    force_vector = MatrixAssembler.force_vector(temp_element_list, database_cursor)

    x = spsolve(stiff_matrix, force_vector)

    element_creator.clean(temp_element_list)
    ElementRefresher.refresh_patch_displacement(x, temp_element_list, database_cursor)
    ElementRefresher.refresh_joint_displacement(temp_element_list, database_cursor)

plot_joint_displacement(database_cursor)
cv_reader.close()
