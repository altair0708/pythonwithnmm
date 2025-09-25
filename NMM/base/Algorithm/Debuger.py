from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.VTKBase.write_file import write_file


class Debuger(AbstractAlgorithm):
    def __init__(self):
        self.__debug_path = entrance_cache.get_item('debug_path_Path').value

    def update(self, u_grid, file_name: str):
        path = self.__debug_path + '/' + file_name
        write_file(u_grid, path)
