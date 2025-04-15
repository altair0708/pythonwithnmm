from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
import numpy as np


class CoverRefresher(AbstractAlgorithm):
    def __init__(self, displacement_vector, mathematics_point: VtkGrid, new_cover: VtkGrid):
        self.__displacement_vector = displacement_vector
        self.__mathematics_point = mathematics_point
        self.__new_cover = new_cover

    def refresh_math_cover(self):
        patch_displacement = self.__displacement_vector
        temp_math_displacement = patch_displacement.reshape((-1, 3))
        for each_cover_id in range(self.__mathematics_point.get_cell_number()):

            assert each_cover_id == self.__mathematics_point.get_cell_attribute('cell_id', each_cover_id)[0]

            math_cover_displacement_increment = temp_math_displacement[each_cover_id]
            self.__mathematics_point.set_attribute('math_cover_displacement_increment', each_cover_id, math_cover_displacement_increment)

            temp_math_cover_displacement = self.__mathematics_point.get_cell_attribute('math_cover_displacement_total', each_cover_id)
            math_cover_displacement_total = np.array(temp_math_cover_displacement, dtype=np.float64) + np.array(math_cover_displacement_increment, dtype=np.float64)
            self.__mathematics_point.set_attribute('math_cover_displacement_total', each_cover_id, math_cover_displacement_total)

    def refresh_new_cover(self):
        patch_displacement = self.__displacement_vector
        temp_math_displacement = patch_displacement.reshape((-1, 3))

        cell_id = [i for i in range(self.__new_cover.get_cell_number())]
        total_id = map(lambda x: int(self.__new_cover.get_cell_attribute('total_id', x)[0]), cell_id)

        for each_cell_id, each_total_id in zip(cell_id, total_id):

            assert each_cell_id == self.__new_cover.get_cell_attribute('cell_id', each_cell_id)[0]
            assert each_total_id == self.__new_cover.get_cell_attribute('total_id', each_cell_id)[0]

            math_cover_displacement_increment = temp_math_displacement[each_total_id]
            self.__new_cover.set_attribute('math_cover_displacement_increment', each_cell_id, math_cover_displacement_increment)

            temp_math_cover_displacement = self.__new_cover.get_cell_attribute('math_cover_displacement_total', each_cell_id)
            math_cover_displacement_total = np.array(temp_math_cover_displacement, dtype=np.float64) + np.array(math_cover_displacement_increment, dtype=np.float64)
            self.__new_cover.set_attribute('math_cover_displacement_total', each_cell_id, math_cover_displacement_total)

    def update(self, *args, **kwargs):
        self.refresh_math_cover()
        self.refresh_new_cover()
