from NMM.base.Property.Property import Property


class PropertyMatrix(Property):
    def __init__(self, value):
        super(PropertyMatrix, self).__init__()
        self._type = 'PropertyMatrix'
        self._name = ''
        self._value = value
