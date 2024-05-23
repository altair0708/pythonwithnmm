from NMM.preprocess_3D.GenerateGeometryInfo import generate_geometry_info
from NMM.preprocess_3D.GenerateManifoldElement import generate_manifold_element
from NMM.preprocess_3D.ExtractElementSurface import generate_element_surface
from NMM.preprocess_3D.GenerateCrackSurfaceFileNew import generate_crack_surface_file_1
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.crack_3D.CrackElementCreator3D import CrackElementCreator3D
from NMM.crack_3D.ElementCrackNew3D import ElementCracker3D
from NMM.crack_3D.CrackElementRefresh3D import CrackElementRefresher
from NMM.GlobalVariable import CONST, DataStructure, Variable, CrackList
from vtkmodules.vtkCommonDataModel import VTK_TETRA, vtkUnstructuredGrid

mesh_file = './mesh_file/'
geometry_file = './geometry_file/'

class PATH:
    work_path = ''
    element_file = 'geometry_file/manifold_element.vtu'
    crack_file = 'geometry_file/crack_surface.vtu'
    surface_file = 'geometry_file/element_surface.vtu'
    crack_edge = 'geometry_file/crack_edge.vtu'
    new_element_file = 'geometry_file/new_element.vtu'
    output_path = './result/'
    gmsh_file = 'gmsh_file.vtu'

generate_geometry_info(mesh_file, geometry_file, VTK_TETRA, path_file=PATH)
generate_manifold_element(mesh_file, geometry_file)
generate_element_surface(mesh_file, geometry_file)
generate_crack_surface_file_1(mesh_file, geometry_file)

data_structure = DataStructure()
data_structure.manifold_element = ElementIOer3D.load_vtk_model(PATH.element_file)
data_structure.crack_surface = ElementIOer3D.load_vtk_model(PATH.crack_file)
data_structure.element_surface = ElementIOer3D.load_vtk_model(PATH.surface_file)
data_structure.crack_edge = ElementIOer3D.load_vtk_model(PATH.crack_edge)
data_structure.new_element = ElementIOer3D.load_vtk_model(PATH.new_element_file)

for i in range(30):
    Variable.element_number = data_structure.manifold_element.content.GetNumberOfCells()
    Variable.surface_number = data_structure.element_surface.content.GetNumberOfCells()
    Variable.crack_surface_number = data_structure.crack_surface.content.GetNumberOfCells()
    Variable.crack_edge_number = data_structure.crack_edge.content.GetNumberOfCells()
    Variable.new_element_number = data_structure.new_element.content.GetNumberOfCells()

    CrackList.element_list = CrackElementCreator3D.create_all_element(data_structure)
    CrackList.surface_list = CrackElementCreator3D.create_all_surface(data_structure)
    CrackList.crack_surface_list = CrackElementCreator3D.create_all_crack_surface(data_structure)
    CrackList.crack_edge_list = CrackElementCreator3D.create_all_crack_edge(data_structure)
    # add new element to the list each step
    CrackList.new_element_list = []
    CrackElementCreator3D.build_all_link(CrackList.element_list,
                                         CrackList.surface_list,
                                         CrackList.crack_surface_list,
                                         CrackList.crack_edge_list)

    ElementCracker3D.crack_all_element(CrackList.element_list)

    CrackElementRefresher.refresh_manifold_element(data_structure, CrackList.element_list)
    CrackElementRefresher.refresh_element_surface(data_structure, CrackList.surface_list)
    CrackElementRefresher.refresh_crack_surface(data_structure, CrackList.crack_surface_list)
    CrackElementRefresher.refresh_crack_edge(data_structure, CrackList.crack_edge_list)
    CrackElementRefresher.refresh_new_element(data_structure, CrackList.new_element_list)
    CrackElementRefresher.refresh_physical_cover(data_structure, CrackList.element_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_surface, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.element_surface, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_edge, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.new_element, path_file=PATH)

    print('Step: {}'.format(CONST.STEP))
    CONST.STEP = CONST.STEP + 1


