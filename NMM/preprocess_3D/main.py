from NMM.preprocess_3D.GenerateGeometryInfo import generate_geometry_info
from NMM.preprocess_3D.GenerateMathCover import generate_math_point, generate_math_cover
from NMM.preprocess_3D.GenerateManifoldElement import generate_manifold_element
from NMM.preprocess_3D.GenerateCrackSurfaceFile import generate_crack_surface_file
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, VTK_LINE, VTK_TRIANGLE, VTK_TETRA


def generate_all_vtu_file(gmsh_file_name, special_point_file_name, output_path):
    generate_geometry_info(gmsh_file_name, output_path, VTK_VERTEX)
    generate_geometry_info(gmsh_file_name, output_path, VTK_LINE)
    generate_geometry_info(gmsh_file_name, output_path, VTK_TRIANGLE)
    generate_geometry_info(gmsh_file_name, output_path, VTK_TETRA)

    tetrahedron_file = 'geometry_tetrahedron.vtu'
    gmsh_tetrahedron_file_name = output_path + tetrahedron_file

    generate_math_cover(gmsh_tetrahedron_file_name, output_path)
    generate_math_point(gmsh_tetrahedron_file_name, output_path)
    generate_manifold_element(gmsh_tetrahedron_file_name, special_point_file_name, output_path)

    element_manifold_file_name = output_path + 'manifold_element.vtu'
    initial_crack_file_name = output_path + 'initial_crack.vtu'
    generate_crack_surface_file(initial_crack_file_name, element_manifold_file_name, output_path)


if __name__ == '__main__':
    # file_name = 'simplex.vtu'
    # special_point_file = 'special_points_simplex.vtu'
    file_name = 'cylinder.vtu'
    # special_point_file = 'special_point_1.vtu'
    special_point_file = 'special_point.vtu'
    work_path = '../../data_3D/'
    gmsh_file = work_path + file_name
    special_point_file = work_path + special_point_file

    generate_all_vtu_file(gmsh_file, special_point_file, work_path)
