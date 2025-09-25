from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.crack_propagate.generate_crack_quad import generate_crack_polygon
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.VTKBase.crack_propagate.intersection_with_shell import intersection_with_shell
import numpy as np


class CrackQuad(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid, crack_propagation: VtkGrid):
        self.__crack_tip = crack_tip
        self.__crack_propagation = crack_propagation

    def update(self, *args, **kwargs):
        crack_tip = self.__crack_tip
        crack_propagation = self.__crack_propagation
        for each_id, each_crack_tip in enumerate(crack_tip):
            if crack_tip.is_empty_cell(each_id):
                continue
            # generate crack quad
            point_id = crack_tip.get_cell_point_id(each_id)
            origin_coordinate = [crack_tip.get_point_coordinate(i) for i in point_id]
            propagate_vector = [crack_tip.get_point_attribute('propagate_vector', i) for i in point_id]

            quad_cell = generate_crack_polygon(origin_coordinate, propagate_vector)

            # add crack quad to crack propagation
            if quad_cell is not None:
                crack_propagation.value = insert_a_vtk_cell(quad_cell, crack_propagation.value)
