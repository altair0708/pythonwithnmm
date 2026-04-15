import numpy as np
from scipy.sparse.linalg import cg, spsolve, eigsh, spilu, LinearOperator
from NMM.base.Algorithm.Solver.AbstractSolver import AbstractSolver


class DOFScalingSolver(AbstractSolver):
    def update(self, *args, **kwargs):
        k = self._total_matrix
        f = self._total_force

        diag_k = k.diagonal()
        eps = 10**-16
        d_inv = 1.0 / np.sqrt(np.abs(diag_k) + eps)

        k_scaled = k.multiply(d_inv[:, None])
        k_scaled = k_scaled.multiply(d_inv[None, :])

        f_scaled = d_inv * f

        m = None
        try:
            k_csc = k_scaled.tocsc()
            ilu = spilu(k_csc)

            m = LinearOperator(k.shape, ilu.solve)
        except Exception as e:
            print('ILU failed, fallback to no preconditioner:', e)

        tol = 10**-15
        maxiter=1000
        u_hat, info = cg(k_scaled, f_scaled, tol=tol, maxiter=maxiter, M=m)
        # print(np.linalg.cond(k_scaled.toarray()))
        u = d_inv * u_hat

        self._result = u
