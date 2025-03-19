from NMM.base.Property.Property import Property


class PropertyVector(Property):
    def __init__(self, value):
        super(PropertyVector, self).__init__()
        self._type = 'PropertyVector'
        self._name = ''
        self._value = value

    def __len__(self):
        return len(self._value)
