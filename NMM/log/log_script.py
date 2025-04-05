import numpy as np


def print_matrix(matrix_name: str):
    old_name = f'data/old_{matrix_name}.npy'
    new_name = f'data/new_{matrix_name}.npy'
    old = np.load(old_name)
    new = np.load(new_name)
    print(f'old_{matrix_name}:')
    print(old)
    print(f'new_{matrix_name}:')
    print(new)


def matrix_difference(matrix_name: str):
    old_name = f'data/old_{matrix_name}.npy'
    new_name = f'data/new_{matrix_name}.npy'
    old = np.load(old_name)
    new = np.load(new_name)
    # print(f'{matrix_name}_difference:')
    # print(f'{old - new}')
    x = np.linalg.norm(old - new, ord=1)
    if x != 0:
        print(f'{matrix_name}_norm:')
        print(x)
    return x


if __name__ == '__main__':
    # summary = 0
    # for element_id in range(3583):
    #     summary = summary + matrix_difference(f'matrix_{element_id}')
    # print(summary)
    print_matrix('matrix_1074')
