from NMM.base.Part.Part import Part


class FilePath(Part):
    def __init__(self):
        super(FilePath, self).__init__()
        self._name = 'file_path'

    def get_path(self, path_name: str):
        return self.get_property(path_name).value
