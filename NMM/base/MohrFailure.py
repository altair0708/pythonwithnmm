import json
import math
from NMM.base.TensorBase import Tensor


def is_json(src):
    src = json.loads(src)
    if type(src) == dict:
        return True
    else:
        return False


def mohr_failure(stress: Tensor, material: str):

    if not is_json(material):
        raise Exception('Material json format error!')

    sigma_1 = stress.max_component_vector[0]
    sigma_2 = stress.middle_component_vector[0]
    sigma_3 = stress.min_component_vector[0]

    material_dict = json.loads(material)
    friction_angle = material_dict['yield_coefficient']['friction_angle']
    cohesion = material_dict['yield_coefficient']['cohesion']
    tensile_strength = material_dict['yield_coefficient']['tensile_strength']

    N_0 = (1 + math.sin(friction_angle)) / (1 - math.sin(friction_angle))
    Fs = - sigma_3 + sigma_1 * N_0 - 2 * cohesion * math.sqrt(N_0)
    Ft = sigma_1 - tensile_strength

    rc = math.sqrt(1 + N_0**2)
    Fsd = Fs / rc

    if Fs < 0 and Ft < 0:
        # no failure
        return 0
    elif Fsd > 0 and Fsd >= Ft:
        # shear failure
        return 1
    elif Ft > 0 and Ft >= Fsd:
        # tensile failure
        return 2
    else:
        raise Exception('Failure mode error!')

