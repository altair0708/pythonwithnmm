from abc import ABC, abstractmethod
from NMM.crack_3D.CrackEdgeBase3D import CrackEdge3D
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from typing import List


class AbstractCrackType(ABC):
    @abstractmethod
    def calculate_origin_point_normal_vector(self, crack_edge_cell_list: List[CrackEdge3D], crack_edge_grid: vtkUnstructuredGrid, max_strain):
        pass
