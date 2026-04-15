import numpy as np
from scipy.sparse.linalg import cg, spsolve, eigsh, spilu, LinearOperator
from scipy.sparse import diags
from NMM.base.Algorithm.Solver.AbstractSolver import AbstractSolver
from NMM.base.Algorithm.Solver.GeometricPrecondition import GeometricPrecondition
from NMM.base.Algorithm.Solver.DOFLocking import DOFLocking
from NMM.base.Algorithm.Solver.NewCoverMapping import NewCoverMapping


def find_diag_gt_tol(T, Ttol):
    d = T.diagonal()  # 直接取对角线
    idx = np.where(d > Ttol)[0]  # 找满足条件的索引
    return idx, d[idx]


class PreconditionGeometrySolver(AbstractSolver):
    def update(self, *args, **kwargs):
        k = self._total_matrix
        f = self._total_force

        algorithm = GeometricPrecondition()
        algorithm.update()
        T = algorithm.precondition
        T = diags(T)

        id_list, _ = find_diag_gt_tol(T, 100000)

        algorithm = NewCoverMapping()
        algorithm.update()
        new_cover_dict = algorithm.new_cover_map

        algorithm = DOFLocking(k, f, T)
        for each_id in id_list:
            each_real_id = new_cover_dict[each_id]
            algorithm.lock(each_real_id, each_id)
        k_new, f_new, T_new = algorithm.update()

        k_precondition = (T_new @ k_new @ T_new).tocsc()
        f_precondition = T_new @ f_new

        u_precondition = spsolve(k_precondition, f_precondition)
        u_new = T_new @ u_precondition

        u = algorithm.recover(u_new)
        sum_count = u.size
        error_count = np.sum(u > 0.001)

        print(sum_count)
        print(error_count)

        # r = k @ u - f
        # abs_err = np.linalg.norm(r)
        # print(abs_err / np.linalg.norm(f))

        self._result = u
