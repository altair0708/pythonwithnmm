from NMM.base.Property.Property import Property


class Path(Property):
    def __init__(self, path_name, path):
        super(Path, self).__init__()

        assert type(path_name) is str
        self._name = path_name

        self._type = 'Path'

        assert type(path) is str
        self._value = path

