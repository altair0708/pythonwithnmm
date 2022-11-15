from NMM.control_3D.ElementCreator3D import ElementCreator3D
from NMM.control_3D.MatrixAssembly3D import MatrixAssembler3D
from NMM.control_3D.ElementRefresh3D import ElementRefresher3D
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.crack_3D.CrackElementCreator3D import CrackElementCreator3D
from NMM.crack_3D.ElementCrack3D import ElementCracker3D
from NMM.crack_3D.CrackElementRefresh3D import CrackElementRefresher
from NMM.GlobalVariable import CONST, PATH, DataStructure, Variable
from scipy.sparse.linalg import spsolve

data_structure = DataStructure()
data_structure.manifold_element = ElementIOer3D.load_vtk_model(PATH.element_file)
data_structure.physical_cover = ElementIOer3D.load_vtk_model(PATH.mathcover_file)
data_structure.crack_surface = ElementIOer3D.load_vtk_model(PATH.crack_file)
data_structure.relationship_element_cover = ElementIOer3D.load_database(PATH.database_name)
data_structure.special_point = ElementIOer3D.load_vtk_model(PATH.special_point_file)
for step in range(300):
    print('step: {}'.format(step))
    Variable.cover_number = data_structure.physical_cover.content.GetNumberOfCells()
    Variable.element_number = data_structure.manifold_element.content.GetNumberOfCells()

    element_list = ElementCreator3D.create_element_list(data_structure, PATH.material_coefficient_file)

    stiff_matrix = MatrixAssembler3D.stiff_matrix(element_list, Variable.cover_number)
    force_vector = MatrixAssembler3D.force_vector(element_list, Variable.cover_number)
    x = spsolve(stiff_matrix, force_vector)

    ElementRefresher3D.refresh_physical_cover(x, data_structure.physical_cover)
    ElementRefresher3D.refresh_manifold_element(data_structure, element_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element)
    ElementIOer3D.write_vtk_model(data_structure.physical_cover)

    del element_list

    crack_element_list = CrackElementCreator3D.create_all_element(data_structure)

    ElementCracker3D.crack_all_element(crack_element_list)

    CrackElementRefresher.refresh_manifold_element(data_structure, crack_element_list)
    CrackElementRefresher.refresh_physical_cover(data_structure, crack_element_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element)
    ElementIOer3D.write_vtk_model(data_structure.physical_cover)
    ElementIOer3D.write_vtk_model(data_structure.crack_surface)

    del crack_element_list

    CONST.STEP = CONST.STEP + 1

