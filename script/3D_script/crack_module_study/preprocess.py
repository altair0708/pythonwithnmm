from NMM.preprocess_3D.ExtractElementSurface import generate_element_surface
from NMM.preprocess_3D.GenerateManifoldElement import generate_manifold_element
from NMM.preprocess_3D.GenerateMathCover import generate_math_point, generate_math_cover
from NMM.preprocess_3D.GenerateCrackSurfaceFile import generate_crack_surface_file
from NMM.preprocess_3D.GenerateGeometryInfo import generate_geometry_info
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, VTK_LINE, VTK_TRIANGLE, VTK_TETRA

mesh_path = 'mesh_file/'
geometry_path = 'geometry_file/'

generate_geometry_info(mesh_path, geometry_path, VTK_VERTEX)
generate_geometry_info(mesh_path, geometry_path, VTK_LINE)
generate_geometry_info(mesh_path, geometry_path, VTK_TRIANGLE)
generate_geometry_info(mesh_path, geometry_path, VTK_TETRA)

generate_math_cover(mesh_path, geometry_path)
generate_math_point(mesh_path, geometry_path)
generate_manifold_element(mesh_path, geometry_path)

generate_element_surface(mesh_path, geometry_path)
generate_crack_surface_file(mesh_path, geometry_path)
