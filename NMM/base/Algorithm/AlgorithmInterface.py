from NMM.base.Object.NmmObjectBase import NmmObjectBase
from abc import ABC, abstractmethod


class AbstractInterface(NmmObjectBase, ABC):
    @abstractmethod
    def update(self, *args):
        pass
