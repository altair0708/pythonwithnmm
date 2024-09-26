from NMM.base.Algorithm.AlgorithmInterface import AbstractInterface
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.generate_crack_grid.generate_crack_grid import generate_crack_grid
from NMM.base.VTKBase import get_a_vtk_cell_grid, is_intersect, write_file, clip_a_element, clip_a_surface
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints


class InitialCrackGenerator(AbstractInterface):
    def __init__(self, initial_crack_grid: VtkGrid,
                 new_cover_grid: VtkGrid, new_element_grid: VtkGrid, new_surface_grid: VtkGrid,
                 mathematics_point_grid: VtkGrid, manifold_element_grid: VtkGrid, element_surface_grid: VtkGrid,
                 crack_surface_grid: VtkGrid, crack_edge_grid: VtkGrid):
        super(InitialCrackGenerator, self).__init__()

        self.__initial_crack_grid = initial_crack_grid
        self.__new_cover_grid = new_cover_grid
        self.__new_element_grid = new_element_grid
        self.__new_surface_grid = new_surface_grid
        self.__mathematics_point_grid = mathematics_point_grid
        self.__manifold_element_grid = manifold_element_grid
        self.__element_surface_grid = element_surface_grid
        self.__crack_surface_grid = crack_surface_grid
        self.__crack_edge_grid = crack_edge_grid

    def update(self):

        assert self.__initial_crack_grid.get_cell_number() == 1
        crack_polygon_grid: vtkUnstructuredGrid = self.__initial_crack_grid[0]

        # normal vector, origin point
        normal = [0, 0, 0]
        temp_polygon_points: vtkPoints = crack_polygon_grid.GetPoints()
        vtkPolygon.ComputeNormal(temp_polygon_points, normal)
        origin = temp_polygon_points.GetPoint(0)

        for each_id, each_manifold_element in enumerate(self.__manifold_element_grid):
            if is_intersect(crack_polygon_grid, each_manifold_element):
                try:
                    crack_surface, new_element_0, new_element_1 = clip_a_element(each_manifold_element, origin, normal)
                except AssertionError:
                    continue

                relationship_cache.add_item('element', each_id, 'cracksurface', self.__crack_surface_grid.get_cell_number())
                self.__crack_surface_grid.add_item(crack_surface)
                relationship_cache.add_item('element', each_id, 'newelement', self.__new_element_grid.get_cell_number())
                self.__new_element_grid.add_item(new_element_0)
                relationship_cache.add_item('element', each_id, 'newelement', self.__new_element_grid.get_cell_number())
                self.__new_element_grid.add_item(new_element_1)

                relationship_list = relationship_cache.get_item(name_0='element', name_1='surface', id_0=each_id, id_1=None)
                for each_relationship in relationship_list:
                    surface_id = each_relationship['surface']
                    each_element_surface: vtkUnstructuredGrid = self.__element_surface_grid[surface_id]
                    try:
                        crack_edge, new_surface_0, new_surface_1 = clip_a_element(each_element_surface, origin, normal)
                    except AssertionError:
                        continue

                    relationship_cache.add_item('surface', surface_id, 'crackedge', self.__crack_edge_grid.get_cell_number())
                    self.__crack_edge_grid.add_item(crack_edge)
                    relationship_cache.add_item('surface', surface_id, 'newsurface', self.__new_surface_grid.get_cell_number())
                    self.__new_surface_grid.add_item(new_surface_0)
                    relationship_cache.add_item('surface', surface_id, 'newsurface', self.__new_surface_grid.get_cell_number())
                    self.__new_surface_grid.add_item(new_surface_1)

