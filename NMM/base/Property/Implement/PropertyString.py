from NMM.base.Property.Property import Property


class PropertyString(Property):
    def __init__(self, value):
        super(PropertyString, self).__init__()
        self._type = 'PropertyString'
        self._name = ''
        self._value = value
