from NMM.base.CompositeObject.CompositeObject import CompositeObject
from abc import ABC


class Model(CompositeObject, ABC):
    def __init__(self):
        super(Model, self).__init__()
        self._type = 'Model'

