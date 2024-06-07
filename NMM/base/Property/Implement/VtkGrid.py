from NMM.base.Property.Property import Property
from NMM.base.VTKBase.Implement.VTKBase import VTKBase
from NMM.base.VTKBase import get_grid_by_cell_type, generate_cover_grid, add_attribute, write_file


class VtkGrid(Property):
    def __init__(self, grid_name: str, file_name: str = None):
        super(VtkGrid, self).__init__()
        self._name = grid_name
        self._type = 'VtkGrid'

        if file_name is None:
            self._value = VTKBase.new_a_grid()
        else:
            self._value = VTKBase.load_a_grid(file_name)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vtk_grid):
        self._value = vtk_grid

    def add_attribute(self, attribute_name):
        add_attribute(self._value, attribute_name)

    def extract_by_cell_type(self, geometric_name: str):
        return get_grid_by_cell_type(self._value, geometric_name)

    def extract_mathematics_cover(self, cover_name):
        return generate_cover_grid(self._value, cover_name)

    def write_file(self, file_name):
        write_file(self._value, file_name)
