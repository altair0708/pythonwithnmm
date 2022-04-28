import matplotlib.pyplot as plt
from NMM.control.ElementCreator import ElementCreator
from NMM.control.MatrixAssembly import MatrixAssembler
from NMM.control.ElementRefresh import ElementRefresher
from NMM.preprocess.CvFileReader import CvFileReader
from NMM.plot.PlotPatchDisplacement import plot_joint_x_displacement, plot_joint_y_displacement
from scipy.sparse.linalg import spsolve

cv_filename = 'cvUniaxialCompression02'
database_name = ':memory:'
work_path = '../data/'

cv_reader = CvFileReader(cv_file_name=work_path+cv_filename, data_base_name=database_name)
cv_reader.run()
database_cursor = cv_reader.cursor

element_creator = ElementCreator(database_cursor)
temp_element_list = element_creator.start()

plt.ion()
fig: plt.Figure = plt.figure(figsize=(16, 9))
for i in range(100):
    print('{step}'.format(step=i + 1))
    stiff_matrix = MatrixAssembler.stiff_matrix(temp_element_list, database_cursor)
    force_vector = MatrixAssembler.force_vector(temp_element_list, database_cursor)
    a = stiff_matrix.toarray()

    x = spsolve(stiff_matrix, force_vector)

    element_creator.clean(temp_element_list)
    ElementRefresher.refresh_patch_displacement(x, temp_element_list, database_cursor)
    ElementRefresher.refresh_joint_displacement(temp_element_list, database_cursor)
    print('##########')

    fig.clf()
    ax1: plt.Axes = fig.add_subplot(121)
    ax2: plt.Axes = fig.add_subplot(122)
    plot_joint_x_displacement(database_cursor, ax1)
    plot_joint_y_displacement(database_cursor, ax2)
    plt.pause(0.01)

plt.ioff()
plt.show()
cv_reader.close()
