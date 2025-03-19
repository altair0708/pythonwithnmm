from abc import abstractmethod
from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder


class AbstractMatrixElementBuilder(AbstractElementBuilder):
    @abstractmethod
    def set_simple_properties(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_vertexes(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_patches(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_special_points(self, *args, **kwargs):
        pass


