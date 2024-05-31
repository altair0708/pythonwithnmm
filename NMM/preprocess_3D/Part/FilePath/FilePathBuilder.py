from NMM.base.Object.Builder.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Part.FilePath.FilePath import FilePath
from NMM.base.Property.Implement.Path import Path
import os


class FilePathBuilder(AbstractConstructor):
    def build(self, root_path):
        file_path = FilePath()

        # work_path
        work_path = Path('work_path', self.path_cater(root_path))
        file_path.add_property(work_path)

        # preprocess mesh_path
        mesh_path = Path('mesh_path', self.path_cater(root_path, 'mesh'))
        file_path.add_property(mesh_path)

        # calculation geometry_path
        geometry_path = Path('geometry_path', self.path_cater(root_path, 'geometry'))
        file_path.add_property(geometry_path)

        # postprocess result_path
        result_path = Path('result_path', self.path_cater(root_path, 'result'))
        file_path.add_property(result_path)

        return file_path

    @staticmethod
    def path_cater(root_path, direction_path=''):
        # method to normalize and generate a absolute path
        return os.path.normpath(os.path.join(root_path, direction_path))

