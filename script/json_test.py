import json

file_name = '../data/global_variable.json'
material_file_name = '../data/material_coefficient.json'
joint_material_file_name = '../data/joint_material_coefficient.json'
global_variable = {
    'dynamic_coefficient': 1,
    'step': 100,
    'material_types': 1,
    'joint_material_types': 1,
    'displacement_allow': 0.003,
    'time_increment': 0.02,
    'contact_spring_stiff': 100000,
    'SOR_factor': 1.80,
    'coordinate_system': (0, 0, 0)
}
material_coefficient = {
    'id': 1,
    'unit_mass': 0.05,
    'body_force': (0, -1),
    'elastic_modulus': 5000,
    'possion_ratio': 0.3,
    'initial_force': (0, 0, 0),
    'yield_coefficient': {
        'friction_angle': 0,
        'cohesion': 0,
        'tensile_strength': 0
    },
    'initial_velocity': (0, 0, 0)
}
joint_material_coefficient = {
    'id': 1,
    'friction_angle': 0,
    'cohesion': 0,
    'tensile_strength': 0
}
with open(file_name, 'w') as configure_file:
    json.dump(global_variable, configure_file, indent=4)
with open(material_file_name, 'w') as configure_file:
    json.dump(material_coefficient, configure_file, indent=4)
with open(joint_material_file_name, 'w') as configure_file:
    json.dump(joint_material_coefficient, configure_file, indent=4)

with open(material_file_name, 'r') as configure_file:
    a = json.load(configure_file)
print(type(a['initial_force']))
