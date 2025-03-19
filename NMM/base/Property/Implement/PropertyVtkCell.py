from NMM.base.Property.Property import Property


class PropertyVtkCell(Property):
    def __init__(self, id_value: int, grid_name: str):
        super(PropertyVtkCell, self).__init__()
        self._type = 'PropertyVtkCell'
        self._name = ''
        self._value = None
