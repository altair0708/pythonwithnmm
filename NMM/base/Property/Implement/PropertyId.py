from NMM.base.Property.Property import Property


class PropertyId(Property):
    def __init__(self, value):
        super(PropertyId, self).__init__()
        self._type = 'PropertyId'
        self._name = ''
        self._value = value
