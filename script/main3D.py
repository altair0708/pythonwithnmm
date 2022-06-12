from NMM.control_3D.ElementCreater3D import ElementCreator3D
from NMM.control_3D.MatrixAssembly3D import MatrixAssembler3D
from NMM.control_3D.ElementRefresh3D import ElementRefresher3D
from NMM.GlobalVariable import CONST
from scipy.sparse.linalg import spsolve

element_file = '../data_3D/manifold_element.vtu'
mathcover_file = '../data_3D/math_cover.vtu'
database_name = '../data_3D/manifold_mathcover.db'
# special_point_file = '../data_3D/special_points_simplex.vtu'
special_point_file = '../data_3D/special_point.vtu'
# special_point_file = '../data_3D/special_point_1.vtu'
material_coefficient_file = '../data_3D/material_coefficient.json'
element_list = ElementCreator3D.create_all_element(database_name, element_file, mathcover_file, special_point_file, material_coefficient_file)

for step in range(3):
    print('step: {}'.format(step))
    stiff_matrix = MatrixAssembler3D.stiff_matrix(element_list, mathcover_file)
    force_vector = MatrixAssembler3D.force_vector(element_list, mathcover_file)
    a = stiff_matrix.toarray()
    assert a.all() == a.T.all()
    x = spsolve(stiff_matrix, force_vector)
    ElementRefresher3D.refresh_math_cover_file_displacement(x, mathcover_file)
    ElementRefresher3D.refresh_element_list_displacement(element_list, mathcover_file)
    ElementRefresher3D.refresh_manifold_element_file_displacement(element_list, element_file)
    ElementRefresher3D.clean_all(element_list)
    CONST.STEP = CONST.STEP + 1
