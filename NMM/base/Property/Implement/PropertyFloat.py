from NMM.base.Property.Property import Property


class PropertyFloat(Property):
    def __init__(self, value):
        super(PropertyFloat, self).__init__()
        self._type = 'PropertyFloat'
        self._name = ''
        self._value = value
