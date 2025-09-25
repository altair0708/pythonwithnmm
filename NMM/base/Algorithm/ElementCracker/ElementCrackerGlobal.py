from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Algorithm.ElementCracker.CompleteElementCutterGlobal import CompleteElementCutter
from NMM.base.Algorithm.Debuger import Debuger
from NMM.base.VTKBase.write_file import debug_write_file
from NMM.base.VTKBase.test_example import generate_point_grid
from typing import Dict
from copy import deepcopy
import numpy as np
import sys


class ElementCrackerGlobal(AbstractAlgorithm):
    def __init__(self, manifold_element_grid: VtkGrid):
        super(ElementCrackerGlobal, self).__init__()
        self.__manifold_element = manifold_element_grid

        self.__crack_point_dict = {}

    def update(self):
        manifold_element = self.__manifold_element
        element_number = self.__manifold_element.get_cell_number()
        new_cracked = filter(lambda element_id: self.__manifold_element.get_cell_attribute('cracked', element_id)[0] == 8, range(element_number))

        assert len(self.__crack_point_dict) > 0

        new_cracked = list(new_cracked)
        for each_id in new_cracked:
            crack_point_list = self.__crack_point_dict[each_id]

            try:
                assert len(crack_point_list) >= 3
            except AssertionError:
                error_grid = entrance_cache.get_item('crack_propagation_VtkGrid')
                debuger = Debuger()
                debuger.update(error_grid.value, 'crack_propagation.vtu')

                error_grid = entrance_cache.get_item('crack_tip_VtkGrid')
                debuger.update(error_grid.value, 'crack_tip.vtu')

                error_grid = entrance_cache.get_item('manifold_element_VtkGrid')
                debuger.update(error_grid.value, 'manifold_element.vtu')

                for each in range(len(crack_point_list)):
                    point_grid = generate_point_grid(crack_point_list[each])
                    debuger.update(point_grid, f'point_grid_{each}.vtu')

                print(f'crack point number error!')
                print(f'element_id: {each_id}')
                print(f'crack_point_list: {crack_point_list}')
                print(f'crack status: {manifold_element.get_cell_attribute("cracked", each_id)}')
                sys.exit()

            origin, normal = fit_plane(crack_point_list)
            cutter = CompleteElementCutter(each_id, manifold_element, origin, normal)
            cutter.update()

    @property
    def crack_point_dict(self):
        return self.__crack_point_dict

    @crack_point_dict.setter
    def crack_point_dict(self, value: Dict):
        self.__crack_point_dict = deepcopy(value)


def fit_plane(points):
    """
    使用最小二乘法拟合平面，输入为一组三维点。
    返回拟合平面的法向量（normal）和质心（origin）。

    参数：
        points (list of list or np.ndarray): 形如 [[x1, y1, z1], [x2, y2, z2], ...]

    返回：
        origin (np.ndarray): 平面上的一个点（质心）
        normal (np.ndarray): 单位法向量
    """
    points = np.array(points)

    if points.shape[0] < 3:
        raise ValueError("至少需要3个点来拟合平面")

    # 计算质心
    centroid = np.mean(points, axis=0)

    # 中心化点集
    centered = points - centroid

    # 计算协方差矩阵，并求最小特征值对应的特征向量
    _, _, vh = np.linalg.svd(centered)
    normal = vh[-1]

    return centroid, normal / np.linalg.norm(normal)
