from abc import ABC, abstractmethod


class AbstractElementBuilder(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_element(self):
        pass

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
