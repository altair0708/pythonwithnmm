from NMM.fem_3D.ElementBase_3D import Element3D, calculate_integration
from NMM.base.TensorBase import Tensor
import numpy as np

joint_list = [(0, 0, 0),
              (1, 0, 0),
              (0, 1, 0),
              (0, 0, 1)]
element = Element3D(0)

for i, each_joint in enumerate(joint_list):
    element.joint_id[i] = i
    element.joint_list[i] = each_joint

for i, each_joint in enumerate(joint_list):
    element.patch_id[i] = i
    element.patch_list[i] = each_joint

element.patch_displacement[0] = (0, 0, 0)
element.patch_displacement[1] = (1, 0, 0)
element.patch_displacement[2] = (0, 0, 0)
element.patch_displacement[3] = (0, 0, 0)

# print(element.B_shape_matrix)
strain = Tensor(element.initial_strain_total)
print(strain.max_component_vector)

