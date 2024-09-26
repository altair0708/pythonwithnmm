from NMM.base.Property.Property import Property
import shutil
import os


class Path(Property):
    def __init__(self, path_name, path):
        super(Path, self).__init__()
        self._type = 'Path'

        assert type(path_name) is str
        self.name = path_name


        assert type(path) is str
        self._value = path

    def mkdir(self):
        if os.path.exists(self._value):
            shutil.rmtree(self._value)
        os.mkdir(self._value)

