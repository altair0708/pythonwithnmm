from NMM.crack_3D.operation.CrackSurfaceOriginNormal.Implement.Interface import AbstractCrackType
from NMM.base.LeastSqPlane import min_distance_plane


class LSQCrackSurface(AbstractCrackType):
    def calculate_origin_point_normal_vector(self, crack_edge_cell_list, crack_edge_grid, max_strain):

        assert crack_edge_grid.GetPoint(0) == (0, 0, 0)
        crack_point_list = [crack_edge_grid.GetPoint(i + 1) for i in range(4)]
        origin_point, normal_vector = min_distance_plane(crack_point_list)

        return origin_point, normal_vector
