from NMM.preprocess_3D.GmshReader import GmshReader
from NMM.preprocess_3D.ExtractElementSurface import generate_element_surface

output_path = ''
# tetrahedron_file = 'geometry_tetrahedron.vtu'
tetrahedron_file = 'tetrahedron_grid.vtu'
gmsh_tetrahedron_file_name = output_path + tetrahedron_file

GmshReader.generate_math_cover(gmsh_tetrahedron_file_name, output_path)
GmshReader.generate_math_point(gmsh_tetrahedron_file_name, output_path)
GmshReader.generate_manifold_element(gmsh_tetrahedron_file_name, '', output_path)

element_manifold_file_name = output_path + 'manifold_element.vtu'
initial_crack_file_name = output_path + 'initial_crack.vtu'
generate_element_surface(element_manifold_file_name, output_path)
GmshReader.generate_crack_surface_file(initial_crack_file_name, element_manifold_file_name, output_path)

