from NMM.base.GeometricEntity.Property.PropertyInterface import AbstractProperty


class CrackStatus(AbstractProperty):
    def __init__(self, value):
        self.__name = 'CrackStatus'
        self.__type = 1  # int
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, temp_value):
        self.__value = temp_value
