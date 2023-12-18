from NMM.base.TensorBase import Tensor
import numpy as np


a = Tensor(np.array([-2, -2, -3, 0, 0, 0]).reshape((6, 1)))
print(a.max_component_vector)
print(a.min_component_vector)
print(a.middle_component_vector)
