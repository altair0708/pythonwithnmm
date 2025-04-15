from NMM.base.Property.Property import Property
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


class PropertyVtkCell(Property):
    def __init__(self, vtk_cell: vtkUnstructuredGrid):
        super(PropertyVtkCell, self).__init__()
        self._type = 'PropertyVtkCell'
        self._name = ''
        self._value = vtk_cell
