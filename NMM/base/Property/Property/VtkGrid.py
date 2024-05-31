from NMM.base.Property.PropertyInterface import AbstractProperty
from NMM.base.VTKBase.Implement.VTKBase import VTKBase
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


class VtkGrid(AbstractProperty):
    def __init__(self, grid_name: str, file_name: str = None):
        self.__name = grid_name
        self.__type = 12  # vtkUnstructuredGrid store Model

        if file_name is None:
            self.__value = VTKBase.new_a_grid()
        else:
            self.__value = VTKBase.load_a_grid(file_name)

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    def add_attribute(self, attribute_name: str):
        pass
