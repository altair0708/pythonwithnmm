from NMM.base.Algorithm.ElementCracker.Criterion.CriterionInterface import AbstractCriterion
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap
import numpy as np


class MaximumTensilePlaneStress(AbstractCriterion):
    def __init__(self, element_id: int = -1, manifold_element: VtkGrid = None, material_parameter: PropertyMap = None):
        super().__init__(element_id, manifold_element, material_parameter)
        self.__e1 = np.zeros((3, 1))
        self.__e2 = np.zeros((3, 1))
        self.__e3 = np.zeros((3, 1))

    def set_plane_normal(self, e1, e2, e3):
        self.__e1 = np.array(e1)
        self.__e2 = np.array(e2)
        self.__e3 = np.array(e3)

    def update(self, *args, **kwargs):
        e1 = self.__e1
        e2 = self.__e2
        e3 = self.__e3

        self.calculate_elastic_stress()
        stress_tensor = self.stress_tensor
        stress = np.asarray(stress_tensor.matrix, dtype=np.float64)

        s11 = e1 @ stress @ e1
        s12 = e1 @ stress @ e2
        s21 = e2 @ stress @ e1
        s22 = e2 @ stress @ e2

        sigma_2 = np.array([[s11, s12],
                            [s21, s22]], dtype=np.float64)

        # 求特征值与特征向量
        eigvals, eigvecs = np.linalg.eigh(sigma_2)  # 升序

        # 降序排列（第一为最大主应力）
        idx = np.argsort(eigvals)[::-1]

        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]  # 每列是一个 2D 特征向量（在 e1,e2 基下）

        # 最大主应力对应的 2D 特征向量（取第一列）
        v2 = eigvecs[:, 0]

        # 映回三维方向： p3 = v2[0]*e1 + v2[1]*e2
        p3 = v2[0] * e1 + v2[1] * e2
        p3 = p3 / np.linalg.norm(p3)  # 单位化（数值稳定）

        if eigvals[0] > 1000:
            self._crack_flag = True
        else:
            self._crack_flag = False

        normal = np.cross(p3, e3)
        self._normal = normal / np.linalg.norm(normal)

        assert len(self._normal) == 3
