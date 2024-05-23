from NMM.crack_3D.operation.CrackSurfaceOriginNormal.Implement.Interface import AbstractCrackType
import numpy as np


class CoplaneCrackSurface(AbstractCrackType):
    def calculate_origin_point_normal_vector(self, crack_edge_cell_list, crack_edge_grid, max_strain):

        vector_0 = crack_edge_cell_list[0].vector
        vector_1 = crack_edge_cell_list[1].vector

        normal_vector = np.cross(vector_0, vector_1)
        origin_point = crack_edge_cell_list[0].point_0

        return origin_point, normal_vector
