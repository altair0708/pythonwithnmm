from NMM.base.Property.Property import Property


class CrackStatus(Property):
    def __init__(self, value):
        super(CrackStatus, self).__init__()
        self._name = 'CrackStatus'
        self._type = 'CrackStatus'
        self._value = value
