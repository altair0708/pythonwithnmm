from NMM.base.Property.Property import Property


class Relationship(Property):
    def __init__(self, relationship_name: str, id_0: int, id_1: int):
        super(Relationship, self).__init__()
        self._name = relationship_name
        assert len(relationship_name.split('_')) == 2

        self._type = 'Relationship'
        self._value = {relationship_name.split('_')[0]: id_0,
                       relationship_name.split('_')[1]: id_1}
