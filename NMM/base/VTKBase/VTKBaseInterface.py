from abc import ABC, abstractmethod
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell


class AbstractVTKBase(ABC):
    @staticmethod
    @abstractmethod
    def insert_a_grid(vtk_model: vtkUnstructuredGrid, new_vtk_model: vtkUnstructuredGrid):
        pass

    @staticmethod
    @abstractmethod
    def insert_a_grid_0(vtk_model: vtkUnstructuredGrid, new_vtk_model: vtkUnstructuredGrid):
        pass

    @staticmethod
    @abstractmethod
    def get_a_vtk_cell_grid(vtk_model: vtkUnstructuredGrid, id_value: int):
        pass
