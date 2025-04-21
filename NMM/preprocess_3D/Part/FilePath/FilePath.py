from NMM.base.Part.Part import Part
from NMM.base.Property.Implement.Path import Path
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
import shutil
import os


class FilePath(Part):
    def __init__(self):
        super(FilePath, self).__init__()
        self.name = 'file_path'

    def get_path(self, path_name: str):
        return self.get_property(path_name).value

    @staticmethod
    def path_cater(root_path, direction_path=''):
        # method to normalize and generate a absolute path
        return os.path.normpath(os.path.join(root_path, direction_path))

    @staticmethod
    def mkdir(path_name: str):
        if not os.path.exists(path_name):
            os.mkdir(path_name)

    def generate_output_result_path(self, grid_name: str):
        result_path: str = self.get_property('result_path').value
        folder_path_str = self.path_cater(result_path, grid_name)

        self.mkdir(folder_path_str)

        time_step = str(global_variable_cache.get_item('time_step')).zfill(5)
        file_name = f'{grid_name}_{time_step}.vtu'

        return self.path_cater(folder_path_str, file_name)

