from NMM.base.CompositeObject.CompositeObject import CompositeObject
from abc import ABC


class Part(CompositeObject, ABC):
    def __init__(self):
        super(Part, self).__init__()
        self._type = 'Part'
