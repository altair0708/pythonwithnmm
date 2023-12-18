from NMM.base.TensorBase import Tensor
from NMM.base.MohrFailure import mohr_failure
import numpy as np
import json

with open('../../data_3D/material/material_coefficient.json') as f:
    material_json = json.load(f)

material = json.dumps(material_json)

stress = Tensor(np.array([[-3], [2], [1], [0], [0], [0]]))

result = mohr_failure(stress, material)

print(result)
