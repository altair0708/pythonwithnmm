from NMM.base.Property.Property import Property


class PropertyList(Property):
    def __init__(self, value):
        super(PropertyList, self).__init__()
        self._type = 'PropertyList'
        self._name = ''
        self._value = value
