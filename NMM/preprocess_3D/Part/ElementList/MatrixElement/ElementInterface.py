from NMM.base.CompositeObject.CompositeObject import CompositeObject
from abc import ABC, abstractmethod


class AbstractElement(CompositeObject):
    def __init__(self):
        super(AbstractElement, self).__init__()
        self._name = 'abstract_element'

    @CompositeObject.name.setter
    def name(self, value):
        self._name = value
