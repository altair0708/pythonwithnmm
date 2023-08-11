from NMM.control_3D.ElementCreator3D import ElementCreator3D
from NMM.control_3D.MatrixAssembly3D import MatrixAssembler3D
from NMM.control_3D.ElementRefresh3D import ElementRefresher3D
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.crack_3D.CrackElementCreator3D import CrackElementCreator3D
from NMM.crack_3D.ElementCrack3D import ElementCracker3D
from NMM.crack_3D.CrackElementRefresh3D import CrackElementRefresher
from NMM.GlobalVariable import CONST, PATH, DataStructure, Variable, CrackList
from scipy.sparse.linalg import spsolve, cg, lsmr, lsqr, gmres, aslinearoperator
import numpy as np

data_structure = DataStructure()
data_structure.physical_cover = ElementIOer3D.load_vtk_model(PATH.mathcover_file)
data_structure.relationship_element_cover = ElementIOer3D.load_database(PATH.database_name)
data_structure.manifold_element = ElementIOer3D.load_vtk_model(PATH.element_file)
data_structure.element_surface = ElementIOer3D.load_vtk_model(PATH.surface_file)
data_structure.crack_surface = ElementIOer3D.load_vtk_model(PATH.crack_file)
data_structure.crack_edge = ElementIOer3D.load_vtk_model(PATH.crack_edge)
data_structure.special_point = ElementIOer3D.load_vtk_model(PATH.special_point_file)
for step in range(30):
    print('step: {}'.format(step))
    Variable.cover_number = data_structure.physical_cover.content.GetNumberOfCells()
    Variable.element_number = data_structure.manifold_element.content.GetNumberOfCells()
    Variable.surface_number = data_structure.element_surface.content.GetNumberOfCells()
    Variable.crack_surface_number = data_structure.crack_surface.content.GetNumberOfCells()
    Variable.crack_edge_number = data_structure.crack_edge.content.GetNumberOfCells()

    element_list = ElementCreator3D.create_element_list(data_structure, PATH.material_coefficient_file)

    stiff_matrix = MatrixAssembler3D.stiff_matrix(element_list, Variable.cover_number)
    force_vector = MatrixAssembler3D.force_vector(element_list, Variable.cover_number)
    # print(np.linalg.det(stiff_matrix.toarray()))
    # print(np.linalg.cond(stiff_matrix.toarray()))
    # print(np.linalg.matrix_rank(stiff_matrix.toarray()))
    x = spsolve(stiff_matrix, force_vector)

    # singular matrix
    if np.isnan(x).any():
        # print(stiff_matrix.shape)
        # np.save('singular_stiff_matrix.npy', stiff_matrix.toarray())
        # raise Exception('Matrix is exactly singular!')
        # x = total_least_square(stiff_matrix, force_vector)

        # svd solver
        # stiff_matrix_0 = pinv(stiff_matrix.toarray())
        # print('Full rank:', np.linalg.matrix_rank(stiff_matrix.toarray()) == stiff_matrix.toarray().shape[0])
        # x = np.dot(stiff_matrix_0, force_vector)
        # x, _, _, _ = np.linalg.lstsq(stiff_matrix.toarray(), force_vector)

        # Conjugate gradient solver
        # stiff_diag = diags(stiff_matrix.diagonal(), 0)
        # print(type(stiff_diag))
        # x, exit_code = cg(stiff_matrix, force_vector, M=stiff_diag)
        x, exit_code = cg(stiff_matrix, force_vector, tol=1e-15, atol=0.01)
        # print('exit_code:', exit_code)

    # stiff_matrix_operator = aslinearoperator(stiff_matrix)
    # force_vector_0 = stiff_matrix_operator.matvec(x)
    # error = np.linalg.norm(force_vector - force_vector_0, ord=2)
    # relative_error = error / np.linalg.norm(force_vector, ord=2)
    # print('relative error: {num}'.format(num=relative_error))

    ElementRefresher3D.refresh_physical_cover(x, data_structure.physical_cover)
    ElementRefresher3D.refresh_manifold_element(data_structure, element_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element)
    ElementIOer3D.write_vtk_model(data_structure.physical_cover)
    ElementIOer3D.write_vtk_model(data_structure.special_point)

    CrackList.element_list = CrackElementCreator3D.create_all_element(data_structure)
    CrackList.surface_list = CrackElementCreator3D.create_all_surface(data_structure)
    CrackList.crack_surface_list = CrackElementCreator3D.create_all_crack_surface(data_structure)
    CrackList.crack_edge_list = CrackElementCreator3D.create_all_crack_edge(data_structure)
    CrackElementCreator3D.build_all_link(CrackList.element_list,
                                         CrackList.surface_list,
                                         CrackList.crack_surface_list,
                                         CrackList.crack_edge_list)

    ElementCracker3D.crack_all_element(CrackList.element_list)

    CrackElementRefresher.refresh_manifold_element(data_structure, CrackList.element_list)
    CrackElementRefresher.refresh_element_surface(data_structure, CrackList.surface_list)
    CrackElementRefresher.refresh_crack_surface(data_structure, CrackList.crack_surface_list)
    CrackElementRefresher.refresh_crack_edge(data_structure, CrackList.crack_edge_list)
    CrackElementRefresher.refresh_physical_cover(data_structure, CrackList.element_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.physical_cover, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_surface, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.element_surface, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_edge, path_file=PATH)

    CONST.STEP = CONST.STEP + 1

