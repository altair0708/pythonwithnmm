from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase import get_a_vtk_cell_grid, is_intersect, debug_write_file, clip_a_element, clip_a_surface, check_point_in_cell
from NMM.base.VTKBase.triangulate_crack_advance import triangle_and_iterate_grid
from NMM.base.VTKBase.intersection_line_with_triangle import intersect_line_with_triangle
from NMM.base.VTKBase.intersection_line_with_polyhedron import intersection_line_with_polyhedron
from NMM.base.VTKBase.intersection_line_with_polydata import intersection_line_with_polydata_cache, intersection_line_with_polydata
from NMM.base.VTKBase.iterate_polyhedron_edge import iterate_polyhedron_edges
from NMM.base.VTKBase.is_empty_cell import is_empty_cell
from NMM.base.VTKBase.intersection_box import intersection_box
from NMM.base.VTKBase.check_line_on_shell import check_line_on_shell


class CrackStatusUpdate(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid, crack_propagation: VtkGrid, manifold_element_grid: VtkGrid):
        super(CrackStatusUpdate, self).__init__()

        self.__crack_tip = crack_tip
        self.__crack_propagation = crack_propagation
        self.__manifold_element_grid = manifold_element_grid

        self.__crack_point_dict = {}
        self.__new_cracked_set = {}
        self.__crack_tip_set = {}

    def update(self):
        crack_propagation = self.__crack_propagation
        manifold_element = self.__manifold_element_grid

        # initial selection of crack element
        initial_crack_element = set()
        for each_element_id, each_manifold_element in enumerate(manifold_element):
            # check if empty cell
            if is_empty_cell(each_manifold_element):
                continue
            if intersection_box(crack_propagation.value, each_manifold_element):
                initial_crack_element.add(each_element_id)

        # select all crack propagation intersection cell
        crack_element = set()
        crack_point_dict = {}

        for each_id in initial_crack_element:
            each_manifold_element = manifold_element[each_id]
            edge_iteration = iterate_polyhedron_edges(each_manifold_element)

            crack_point_list = []
            for each_edge in edge_iteration:
                result, point = intersection_line_with_polydata(crack_propagation.value, each_edge)
                if result:
                    crack_point_list.append(point)
            if len(crack_point_list) > 0:
                crack_element.add(each_id)
                crack_point_dict.setdefault(each_id, []).extend(crack_point_list)

        crack_tip_element = set()
        for each_id in initial_crack_element:
            each_manifold_element = manifold_element[each_id]
            for each_crack_tip_id, each_crack_tip in enumerate(self.__crack_tip):
                if self.__crack_tip.get_cell_attribute('line_on_shell', each_crack_tip_id)[0] == 0:
                    if intersection_line_with_polyhedron(each_crack_tip, each_manifold_element):
                        crack_tip_element.add(each_id)
        # crack_element = set()
        # crack_point_dict = {}
        # for each_crack_polygon in self.__crack_propagation:
        #     for each_element_id, each_manifold_element in enumerate(self.__manifold_element_grid):
        #         # check if empty cell
        #         if is_empty_cell(each_manifold_element):
        #             continue
        #
        #         if is_intersect(each_crack_polygon, each_manifold_element):
        #             crack_element.add(each_element_id)
        #
        #             crack_point_count = 0
        #             crack_point_list = []
        #             crack_iteration = triangle_and_iterate_grid(each_crack_polygon)
        #             for each_crack_triangle in crack_iteration:
        #                 edge_iteration = iterate_polyhedron_edges(each_manifold_element)
        #                 for each_edge in edge_iteration:
        #                     result = intersect_line_with_triangle(each_edge, each_crack_triangle)
        #                     if result is not None:
        #                         crack_point_count = crack_point_count + 1
        #                         crack_point_list.append(result)
        #
        #             crack_point_dict.setdefault(each_element_id, []).extend(crack_point_list)
        #
        # # select all crack tip element
        # crack_tip_element = set()
        # for each_crack_tip_id, each_crack_tip in enumerate(self.__crack_tip):
        #     if self.__crack_tip.get_cell_attribute('line_on_shell', each_crack_tip_id)[0] == 0:
        #         for each_element_id, each_manifold_element in enumerate(self.__manifold_element_grid):
        #             # check if empty cell
        #             if is_empty_cell(each_manifold_element):
        #                 continue
        #
        #             if intersection_line_with_polyhedron(each_crack_tip, each_manifold_element):
        #                 crack_tip_element.add(each_element_id)

        cracked_element = crack_element - crack_tip_element
        # print(crack_element)
        # print(cracked_element)
        # print(crack_tip_element)

        new_cracked_element = set()
        for each_crack_tip_id in crack_tip_element:
            if self.__manifold_element_grid.get_cell_attribute('cracked', each_crack_tip_id)[0] < 7:
                self.__manifold_element_grid.set_cell_attribute('cracked', each_crack_tip_id, 7)
        for each_cracked_id in cracked_element:
            if self.__manifold_element_grid.get_cell_attribute('cracked', each_cracked_id)[0] < 8:
                self.__manifold_element_grid.set_cell_attribute('cracked', each_cracked_id, 8)
                new_cracked_element.add(each_cracked_id)

        self.__crack_point_dict = crack_point_dict
        self.__new_cracked_set = new_cracked_element
        self.__crack_tip_set = crack_tip_element

    @property
    def crack_point_dict(self):
        return self.__crack_point_dict

    @property
    def new_cracked_set(self):
        return self.__new_cracked_set

    @property
    def crack_tip_set(self):
        return self.__crack_tip_set



