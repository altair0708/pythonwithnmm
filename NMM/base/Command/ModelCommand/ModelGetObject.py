from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Model.Model import PreprocessModel


class ModelGetObject(AbstractCommand):
    def __init__(self, object_name):
        self.__object_name = object_name

    def execute(self):
        model = PreprocessModel()

