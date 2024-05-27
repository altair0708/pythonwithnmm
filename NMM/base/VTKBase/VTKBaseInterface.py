from abc import ABC, abstractmethod
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell


class AbstractVTKBase(ABC):
    @staticmethod
    @abstractmethod
    def insert_a_vtk_cell(vtk_model: vtkUnstructuredGrid, vtk_cell: vtkCell):
        pass

    @staticmethod
    @abstractmethod
    def insert_a_grid(vtk_model: vtkUnstructuredGrid, new_vtk_model: vtkUnstructuredGrid):
        pass
