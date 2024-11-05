from NMM.base.Object.NmmObjectBase import NmmObjectBase
from abc import ABC, abstractmethod


class AbstractAlgorithm(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass
