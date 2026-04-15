from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from scipy.sparse import diags
import numpy as np


class DOFLocking(AbstractAlgorithm):
    def __init__(self, k, f, T=None):
        self.__k = k
        self.__f = f

        self.__T = T  # Precondition Matrix, default None

        self.__dof_pairs = []
        self.__mask = None
        self.__size = None

    def lock(self, real_id: int, virtual_id: int, *args, **kwargs):
        self.__dof_pairs.append(tuple([virtual_id, real_id]))

    def update(self, *args, **kwargs):
        k = self.__k.tolil()
        f = self.__f

        delete_set = set()

        for a, b in self.__dof_pairs:
            # -------- Step 1: 刚度矩阵合并 --------
            k[b, :] = k[b, :] + k[a, :]
            k[:, b] = k[:, b] + k[:, a]

            # -------- Step 2: 力向量合并 --------
            f[b] = f[b] + f[a]

            delete_set.add(a)

        # -------- Step 3: 删除 a --------
        n = k.shape[0]
        mask = np.ones(n, dtype=bool)

        for a in delete_set:
            mask[a] = False

        self.__size = n
        self.__mask = mask

        k_new = k[mask][:, mask]
        f_new = f[mask]

        self.__k = k_new.tocsc()
        self.__f = f_new

        if self.__T is not None:
            t = self.__T.diagonal()
            t_new = t[mask]
            T_new = diags(t_new)
            self.__T = T_new
            return self.__k, self.__f, self.__T

        return self.__k, self.__f

    def recover(self, u_reduced):
        """
        将压缩后的解恢复为完整解向量
        """
        u_full = np.zeros(self.__size)

        # -------- Step 1: 填充保留 DOF --------
        u_full[self.__mask] = u_reduced

        # -------- Step 2: 恢复约束 DOF --------
        for a, b in self.__dof_pairs:
            u_full[a] = u_full[b]

        return u_full

