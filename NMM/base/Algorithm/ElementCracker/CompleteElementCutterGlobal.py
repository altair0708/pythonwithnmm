from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.VTKBase import get_a_vtk_cell_grid, is_intersect, debug_write_file, clip_a_element, clip_a_surface, check_point_in_cell
from NMM.base.CacheBase import entrance_cache, relationship_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement import VtkGrid
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


class CompleteElementCutter(AbstractAlgorithm):
    def __init__(self, id_value: int, manifold_element: VtkGrid, origin, normal, angle_algorithm=None):
        self.__id_value = id_value
        self.__origin = origin
        assert len(normal) == 3
        self.__normal = normal

        self.__manifold_element = manifold_element
        self.__mathematics_point = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover = entrance_cache.get_item('new_cover_VtkGrid')
        self.__new_element = entrance_cache.get_item('new_element_VtkGrid')

        self.__crack_surface = entrance_cache.get_item('crack_surface_VtkGrid')
        self.__element_surface = entrance_cache.get_item('element_surface_VtkGrid')
        self.__new_surface = entrance_cache.get_item('new_surface_VtkGrid')
        self.__crack_edge = entrance_cache.get_item('crack_edge_VtkGrid')

        self.__angle_algorithm = angle_algorithm

    def update(self, *args, **kwargs):
        element_id = self.__id_value
        origin = self.__origin
        normal = self.__normal
        element = self.__manifold_element[element_id]

        # geometric calculation of cut an element
        try:
            crack_surface, new_element_0, new_element_1 = clip_a_element(element, origin, normal)
        except AssertionError:
            return

        if self.__angle_algorithm is not None:
            self.__angle_algorithm.crack_surface = crack_surface
            self.__angle_algorithm.update()
            angle = self.__angle_algorithm.angle
            if angle < 90:
                return

        # delete cell
        self.__manifold_element.delete_cell(element_id)

        # manifold element attribute
        self.__manifold_element.set_attribute('cracked', element_id, 9)

        # crack surface attribute
        temp_id = self.__crack_surface.get_cell_number()
        relationship_cache.add_item('element', element_id, 'cracksurface', temp_id)
        self.__crack_surface.add_item(crack_surface)
        self.__crack_surface.set_attribute('cell_id', temp_id, temp_id)

        # new element attribute
        element_number = global_variable_cache.get_item('element_number')
        new_element_number = global_variable_cache.get_item('new_element_number')
        total_number = element_number + new_element_number
        global_variable_cache.add_item('new_element_number', new_element_number + 2)
        assert new_element_number == self.__new_element.get_cell_number()

        new_element_0_id = self.__new_element.get_cell_number()

        # add new_element_0_id to global_variable
        new_element_list = global_variable_cache.get_item('new_element_id')
        new_element_list.append(new_element_0_id)
        global_variable_cache.add_item('new_element_id', new_element_list)

        relationship_cache.add_item('element', element_id, 'newelement', new_element_0_id)
        self.__new_element.add_item(new_element_0)
        self.__new_element.set_attribute('cell_id', new_element_0_id, new_element_0_id)
        self.__new_element.set_attribute('total_id', new_element_0_id, total_number)

        new_element_1_id = self.__new_element.get_cell_number()

        # add new_element_0_id to global_variable
        new_element_list = global_variable_cache.get_item('new_element_id')
        new_element_list.append(new_element_1_id)
        global_variable_cache.add_item('new_element_id', new_element_list)

        relationship_cache.add_item('element', element_id, 'newelement', new_element_1_id)
        self.__new_element.add_item(new_element_1)
        self.__new_element.set_attribute('cell_id', new_element_1_id, new_element_1_id)
        self.__new_element.set_attribute('total_id', new_element_1_id, total_number + 1)

        # generate new surface
        relationship_list = relationship_cache.get_item(name_0='element', name_1='surface', id_0=element_id,
                                                        id_1=None)
        for each_relationship in relationship_list:
            surface_id = each_relationship['surface']
            if self.__element_surface.get_attribute('cracked', surface_id)[0] == 9:
                continue
            element_surface: vtkUnstructuredGrid = self.__element_surface[surface_id]

            crack_edge, new_surface_0, new_surface_1 = clip_a_surface(element_surface, origin, normal)
            if crack_edge is None:
                continue

            # # potential crack element, set attribute 'cracked' 8.
            # adjacent_relationship = relationship_cache.get_item(name_0='element', name_1='surface', id_0=None,
            #                                                 id_1=surface_id)
            # for temp_relationship in adjacent_relationship:
            #     adjacent_element_id = temp_relationship['element']
            #     if adjacent_element_id == element_id:
            #         continue
            #     if self.__manifold_element.get_attribute('cracked', adjacent_element_id)[0] == 9:
            #         continue
            #     self.__manifold_element.set_attribute('cracked', adjacent_element_id, 8)

            # element surface attribute
            self.__element_surface.set_attribute('cracked', surface_id, 9)

            # crack edge attribute
            temp_id = self.__crack_edge.get_cell_number()
            relationship_cache.add_item('surface', surface_id, 'crackedge', temp_id)
            self.__crack_edge.add_item(crack_edge)
            self.__crack_edge.set_attribute('cell_id', temp_id, temp_id)

            # new surface
            temp_id = self.__new_surface.get_cell_number()
            relationship_cache.add_item('surface', surface_id, 'newsurface', temp_id)
            self.__new_surface.add_item(new_surface_0)
            self.__new_surface.set_attribute('cell_id', temp_id, temp_id)

            temp_id = self.__new_surface.get_cell_number()
            relationship_cache.add_item('surface', surface_id, 'newsurface', temp_id)
            self.__new_surface.add_item(new_surface_1)
            self.__new_surface.set_attribute('cell_id', temp_id, temp_id)

        # generate new cover
        relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None,
                                                        id_1=element_id)
        for each_relationship in relationship_list:
            cover_id = each_relationship['cover']

            real_cover_point = self.__mathematics_point[cover_id]
            virtual_cover_point = self.__mathematics_point[cover_id]

            # cracked mathematics point
            if self.__mathematics_point.get_attribute('cracked', cover_id)[0] == 9:
                # cracked cover
                cover_relationship_list = relationship_cache.get_item(name_0='cover', name_1='newcover', id_0=cover_id,
                                                                      id_1=None)
                assert len(cover_relationship_list) == 2

                for each_cover in cover_relationship_list:
                    new_cover_id = each_cover['newcover']
                    if self.__new_cover.get_attribute('real', new_cover_id)[0] == 1:
                        real_cover_id = each_cover['newcover']
                        if check_point_in_cell(real_cover_point, new_element_0):
                            relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement',
                                                        id_1=new_element_0_id)
                        elif check_point_in_cell(real_cover_point, new_element_1):
                            relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement',
                                                        id_1=new_element_1_id)

                    elif self.__new_cover.get_attribute('real', new_cover_id)[0] == 0:
                        virtual_cover_id = each_cover['newcover']
                        if check_point_in_cell(virtual_cover_point, new_element_0):
                            relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement',
                                                        id_1=new_element_1_id)
                        elif check_point_in_cell(virtual_cover_point, new_element_1):
                            relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement',
                                                        id_1=new_element_0_id)
                    else:
                        raise Exception('Attribute value error: real!!!!')

            elif self.__mathematics_point.get_attribute('cracked', cover_id)[0] == -1:
                cover_number = global_variable_cache.get_item('cover_number')
                new_cover_number = global_variable_cache.get_item('new_cover_number')
                total_cover_number = cover_number + (new_cover_number / 2)
                global_variable_cache.add_item('new_cover_number', new_cover_number + 2)
                assert new_cover_number == self.__new_cover.get_cell_number()

                # not cracked cover
                # mathematics point attribute
                self.__mathematics_point.set_attribute('cracked', cover_id, 9)

                # new cover attribute: real cover
                real_cover_id = self.__new_cover.get_cell_number()

                new_cover_list = global_variable_cache.get_item('new_cover_id')
                new_cover_list.append(real_cover_id)
                global_variable_cache.add_item('new_cover_id', new_cover_list)

                relationship_cache.add_item('cover', cover_id, 'newcover', real_cover_id)
                self.__new_cover.add_item(real_cover_point)
                self.__new_cover.set_attribute('cell_id', real_cover_id, real_cover_id)
                self.__new_cover.set_attribute('real', real_cover_id, 1)  # real cover
                self.__new_cover.set_attribute('total_id', real_cover_id, cover_id)

                # new cover attribute: virtual cover
                virtual_cover_id = self.__new_cover.get_cell_number()

                new_cover_list = global_variable_cache.get_item('new_cover_id')
                new_cover_list.append(virtual_cover_id)
                global_variable_cache.add_item('new_cover_id', new_cover_list)

                relationship_cache.add_item('cover', cover_id, 'newcover', virtual_cover_id)
                self.__new_cover.add_item(virtual_cover_point)
                self.__new_cover.set_attribute('cell_id', virtual_cover_id, virtual_cover_id)
                self.__new_cover.set_attribute('real', virtual_cover_id, 0)  # virtual cover
                self.__new_cover.set_attribute('total_id', virtual_cover_id, total_cover_number)

                if check_point_in_cell(real_cover_point, new_element_0):
                    relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement',
                                                id_1=new_element_0_id)
                    relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement',
                                                id_1=new_element_1_id)
                else:
                    relationship_cache.add_item(name_0='newcover', id_0=virtual_cover_id, name_1='newelement',
                                                id_1=new_element_0_id)
                    relationship_cache.add_item(name_0='newcover', id_0=real_cover_id, name_1='newelement',
                                                id_1=new_element_1_id)
            else:
                raise Exception(
                    f"Attribute value error: cracked{self.__mathematics_point.get_attribute('cracked', cover_id)[0]}!!!")
