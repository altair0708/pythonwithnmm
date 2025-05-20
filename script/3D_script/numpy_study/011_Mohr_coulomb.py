import numpy as np


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
    theta = np.radians(45) + phi_rad / 2  # θ = 45° + φ/2

    # 向量归一化（以防用户输入不是单位向量）
    e1 = np.array(e1) / np.linalg.norm(e1)
    e3 = np.array(e3) / np.linalg.norm(e3)

    # 破坏面法向量
    n = np.cos(theta) * e1 + np.sin(theta) * e3
    n_normalized = n / np.linalg.norm(n)

    return n_normalized


if __name__ == '__main__':
    # 示例主应力方向（单位向量）
    e1 = [1, 0, 0]  # 最大主应力方向
    e3 = [0, 0, 1]  # 最小主应力方向

    phi = 30  # 摩擦角 φ = 30°

    n = compute_failure_plane_normal(e1, e3, phi)
    print("剪切破坏面法向量:", n)
