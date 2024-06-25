from NMM.base.Part.Part import Part
from abc import ABC


class EntityList(Part, ABC):
    def __init__(self):
        super(EntityList, self).__init__()
        self._entity_list = []

    def add_entity(self, entity):
        self._entity_list.append(entity)

    def get_entity(self, id_value):
        return self._entity_list[id_value]

    def get_number(self):
        return len(self._entity_list)
