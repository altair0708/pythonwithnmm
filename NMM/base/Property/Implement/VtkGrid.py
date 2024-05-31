from NMM.base.Property.Property import Property
from NMM.base.VTKBase.Implement.VTKBase import VTKBase


class VtkGrid(Property):
    def __init__(self, grid_name: str, file_name: str = None):
        super(VtkGrid, self).__init__()
        self._name = grid_name
        self._type = 'VtkGrid'

        if file_name is None:
            self._value = VTKBase.new_a_grid()
        else:
            self._value = VTKBase.load_a_grid(file_name)

    def add_attribute(self, attribute_name):
        pass
