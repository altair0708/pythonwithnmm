from NMM.base.Algorithm.ElementCracker.Criterion.CriterionInterface import AbstractCriterion
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap
import math
import numpy as np


class MohrCoulombPlaneStress(AbstractCriterion):
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

        material_parameter: PropertyMap = self._material_parameter
        material_id = int(self.material_id)

        friction_angle = material_parameter[str(material_id)]['friction_angle']
        cohesion = material_parameter[str(material_id)]['cohesion']
        tensile_strength = material_parameter[str(material_id)]['tensile_strength']

        self.calculate_elastic_stress()
        stress_tensor = self.stress_tensor
        stress = np.asarray(stress_tensor.matrix, dtype=np.float64)

        s11 = e1 @ stress @ e1
        s12 = e1 @ stress @ e2
        s21 = e2 @ stress @ e1
        s22 = e2 @ stress @ e2

        sigma = np.array([[s11, s12],
                          [s21, s22]], dtype=np.float64)

        # 求特征值与特征向量
        eigvals, eigvecs = np.linalg.eigh(sigma)  # 升序

        # 降序排列（第一为最大主应力）
        idx = np.argsort(eigvals)[::-1]

        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]  # 每列是一个 2D 特征向量（在 e1,e2 基下）

        # sigma_1 < sigma_2 < sigma_3.
        # compressive stresses are negative.

        sigma_3 = eigvals[0]
        sigma_1 = eigvals[1]

        # 最大主应力对应的 2D 特征向量（取第一列）
        v3 = eigvecs[:, 0]
        p3 = v3[0] * e1 + v3[1] * e2
        p3 = p3 / np.linalg.norm(p3)

        v1 = eigvecs[:, 1]
        p1 = v1[0] * e1 + v1[1] * e2
        p1 = p1 / np.linalg.norm(p1)

        N_0 = (1 + math.sin(friction_angle)) / (1 - math.sin(friction_angle))
        Fs = - sigma_1 + sigma_3 * N_0 - 2 * cohesion * math.sqrt(N_0)
        Ft = sigma_3 - tensile_strength

        rc = math.sqrt(1 + N_0 ** 2)
        Fsd = Fs / rc

        if Fs < 0 and Ft < 0:
            # no failure
            self._crack_flag = False
        elif Fsd > 0 and Fsd >= Ft:
            # shear failure
            self._crack_flag = True

            phi_rad = np.radians(friction_angle)
            theta = np.radians(45) + phi_rad / 2

            n = np.cos(theta) * p3 + np.sin(theta) * p1
            self._normal = n / np.linalg.norm(n)

        elif Ft > 0 and Ft >= Fsd:
            # tensile failure
            self._crack_flag = True
            normal = np.cross(p3, e3)
            self._normal = normal / np.linalg.norm(normal)
        else:
            raise Exception('Failure mode error!')

        assert len(self._normal) == 3
