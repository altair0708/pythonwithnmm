from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Algorithm.ElementCracker.CompleteElementCutter import CompleteElementCutter
from NMM.base.Algorithm.ElementCracker.CrackPointCounter import CrackPointCounter
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.Algorithm.ElementCracker.Criterion.CriterionInterface import AbstractCriterion
from NMM.base.Algorithm.CalculateDihedralAngle import CalculateDihedralAngle
import numpy as np


def schmidt_orthogonalization(vector_1, vector_2):
    # v1, v2
    vector_1 = np.array(vector_1).reshape(3)
    vector_2 = np.array(vector_2).reshape(3)
    result = vector_2 - (np.dot(vector_1, vector_2) / np.dot(vector_1, vector_1)) * vector_1
    return result


class ElementCracker(AbstractAlgorithm):
    def __init__(self, id_value: int, manifold_element_grid: VtkGrid):
        super(ElementCracker, self).__init__()
        self.__element_id = id_value
        self.__manifold_element = manifold_element_grid

        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')
        self.__criterion = None

    def update(self):
        criterion: AbstractCriterion = self.__criterion
        criterion.set_element_id(self.__element_id)
        criterion.update()

        # normal vector, origin point, crack_flag
        # normal = [0, 1, 0]
        # origin = [0, 0, 0]
        # crack_flag = True

        normal = criterion.normal
        crack_flag = criterion.crack_flag

        counter = CrackPointCounter(self.__element_id)
        counter.update()
        crack_point_list = counter.point_list
        origin = counter.origin

        angle_algorithm = None
        if len(crack_point_list) == 2:
            edge_vector = counter.edge_vector
            normal = schmidt_orthogonalization(edge_vector, normal)
            angle_algorithm = CalculateDihedralAngle(counter.adjacent_crack_surface_id)

        elif len(crack_point_list) > 2:
            normal = counter.normal
        else:
            raise Exception('Crack point list error!!!')

        assert len(normal) == 3
        normal = (0, 0, 1)
        if crack_flag:
            cutter = CompleteElementCutter(self.__element_id, self.__manifold_element, origin, normal, angle_algorithm)
            cutter.update()

    def set_criterion(self, criterion):
        self.__criterion = criterion
