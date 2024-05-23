from abc import ABC, abstractmethod


class AbstractCrackObject(ABC):
    @abstractmethod
    @property
    def id(self):
        pass

    @abstractmethod
    @property
    def vtk_cell(self):
        pass
