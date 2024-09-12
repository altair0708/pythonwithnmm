from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Part.FilePath.FilePath import FilePath
from NMM.base.Property.Implement.Path import Path
import os


class FilePathBuilder(AbstractConstructor):
    def __init__(self, root_path):
        self.__root_path = root_path

    def build(self):
        file_path = FilePath()

        # work_path
        work_path = Path('work_path', self.path_cater(self.__root_path))
        file_path.add_property(work_path)

        # preprocess mesh_path
        mesh_path_str = self.path_cater(self.__root_path, 'mesh')
        mesh_path = Path('mesh_path', mesh_path_str)
        file_path.add_property(mesh_path)

        mesh_file_list = ['gmsh_file', 'special_point', 'initial_crack']
        for each_mesh_file in mesh_file_list:
            temp_path = Path(each_mesh_file, self.path_cater(mesh_path_str, f'{each_mesh_file}.vtu'))
            file_path.add_property(temp_path)

        # calculation geometry_path
        geometry_path_str = self.path_cater(self.__root_path, 'geometry')
        geometry_path = Path('geometry_path', geometry_path_str)
        geometry_path.mkdir()
        file_path.add_property(geometry_path)

        geometry_file_list = ['database']
        entity_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
        cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface']
        crack_list = ['crack_surface', 'crack_edge', 'new_element']
        for each_geometry_file in geometry_file_list + entity_list + cover_list + crack_list:
            if 'database' == each_geometry_file:
                temp_path = Path(each_geometry_file, self.path_cater(geometry_path_str, f'{each_geometry_file}.db'))
            else:
                temp_path = Path(each_geometry_file, self.path_cater(geometry_path_str, f'{each_geometry_file}.vtu'))
            file_path.add_property(temp_path)

        # postprocess result_path
        result_path = Path('result_path', self.path_cater(self.__root_path, 'result'))
        result_path.mkdir()
        file_path.add_property(result_path)

        return file_path

    @staticmethod
    def path_cater(root_path, direction_path=''):
        # method to normalize and generate a absolute path
        return os.path.normpath(os.path.join(root_path, direction_path))

