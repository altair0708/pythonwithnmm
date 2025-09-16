from NMM.base.Algorithm.ElementCracker.Criterion.CriterionInterface import AbstractCriterion
from NMM.base.Property.Implement.PropertyMap import PropertyMap
import math
import numpy as np


class MohrCoulomb(AbstractCriterion):
    def update(self, *args, **kwargs):
        material_parameter: PropertyMap = self._material_parameter
        material_id = int(self.material_id)

        friction_angle = material_parameter[str(material_id)]['friction_angle']
        cohesion = material_parameter[str(material_id)]['cohesion']
        tensile_strength = material_parameter[str(material_id)]['tensile_strength']

        self.calculate_elastic_stress()
        stress_tensor = self.stress_tensor

        sigma_1 = stress_tensor.max_component_vector[0]
        vector_1 = stress_tensor.max_component_vector[1]

        sigma_2 = stress_tensor.middle_component_vector[0]

        sigma_3 = stress_tensor.min_component_vector[0]
        vector_3 = stress_tensor.min_component_vector[1]

        N_0 = (1 + math.sin(friction_angle)) / (1 - math.sin(friction_angle))
        Fs = - sigma_3 + sigma_1 * N_0 - 2 * cohesion * math.sqrt(N_0)
        Ft = sigma_1 - tensile_strength

        rc = math.sqrt(1 + N_0 ** 2)
        Fsd = Fs / rc

        if Fs < 0 and Ft < 0:
            # no failure
            self._crack_flag = False
        elif Fsd > 0 and Fsd >= Ft:
            # shear failure
            self._crack_flag = True
            self._normal = compute_failure_plane_normal(vector_1, vector_3, friction_angle)
        elif Ft > 0 and Ft >= Fsd:
            # tensile failure
            self._crack_flag = True
            self._normal = stress_tensor.max_component_vector[1]
            self._normal = np.array(self._normal).flatten().tolist()
        else:
            raise Exception('Failure mode error!')


def compute_failure_plane_normal(e1, e3, phi_deg):
    """
    计算Mohr-Coulomb剪切破坏面方向（法向量）

    参数:
        e1: 最大主应力方向 (3D 单位向量)
        e3: 最小主应力方向 (3D 单位向量)
        phi_deg: 内摩擦角 (单位: 度)

    返回:
        破坏面法向量 (单位化)
    """
    # 角度转换
    phi_rad = np.radians(phi_deg)
    # theta = np.radians(45) + phi_rad / 2  # θ = 45° + φ/2
    theta = np.radians(135) + phi_rad / 2  # θ = 45° + φ/2

    # 向量归一化（以防用户输入不是单位向量）
    e1 = np.array(e1) / np.linalg.norm(e1)
    e3 = np.array(e3) / np.linalg.norm(e3)

    # 破坏面法向量
    n = np.cos(theta) * e1 + np.sin(theta) * e3
    n_normalized = n / np.linalg.norm(n)
    # TODO: e1 or e3 relate to crack angle?

    return n_normalized
