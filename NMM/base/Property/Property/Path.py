from NMM.base.Property.PropertyInterface import AbstractProperty


class Path(AbstractProperty):
    def __init__(self, path_name, path):

        assert type(path_name) is str
        self.__name = path_name

        self.__type = 21  # string of path

        assert type(path) is str
        self.__value = path

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value
