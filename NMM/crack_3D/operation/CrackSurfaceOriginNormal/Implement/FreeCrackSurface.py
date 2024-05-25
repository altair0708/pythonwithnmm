from NMM.crack_3D.operation.CrackSurfaceOriginNormal.CrackTypeInterface import AbstractCrackType
from NMM.crack_3D.ElementBase3D import schmidt_orthogonalization


class FreeCrackSurface(AbstractCrackType):
    def calculate_origin_point_normal_vector(self, crack_edge_cell_list, crack_edge_grid, max_strain):

        crack_edge_cell = crack_edge_cell_list[0]
        vector_0 = crack_edge_cell.vector
        origin_point = crack_edge_cell.point_0

        # assert crack edge only relate one crack surface
        assert crack_edge_cell.crack_surface_id[1] == -1

        normal_vector = schmidt_orthogonalization(vector_0, max_strain)

        return origin_point, normal_vector
