import numpy as np


def elastic_matrix(temp_E, temp_mu):
    elastic_matrix = temp_E / ((1 + temp_mu) * (1 - 2 * temp_mu)) * \
                     np.matrix([[1 - temp_mu, temp_mu, temp_mu, 0, 0, 0],
                                [temp_mu, 1 - temp_mu, temp_mu, 0, 0, 0],
                                [temp_mu, temp_mu, 1 - temp_mu, 0, 0, 0],
                                [0, 0, 0, (1 - 2 * temp_mu) / 2, 0, 0],
                                [0, 0, 0, 0, (1 - 2 * temp_mu) / 2, 0],
                                [0, 0, 0, 0, 0, (1 - 2 * temp_mu) / 2]], dtype=np.float64)
    return elastic_matrix
