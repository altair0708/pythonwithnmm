from abc import ABC, abstractmethod
from NMM.GlobalVariable import DataStructure


class AbstractObjectBuilder(ABC):
    @abstractmethod
    def builder(self, id_value: int, data_structure: DataStructure):
        pass
