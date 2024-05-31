from NMM.base.Property.PropertyInterface import AbstractProperty


class ObjectId(AbstractProperty):
    def __init__(self, value):
        self.__name = 'ID'
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
