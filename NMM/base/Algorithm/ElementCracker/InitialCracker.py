from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.generate_crack_grid.generate_crack_grid import generate_crack_grid
from NMM.base.VTKBase import get_a_vtk_cell_grid, is_intersect, debug_write_file, clip_a_element, clip_a_surface, check_point_in_cell
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon
from vtkmodules.vtkCommonCore import vtkPoints


class InitialCrackGenerator(AbstractAlgorithm):
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

        # debug_write_file(crack_polygon_grid, 'crack.vtu')
        for each_id, each_manifold_element in enumerate(self.__manifold_element_grid):
            if is_intersect(crack_polygon_grid, each_manifold_element):
                # try:
                #     crack_surface, new_element_0, new_element_1 = clip_a_element(each_manifold_element, origin, normal)
                # except AssertionError:
                #     continue
                crack_surface, new_element_0, new_element_1 = clip_a_element(each_manifold_element, origin, normal)

                # delete cell
                self.__manifold_element_grid.delete_cell(each_id)

                # manifold element attribute
                self.__manifold_element_grid.set_attribute('cracked', each_id, 9)

                # crack surface attribute
                temp_id = self.__crack_surface_grid.get_cell_number()
                relationship_cache.add_item('element', each_id, 'cracksurface', temp_id)
                self.__crack_surface_grid.add_item(crack_surface)
                self.__crack_surface_grid.set_attribute('cell_id', temp_id, temp_id)

                # new element attribute
                element_number = global_variable_cache.get_item('element_number')
                new_element_number = global_variable_cache.get_item('new_element_number')
                total_number = element_number + new_element_number
                global_variable_cache.add_item('new_element_number', new_element_number + 2)
                assert new_element_number == self.__new_element_grid.get_cell_number()

                new_element_0_id = self.__new_element_grid.get_cell_number()
                relationship_cache.add_item('element', each_id, 'newelement', new_element_0_id)
                self.__new_element_grid.add_item(new_element_0)
                self.__new_element_grid.set_attribute('cell_id', new_element_0_id, new_element_0_id)
                self.__new_element_grid.set_attribute('total_id', new_element_0_id, total_number)

                new_element_1_id = self.__new_element_grid.get_cell_number()
                relationship_cache.add_item('element', each_id, 'newelement', new_element_1_id)
                self.__new_element_grid.add_item(new_element_1)
                self.__new_element_grid.set_attribute('cell_id', new_element_1_id, new_element_1_id)
                self.__new_element_grid.set_attribute('total_id', new_element_1_id, total_number + 1)

                # generate new surface
                relationship_list = relationship_cache.get_item(name_0='element', name_1='surface', id_0=each_id,
                                                                id_1=None)
                for each_relationship in relationship_list:
                    surface_id = each_relationship['surface']
                    if self.__element_surface_grid.get_attribute('cracked', surface_id)[0] == 9:
                        continue
                    element_surface: vtkUnstructuredGrid = self.__element_surface_grid[surface_id]

                    # try:
                    #     crack_edge, new_surface_0, new_surface_1 = clip_a_surface(element_surface, origin, normal)
                    # except AssertionError:
                    #     continue
                    crack_edge, new_surface_0, new_surface_1 = clip_a_surface(element_surface, origin, normal)
                    if crack_edge is None:
                        continue

                    # element surface attribute
                    self.__element_surface_grid.set_attribute('cracked', surface_id, 9)

                    # crack edge attribute
                    temp_id = self.__crack_edge_grid.get_cell_number()
                    relationship_cache.add_item('surface', surface_id, 'crackedge', temp_id)
                    self.__crack_edge_grid.add_item(crack_edge)
                    self.__crack_edge_grid.set_attribute('cell_id', temp_id, temp_id)

                    # new surface
                    temp_id = self.__new_surface_grid.get_cell_number()
                    relationship_cache.add_item('surface', surface_id, 'newsurface', temp_id)
                    self.__new_surface_grid.add_item(new_surface_0)
                    self.__new_surface_grid.set_attribute('cell_id', temp_id, temp_id)

                    temp_id = self.__new_surface_grid.get_cell_number()
                    relationship_cache.add_item('surface', surface_id, 'newsurface', temp_id)
                    self.__new_surface_grid.add_item(new_surface_1)
                    self.__new_surface_grid.set_attribute('cell_id', temp_id, temp_id)

                # generate new cover
                relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None,
                                                                id_1=each_id)
                for each_relationship in relationship_list:
                    cover_id = each_relationship['cover']

                    real_cover_point = self.__mathematics_point_grid[cover_id]
                    virtual_cover_point = self.__mathematics_point_grid[cover_id]

                    # cracked mathematics point
                    if self.__mathematics_point_grid.get_attribute('cracked', cover_id)[0] == 9:
                        # cracked cover
                        cover_relationship_list = relationship_cache.get_item(name_0='cover', name_1='newcover', id_0=cover_id,
                                                                              id_1=None)
                        assert len(cover_relationship_list) == 2

                        for each_cover in cover_relationship_list:
                            new_cover_id = each_cover['newcover']
                            if self.__new_cover_grid.get_attribute('real', new_cover_id)[0] == 1:
                                real_cover_id = each_cover['newcover']
                                if check_point_in_cell(real_cover_point, new_element_0):
                                    relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement', id_1=new_element_0_id)
                                elif check_point_in_cell(real_cover_point, new_element_1):
                                    relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement', id_1=new_element_1_id)

                            elif self.__new_cover_grid.get_attribute('real', new_cover_id)[0] == 0:
                                virtual_cover_id = each_cover['newcover']
                                if check_point_in_cell(virtual_cover_point, new_element_0):
                                    relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement', id_1=new_element_1_id)
                                elif check_point_in_cell(virtual_cover_point, new_element_1):
                                    relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement', id_1=new_element_0_id)
                            else:
                                raise Exception('Attribute value error: real!!!!')

                    elif self.__mathematics_point_grid.get_attribute('cracked', cover_id)[0] == -1:
                        cover_number = global_variable_cache.get_item('cover_number')
                        new_cover_number = global_variable_cache.get_item('new_cover_number')
                        total_cover_number = cover_number + (new_cover_number / 2)
                        global_variable_cache.add_item('new_cover_number', new_cover_number + 2)
                        assert new_cover_number == self.__new_cover_grid.get_cell_number()

                        # not cracked cover
                        # mathematics point attribute
                        self.__mathematics_point_grid.set_attribute('cracked', cover_id, 9)

                        # new cover attribute: real cover
                        real_cover_id = self.__new_cover_grid.get_cell_number()
                        relationship_cache.add_item('cover', cover_id, 'newcover', real_cover_id )
                        self.__new_cover_grid.add_item(real_cover_point)
                        self.__new_cover_grid.set_attribute('cell_id', real_cover_id, real_cover_id)
                        self.__new_cover_grid.set_attribute('real', real_cover_id, 1)  # real cover
                        self.__new_cover_grid.set_attribute('total_id', real_cover_id, cover_id)

                        # new cover attribute: virtual cover
                        virtual_cover_id = self.__new_cover_grid.get_cell_number()
                        relationship_cache.add_item('cover', cover_id, 'newcover', virtual_cover_id)
                        self.__new_cover_grid.add_item(virtual_cover_point)
                        self.__new_cover_grid.set_attribute('cell_id', virtual_cover_id, virtual_cover_id)
                        self.__new_cover_grid.set_attribute('real', virtual_cover_id, 0)  # virtual cover
                        self.__new_cover_grid.set_attribute('total_id', virtual_cover_id, total_cover_number)

                        if check_point_in_cell(real_cover_point, new_element_0):
                            relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement', id_1=new_element_0_id)
                            relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement', id_1=new_element_1_id)
                        else:
                            relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement', id_1=new_element_0_id)
                            relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement', id_1=new_element_1_id)
                    else:
                        raise Exception(f"Attribute value error: cracked{self.__mathematics_point_grid.get_attribute('cracked', cover_id)[0]}!!!")


