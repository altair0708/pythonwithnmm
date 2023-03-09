from NMM.preprocess_3D.GenerateGeometryInfo import generate_geometry_info
from NMM.preprocess_3D.GenerateManifoldElement import generate_manifold_element
from NMM.preprocess_3D.ExtractElementSurface import generate_element_surface
from NMM.preprocess_3D.GenerateCrackSurfaceFile import generate_crack_surface_file, generate_crack_surface_file_0
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.crack_3D.CrackElementCreator3D import CrackElementCreator3D
from NMM.crack_3D.ElementCrack3D import ElementCracker3D
from NMM.crack_3D.CrackElementRefresh3D import CrackElementRefresher
from NMM.GlobalVariable import CONST, DataStructure, Variable
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.CleanUnstructuredGridFunction import clean_unstructured_grid
from NMM.base.CheckDihedralAngle import check_dihedral_angle
from vtkmodules.vtkCommonDataModel import VTK_TETRA, vtkUnstructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

mesh_file = './mesh/'
geometry_file = './geometry/'

generate_geometry_info(mesh_file, geometry_file, VTK_TETRA)
generate_manifold_element(mesh_file, geometry_file)
generate_element_surface(mesh_file, geometry_file)
generate_crack_surface_file_0(mesh_file, geometry_file)

class PATH:
    work_path = ''
    element_file = 'geometry/manifold_element.vtu'
    crack_file = 'geometry/crack_surface.vtu'
    surface_file = 'geometry/element_surface.vtu'
    crack_edge = 'geometry/crack_edge.vtu'
    output_path = './result/'

data_structure = DataStructure()
data_structure.manifold_element = ElementIOer3D.load_vtk_model(PATH.element_file)
data_structure.crack_surface = ElementIOer3D.load_vtk_model(PATH.crack_file)
data_structure.element_surface = ElementIOer3D.load_vtk_model(PATH.surface_file)
data_structure.crack_edge = ElementIOer3D.load_vtk_model(PATH.crack_edge)

for i in range(2):
    Variable.element_number = data_structure.manifold_element.content.GetNumberOfCells()
    Variable.surface_number = data_structure.element_surface.content.GetNumberOfCells()

    crack_element_list = CrackElementCreator3D.create_all_element(data_structure)
    element_surface_list = CrackElementCreator3D.create_all_surface(data_structure)
    CrackElementCreator3D.build_element_surface_link(crack_element_list, element_surface_list)

    ElementCracker3D.crack_all_element(crack_element_list)

    CrackElementRefresher.refresh_manifold_element(data_structure, crack_element_list)
    CrackElementRefresher.refresh_element_surface(data_structure, element_surface_list)

    ElementIOer3D.write_vtk_model(data_structure.manifold_element, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_surface, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.element_surface, path_file=PATH)
    ElementIOer3D.write_vtk_model(data_structure.crack_edge, path_file=PATH)
    del crack_element_list, element_surface_list

    CONST.STEP = CONST.STEP + 1


