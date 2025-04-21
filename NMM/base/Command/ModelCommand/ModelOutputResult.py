from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase import entrance_cache
from NMM.preprocess_3D.Part.FilePath.FilePath import FilePath


class ModelOutputResult(AbstractCommand):
    def __init__(self, grid_name: str):
        self.__grid_name = grid_name

    def execute(self):
        vtk_grid: VtkGrid = entrance_cache.get_item(f'{self.__grid_name}_VtkGrid')
        file_path_part: FilePath = entrance_cache.get_item('file_path_Part')
        output_path = file_path_part.generate_output_result_path(self.__grid_name)
        vtk_grid.write_file(output_path)
