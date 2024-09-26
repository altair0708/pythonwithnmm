from NMM.base.Property.Property import Property


class Relationship(Property):
    @classmethod
    def generate_by_dict(cls, relationship_name: str, relationship_dict: dict):
        entity_name = relationship_name.split('_')
        id_0 = relationship_dict[entity_name[0]]
        id_1 = relationship_dict[entity_name[1]]
        return Relationship(relationship_name, id_0, id_1)

    def __init__(self, relationship_name: str, id_0: int or None, id_1: int or None):
        super(Relationship, self).__init__()
        self._type = 'Relationship'

        self._name = relationship_name
        assert len(relationship_name.split('_')) == 2

        self._value = {relationship_name.split('_')[0]: id_0,
                       relationship_name.split('_')[1]: id_1}

    def __getitem__(self, entity_name: str):
        return self._value[entity_name]
