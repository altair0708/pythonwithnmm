from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from abc import ABC, abstractmethod


class FunctionAddAttribute(ABC):
    @staticmethod
    @abstractmethod
    def add_int_array(vtk_model: vtkUnstructuredGrid, attribute_name: str, tuple_dimensional: int, is_id=False):
        pass

    @staticmethod
    @abstractmethod
    def add_float_array(vtk_model: vtkUnstructuredGrid, attribute_name: str, tuple_dimensional: int, is_id=False):
        pass
