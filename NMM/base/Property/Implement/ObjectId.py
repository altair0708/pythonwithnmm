from NMM.base.Property.Property import Property


class ObjectId(Property):
    def __init__(self, value):
        super(ObjectId, self).__init__()
        self._type = 'ID'

        self._name = 'ID'
        self._value = value
