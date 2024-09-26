from NMM.base.Property.Property import Property


class VtkCell(Property):
    def __init__(self, id_value: int, grid_name: str):
        super(VtkCell, self).__init__()
        self._type = 'VtkCell'

        self._name = 'VtkCell'
        self._value = None

        self.__id_value = id_value
        self.__grid_name = grid_name

        self.generate_vtk_cell_grid()

    def generate_vtk_cell_grid(self):
        pass

