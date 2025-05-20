from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Algorithm.ElementCracker.CompleteElementCutter import CompleteElementCutter
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.generate_crack_grid.generate_crack_grid import generate_crack_grid
from NMM.base.VTKBase import get_a_vtk_cell_grid, is_intersect, debug_write_file, clip_a_element, clip_a_surface, check_point_in_cell
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints


class InitialCrackGenerator(AbstractAlgorithm):
    def __init__(self, initial_crack_grid: VtkGrid, manifold_element_grid: VtkGrid):
        super(InitialCrackGenerator, self).__init__()

        self.__initial_crack_grid = initial_crack_grid
        self.__manifold_element_grid = manifold_element_grid

    def update(self):

        # assert self.__initial_crack_grid.get_cell_number() == 1
        # crack_polygon_grid: vtkUnstructuredGrid = self.__initial_crack_grid[0]

        for each_crack_polygon_grid in self.__initial_crack_grid:
            # normal vector, origin point
            normal = [0, 0, 0]
            temp_polygon_points: vtkPoints = each_crack_polygon_grid.GetPoints()
            vtkPolygon.ComputeNormal(temp_polygon_points, normal)
            origin = temp_polygon_points.GetPoint(0)

            # debug_write_file(crack_polygon_grid, 'crack.vtu')
            for each_id, each_manifold_element in enumerate(self.__manifold_element_grid):
                if is_intersect(each_crack_polygon_grid, each_manifold_element):
                    cutter = CompleteElementCutter(each_id, self.__manifold_element_grid, origin, normal)
                    cutter.update()

