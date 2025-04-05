import numpy as np


def old_matrix_save(matrix: np.ndarray, matrix_name: str, path=None):
    if path is None:
        path = '/Users/suboyi/PycharmProjects/pythonwithnmm/NMM/log/data'
    file_path = f'{path}/old_{matrix_name}.npy'
    np.save(file_path, matrix)


def new_matrix_save(matrix: np.ndarray, matrix_name: str, path=None):
    if path is None:
        path = '/Users/suboyi/PycharmProjects/pythonwithnmm/NMM/log/data'
    file_path = f'{path}/new_{matrix_name}.npy'
    np.save(file_path, matrix)
