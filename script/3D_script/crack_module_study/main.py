from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.crack_3D.CrackElementCreator3D import CrackElementCreator3D
from NMM.crack_3D.ElementCrack3D import ElementCracker3D
from NMM.crack_3D.CrackElementRefresh3D import CrackElementRefresher
from NMM.GlobalVariable import CONST, DataStructure, Variable, CrackList

class PATH:
    work_path = ''
    element_file = 'geometry_file/manifold_element.vtu'
    mathcover_file = 'geometry_file/math_cover.vtu'
    crack_file = 'geometry_file/crack_surface.vtu'
    database_name = 'geometry_file/manifold_mathcover.db'
    material_coefficient_file = 'materical/material_coefficient.json'
    surface_file = 'geometry_file/element_surface.vtu'
    crack_edge = 'geometry_file/crack_edge.vtu'
    output_path = './result/'

data_structure = DataStructure()
data_structure.manifold_element = ElementIOer3D.load_vtk_model(PATH.element_file)
data_structure.physical_cover = ElementIOer3D.load_vtk_model(PATH.mathcover_file)
data_structure.crack_surface = ElementIOer3D.load_vtk_model(PATH.crack_file)
data_structure.relationship_element_cover = ElementIOer3D.load_database(PATH.database_name)
data_structure.element_surface = ElementIOer3D.load_vtk_model(PATH.surface_file)
data_structure.crack_edge = ElementIOer3D.load_vtk_model(PATH.crack_edge)

for step in range(30):
    print('step: {}'.format(step))

    Variable.cover_number = data_structure.physical_cover.content.GetNumberOfCells()
    Variable.element_number = data_structure.manifold_element.content.GetNumberOfCells()
    Variable.surface_number = data_structure.element_surface.content.GetNumberOfCells()
    Variable.crack_surface_number = data_structure.crack_surface.content.GetNumberOfCells()
    Variable.crack_edge_number = data_structure.crack_edge.content.GetNumberOfCells()

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

