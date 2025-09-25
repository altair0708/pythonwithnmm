import numpy as np
from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.VTKBase.find_close_cell import find_close_cell
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class AverageStressCalculator(AbstractAlgorithm):
    def __init__(self, coordinate: tuple):
        assert len(coordinate) == 3
        self.__coordinate = coordinate
        self.__geometric_tetrahedron: VtkGrid = entrance_cache.get_item('geometric_tetrahedron_VtkGrid')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__result = np.zeros((6, 1))

    def update(self, *args, **kwargs):

        geometric_tetrahedron = self.__geometric_tetrahedron
        coordinate = self.__coordinate
        manifold_element = self.__manifold_element
        mathematics_point = self.__mathematics_point

        element_id = find_close_cell(vtk_model=geometric_tetrahedron.value, point_coord=coordinate)

        # get relate cover
        f_matrix = np.zeros((0, 3))
        strain_list = []
        relationship_list = relationship_cache.get_item('cover', 'element', id_0=None, id_1=element_id)
        if len(relationship_list) != 4:
            print(relationship_list)
        assert len(relationship_list) == 4
        for each_cover in relationship_list:
            cover_id = each_cover['cover']
            temp_relationship_list = relationship_cache.get_item('cover', 'element', id_0=cover_id, id_1=None)

            cover_strain = np.zeros((6, 1))
            for each_element in temp_relationship_list:
                adjacent_element_id = each_element['element']
                strain = manifold_element.get_cell_attribute('initial_strain_total', adjacent_element_id)
                strain = np.array(strain).reshape((6, 1))
                cover_strain = cover_strain + strain
            average_strain = cover_strain / len(temp_relationship_list)
            strain_list.append(average_strain)

            cover_coordinate = np.array(mathematics_point.get_point_coordinate(cover_id)).reshape((1, 3))
            f_matrix = np.vstack((f_matrix, cover_coordinate))

        assert f_matrix.shape == (4, 3)
        f_matrix = np.hstack((np.ones((4, 1)), f_matrix))
        f_matrix = np.linalg.inv(f_matrix)

        coordinate_parameter = np.array((1, coordinate[0], coordinate[1], coordinate[2])).reshape((1, 4))
        weight_parameter = np.dot(coordinate_parameter, f_matrix)
        # print(strain_list)
        # print(weight_parameter)

        result = np.zeros((6, 1))
        for i in range(4):
            result = result + weight_parameter[0][i] * strain_list[i]

        self.__result = result

    @property
    def strain(self):
        return self.__result
