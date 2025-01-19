from NMM.base.Property.Property import Property


class PropertyMap(Property):
    def __init__(self, value):
        super(PropertyMap, self).__init__()
        self._type = 'PropertyMap'
        self._name = ''
        self._value = value
