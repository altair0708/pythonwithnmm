from NMM.preprocess_3D.GenerateGeometryInfo import generate_geometry_info
from NMM.preprocess_3D.GenerateMathCover import generate_math_point, generate_math_cover
from NMM.preprocess_3D.GenerateManifoldElement import generate_manifold_element
from NMM.preprocess_3D.GenerateCrackSurfaceFile import generate_crack_surface_file_1
from NMM.preprocess_3D.ExtractElementSurface import generate_element_surface
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, VTK_LINE, VTK_TRIANGLE, VTK_TETRA


def generate_all_vtu_file(mesh_path: str, geometry_path: str):
    generate_geometry_info(mesh_path, geometry_path, VTK_VERTEX)
    generate_geometry_info(mesh_path, geometry_path, VTK_LINE)
    generate_geometry_info(mesh_path, geometry_path, VTK_TRIANGLE)
    generate_geometry_info(mesh_path, geometry_path, VTK_TETRA)

    generate_math_cover(mesh_path, geometry_path)
    generate_math_point(mesh_path, geometry_path)
    generate_manifold_element(mesh_path, geometry_path, True)

    # crack module
    generate_element_surface(mesh_path, geometry_path)
    generate_crack_surface_file_1(mesh_path, geometry_path)


if __name__ == '__main__':
    mesh_path = '../../data_3D/mesh/'
    geometry_path = '../../data_3D/geometry/'
    generate_all_vtu_file(mesh_path, geometry_path)
