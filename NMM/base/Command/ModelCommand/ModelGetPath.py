from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.FilePath.FilePath import FilePath


class ModelGetPath(AbstractCommand):
    def __init__(self, path_name, path_part: FilePath):
        self.__path_name = path_name
        self.__path_part = path_part

    def execute(self):
        return self.__path_part.get_path(self.__path_name)

