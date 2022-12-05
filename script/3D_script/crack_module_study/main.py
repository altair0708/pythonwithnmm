from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.crack_3D.CrackElementCreator3D import CrackElementCreator3D
from NMM.crack_3D.ElementCrack3D import ElementCracker3D
from NMM.crack_3D.CrackElementRefresh3D import CrackElementRefresher
from NMM.GlobalVariable import CONST, DataStructure, Variable

class PATH:
    work_path = ''
    element_file = 'manifold_element.vtu'
    mathcover_file = 'math_cover.vtu'
    crack_file = 'crack_surface.vtu'
    database_name = 'manifold_mathcover.db'
    material_coefficient_file = 'material_coefficient.json'
    output_path = './result/'

data_structure = DataStructure()
data_structure.manifold_element = ElementIOer3D.load_vtk_model(PATH.element_file)
data_structure.physical_cover = ElementIOer3D.load_vtk_model(PATH.mathcover_file)
data_structure.crack_surface = ElementIOer3D.load_vtk_model(PATH.crack_file)
data_structure.relationship_element_cover = ElementIOer3D.load_database(PATH.database_name)

for step in range(30):
    print('step: {}'.format(step))
    Variable.cover_number = data_structure.physical_cover.content.GetNumberOfCells()
    Variable.element_number = data_structure.manifold_element.content.GetNumberOfCells()

    crack_element_list = CrackElementCreator3D.create_all_element(data_structure)

    ElementCracker3D.crack_all_element(crack_element_list)

    CrackElementRefresher.refresh_manifold_element(data_structure, crack_element_list)
    CrackElementRefresher.refresh_physical_cover(data_structure, crack_element_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.physical_cover, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_surface, path_file=PATH)

    del crack_element_list

    CONST.STEP = CONST.STEP + 1

