from NMM.base.Property.Property import Property


class PropertyInteger(Property):
    def __init__(self, value):
        super(PropertyInteger, self).__init__()
        self._type = 'PropertyInteger'
        self._name = ''
        self._value = value
