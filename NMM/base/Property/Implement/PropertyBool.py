from NMM.base.Property.Property import Property


class PropertyBool(Property):
    def __init__(self, value):
        super(PropertyBool, self).__init__()
        self._type = 'PropertyBool'
        self._name = ''
        self._value = value
