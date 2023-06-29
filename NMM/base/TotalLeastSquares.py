from scipy.sparse import hstack
from scipy.sparse.linalg import svds


def total_least_square(A, b, k=6):
    u, s, v = svds(hstack([A, b]), k)
    return v[-1, :-1] / -v[-1, -1]
