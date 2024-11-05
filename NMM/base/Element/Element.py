from NMM.base.CompositeObject.CompositeObject import CompositeObject
from abc import ABC
import warnings


class Element(CompositeObject, ABC):
    def __init__(self):
        warnings.warn('Deprecation class: Element', DeprecationWarning)
        super(Element, self).__init__()
        self._relationship_list = []

    def add_relationship(self, relationship):
        self._relationship_list.append(relationship)

    def get_relationship(self, id_value):
        return self._relationship_list[id_value]

