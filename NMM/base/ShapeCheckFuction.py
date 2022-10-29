import numpy as np
from typing import Tuple


def check_shape(array: np.ndarray, shape: Tuple[int, int]):
    if array.shape != shape:
        raise Exception('array shape error, expect shape: {}, input shape: {}'.format(shape, array.shape))
