from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.SimplexIntegralBase.polyhedron_integral import once_integration
from NMM.base.Algorithm.Debuger import Debuger
from NMM.base.VTKBase.empty_to_polyhedron import empty_to_polyhedron
import numpy as np


class GeometricPrecondition(AbstractAlgorithm):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')

        cover_number = global_variable_cache.get_item('cover_number')
        new_cover_number = global_variable_cache.get_item('new_cover_number')
        total_cover_number = 3 * int(cover_number + (new_cover_number / 2))

        self.__precondition = np.ones(total_cover_number)
        self.__new_cover_map = {}

    @property
    def precondition(self):
        return self.__precondition

    def update(self, *args, **kwargs):
        manifold_element = self.__manifold_element
        new_element = self.__new_element
        new_cover = self.__new_cover
        precondition = self.__precondition

        new_element_number = new_element.get_cell_number()
        for each_id in range(new_element_number):

            vertex_list = []
            vertex_id = new_element.get_cell_point_id(each_id)
            for each_vertex_id in vertex_id:
                vertex_list.append(new_element.get_point_coordinate(each_vertex_id))

            temp = relationship_cache.get_item('newcover', 'newelement', id_0=None, id_1=each_id)
            assert len(temp) == 4
            cover_id_list = [each_relation['newcover'] for each_relation in temp]

            cover_list = []
            cover_total_id_list = []
            for each_cover_id in cover_id_list:
                cover_list.append(new_cover.get_point_coordinate(each_cover_id))
                cover_total_id_list.append(new_cover.get_cell_attribute('total_id', each_cover_id))

            delta_matrix = np.c_[np.ones((4, 1), dtype=np.float64), np.array(cover_list, dtype=np.float64).reshape(4, 3)]
            delta_matrix = np.matrix(delta_matrix)
            delta_matrix = delta_matrix.I
            delta_matrix: np.matrix = delta_matrix.T
            assert delta_matrix.shape == (4, 4)

            new_element_grid = new_element[each_id]
            new_S, new_xS, new_yS, new_zS = once_integration(new_element_grid)

            temp = relationship_cache.get_item('element', 'newelement', id_0=None, id_1=each_id)
            element_id = temp[0]['element']
            element_grid = manifold_element[element_id]
            element_grid = empty_to_polyhedron(element_grid)

            S, xS, yS, zS = once_integration(element_grid)

            for each, each_cover_id in enumerate(cover_id_list):
                is_real = new_cover.get_cell_attribute('real', each_cover_id)[0]
                if is_real == 1:
                    continue
                integration = delta_matrix[each, 0] * new_S + delta_matrix[each, 1] * new_xS + delta_matrix[each, 2] * new_yS + delta_matrix[each, 3] * new_zS
                integration_total = delta_matrix[each, 0] * S + delta_matrix[each, 1] * xS + delta_matrix[each, 2] * yS + delta_matrix[each, 3] * zS
                T0 = 1 / (integration / integration_total) ** 2

                total_id = int(new_cover.get_cell_attribute('total_id', each_cover_id)[0])
                temp = precondition[3 * total_id]

                if temp == 1:
                    precondition[3 * total_id] = T0
                    precondition[3 * total_id + 1] = T0
                    precondition[3 * total_id + 2] = T0
                else:
                    precondition[3 * total_id] = min(temp, T0)
                    precondition[3 * total_id + 1] = min(temp, T0)
                    precondition[3 * total_id + 2] = min(temp, T0)

            self.__precondition = precondition

