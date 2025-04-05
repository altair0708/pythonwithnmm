from NMM.preprocess_3D.Model.ModelBuilder import PreprocessModelBuilder
from NMM.base.Command.Invoker import Invoker, InvokerQueue
from NMM.base.Command.ModelCommand.ModelAddAttribute import ModelAddAttribute
from NMM.base.Command.ModelCommand.ModelGenerateBoundaryCondition import ModelGenerateBoundaryCondition
from NMM.base.Command.ModelCommand.ModelInitialCrack import ModelInitialCrack
from NMM.base.Command.ModelCommand.ModelWriteFile import ModelWriteFile
from NMM.base.Command.ModelCommand.ModelGenerateGrid import ModelGenerateGrid
from NMM.base.Command.ModelCommand.ModelInitialSpecialPoint import ModelInitialSpecialPoint
from NMM.base.Command.ModelCommand.ModelInitialMathPoint import ModelInitialMathPoint
from NMM.base.Command.ModelCommand.ModelInitialManifoldElement import ModelInitialManifoldElement
from NMM.base.Command.ModelCommand.ModelGenerateMathematicsPoint import ModelGenerateMathematicsPoint
from NMM.base.Command.ModelCommand.ModelGenerateManifoldElement import ModelGenerateManifoldElement


builder = PreprocessModelBuilder()
# model = builder.build('D:/science/NMM/python-NMM/example/example001')
model = builder.build('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001')

invoker = InvokerQueue()

data_structure = model.get_property('data_structure')
file_path = model.get_property('file_path')
element_list = model.get_property('matrix_element')
nmm_database = model.get_property('database')

invoker.set_command(ModelGenerateGrid('geometric_vertex', data_structure))
invoker.set_command(ModelAddAttribute('geometric_vertex', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('geometric_vertex', 'cell_id', data_structure))

invoker.set_command(ModelGenerateGrid('geometric_line', data_structure))
invoker.set_command(ModelAddAttribute('geometric_line', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('geometric_line', 'cell_id', data_structure))

invoker.set_command(ModelGenerateGrid('geometric_surface', data_structure))
invoker.set_command(ModelAddAttribute('geometric_surface', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('geometric_surface', 'cell_id', data_structure))

invoker.set_command(ModelGenerateGrid('geometric_tetrahedron', data_structure))
invoker.set_command(ModelAddAttribute('geometric_tetrahedron', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('geometric_tetrahedron', 'cell_id', data_structure))

invoker.set_command(ModelGenerateGrid('mathematics_cover', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_cover', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_cover', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_cover', 'cracked', data_structure))

invoker.set_command(ModelGenerateMathematicsPoint(data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'cracked', data_structure))

invoker.set_command(ModelGenerateManifoldElement(data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'cracked', data_structure))

invoker.set_command(ModelGenerateGrid('element_surface', data_structure))
invoker.set_command(ModelAddAttribute('element_surface', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('element_surface', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('element_surface', 'cracked', data_structure))

invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_displacement_increment', data_structure))
invoker.set_command(ModelInitialMathPoint())

invoker.set_command(ModelAddAttribute('manifold_element', 'material_id', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_velocity', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'initial_strain_total', data_structure))
invoker.set_command(ModelInitialManifoldElement())

crack_list = ['crack_surface', 'crack_edge', 'new_cover', 'new_element', 'new_surface']
for each_entity_name in crack_list:
    invoker.set_command(ModelAddAttribute(each_entity_name, 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'real', data_structure))
invoker.set_command(ModelInitialCrack())

invoker.set_command(ModelGenerateBoundaryCondition())
invoker.set_command(ModelAddAttribute('boundary_condition', 'special_point_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('boundary_condition', 'special_point_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('boundary_condition', 'special_point_coordinate', data_structure))
invoker.set_command(ModelInitialSpecialPoint())

entity_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface']
for each_grid_name in entity_list + cover_list + crack_list + ['boundary_condition']:
    invoker.set_command(ModelWriteFile(each_grid_name, data_structure))

# invoker.set_command(ModelGenerateElementList('matrix_element'))
# invoker.set_command(ModelMatrixSolve())
# invoker.set_command(ModelAssembleTotalMatrix())
# invoker.set_command(ModelRefreshCover())

invoker.press_button()

