from NMM.base.TensorBase import Tensor
import numpy as np


a = Tensor(np.array([1, 2, 3, 4, 5, 6]).reshape((6, 1)))
a = np.array(a.max_component_vector).reshape(3)
print(a)
