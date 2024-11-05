from NMM.base.Object.NmmObjectBase import NmmObjectBase
from abc import ABC, abstractmethod


class AbstractElement(NmmObjectBase):
    def __init__(self):
        super(AbstractElement, self).__init__()
        self._name = 'abstract_element'

    @NmmObjectBase.name.setter
    def name(self, value):
        self._name = value
