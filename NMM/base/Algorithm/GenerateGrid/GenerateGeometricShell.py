from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.VTKBase.extract_geometric_shell import extract_geometric_shell


class GenerateGeometricShell(AbstractAlgorithm):
    def __init__(self, geometric_tetrahedron, geometric_shell):
        self.__geometric_tetrahedron = geometric_tetrahedron
        self.__geometric_shell = geometric_shell

    def update(self, *args, **kwargs):
        entity = self.__geometric_tetrahedron.value
        self.__geometric_shell.value = extract_geometric_shell(entity)
