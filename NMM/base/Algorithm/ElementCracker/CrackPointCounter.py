from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from copy import deepcopy
import math
import numpy as np


class CrackPointCounter(AbstractAlgorithm):
    def __init__(self, element_id, element_surface: VtkGrid = None, crack_edge: VtkGrid = None):
        self.__element_id = element_id
        if element_surface is None:
            self.__element_surface: VtkGrid = entrance_cache.get_item('element_surface_VtkGrid')
        else:
            self.__element_surface = element_surface
        if crack_edge is None:
            self.__crack_edge: VtkGrid = entrance_cache.get_item('crack_edge_VtkGrid')
        else:
            self.__crack_edge = crack_edge

        self.__global_error = 0.000001
        # result
        self.__surface_count = 0
        self.__point_list = []
        self.__normal = [0, 0, 0]
        self.__origin = [0, 0, 0]

        self.__edge_vector = [0, 0, 0]
        self.__adjacent_element_id = -1
        self.__adjacent_crack_surface_id = -1

    @property
    def surface_count(self):
        return self.__surface_count

    @property
    def point_list(self):
        result = deepcopy(self.__point_list)
        return result

    @property
    def normal(self):
        assert len(self.__point_list) > 2
        return self.__normal

    @property
    def edge_vector(self):
        assert len(self.__point_list) == 2
        return self.__edge_vector

    @property
    def adjacent_crack_surface_id(self):
        assert len(self.__point_list) == 2
        return self.__adjacent_crack_surface_id

    @property
    def adjacent_element_id(self):
        assert len(self.__point_list) == 2
        return self.__adjacent_element_id

    @property
    def origin(self):
        return self.__origin

    @staticmethod
    def compute_plane_normal(A, B, C):
        AB = np.subtract(B, A)
        AC = np.subtract(C, A)
        normal = np.cross(AB, AC)
        return normal

    @staticmethod
    def fit_plane(points):
        points = np.array(points)
        centroid = np.mean(points, axis=0)
        centered = points - centroid
        cov = np.cov(centered.T)
        eigvals, eigvecs = np.linalg.eigh(cov)
        normal = eigvecs[:, np.argmin(eigvals)]
        d = -np.dot(normal, centroid)

        normal = normal.tolist()
        centroid = centroid.tolist()
        return normal, d, centroid

    def update(self, *args, **kwargs):
        element_id = self.__element_id
        element_surface = self.__element_surface
        crack_edge = self.__crack_edge

        relationship_list = relationship_cache.get_item(name_0='element', name_1='surface', id_0=element_id, id_1=None)
        assert len(relationship_list) == 4

        temp_point_list = []
        crack_surface_list = []
        for each_relationship in relationship_list:
            surface_id = each_relationship['surface']
            cracked = element_surface.get_cell_attribute('cracked', surface_id)[0]
            if cracked == 9:
                # check number of crack surface
                crack_surface_list.append(surface_id)

                edge_list = relationship_cache.get_item(name_0='surface', name_1='crackedge', id_0=surface_id, id_1=None)
                edge_id = edge_list[0]['crackedge']
                point_id_list = crack_edge.get_cell_point_id(edge_id)

                for each_point_id in point_id_list:
                    coordinate = crack_edge.get_point_coordinate(each_point_id)
                    temp_point_list.append(coordinate)
                self.__surface_count = self.__surface_count + 1

        for p in temp_point_list:
            if not any(math.dist(p, q) < self.__global_error for q in self.__point_list):
                self.__point_list.append(p)
        if len(self.__point_list) == 2:
            self.__origin = self.__point_list[0]
            self.__edge_vector = [self.__point_list[0][i] - self.__point_list[1][i] for i in range(len(self.__point_list[0]))]

            # get adjacent cracked element id and adjacent crack surface id
            assert len(crack_surface_list) == 1
            temp_element_id = relationship_cache.get_item(name_0='element', name_1='surface', id_0=None, id_1=crack_surface_list[0])
            assert len(temp_element_id) == 2
            temp_element_id = [each_relationship['element'] for each_relationship in temp_element_id]
            temp_element_id.remove(element_id)
            temp_element_id = temp_element_id[0]
            temp_crack_surface_id = relationship_cache.get_item(name_0='element', name_1='cracksurface', id_0=temp_element_id)
            assert len(temp_crack_surface_id) == 1

            self.__adjacent_crack_surface_id = temp_crack_surface_id[0]['cracksurface']
            self.__adjacent_element_id = temp_element_id

        if len(self.__point_list) > 2:
            self.__normal, _, self.__origin = self.fit_plane(self.__point_list)
