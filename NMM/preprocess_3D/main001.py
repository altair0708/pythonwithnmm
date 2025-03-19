from NMM.preprocess_3D.Model.ModelBuilder import PreprocessModelBuilder
from NMM.base.Command.Invoker import Invoker, InvokerQueue
from NMM.base.Command.ModelCommand.ModelAddAttribute import ModelAddAttribute
from NMM.base.Command.ModelCommand.ModelGetPath import ModelGetPath
from NMM.base.Command.ModelCommand.ModelGenerateBoundaryCondition import ModelGenerateBoundaryCondition
from NMM.base.Command.ModelCommand.ModelInitialCrack import ModelInitialCrack
from NMM.base.Command.ModelCommand.ModelWriteFile import ModelWriteFile
from NMM.base.Command.ModelCommand.ModelGenerateGrid import ModelGenerateGrid
from NMM.base.Command.ModelCommand.ModelInitialSpecialPoint import ModelInitialSpecialPoint
from NMM.base.Command.ModelCommand.ModelInitialMathPoint import ModelInitialMathPoint
from NMM.base.Command.ModelCommand.ModelGenerateElementList import ModelGenerateElementList
from NMM.base.Command.ModelCommand.ModelAssembleTotalMatrix import ModelAssembleTotalMatrix
from NMM.base.Command.ModelCommand.ModelRefreshCover import ModelRefreshCover
from NMM.base.Command.ModelCommand.ModelMatrixSolve import ModelMatrixSolve


builder = PreprocessModelBuilder()
# model = builder.build('D:/science/NMM/python-NMM/example/example001')
model = builder.build('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001')

invoker = InvokerQueue()

data_structure = model.get_property('data_structure')
file_path = model.get_property('file_path')
element_list = model.get_property('matrix_element')
nmm_database = model.get_property('database')

entity_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
for each_entity_name in entity_list:
    invoker.set_command(ModelGenerateGrid(each_entity_name, data_structure))
    invoker.set_command(ModelAddAttribute(each_entity_name, 'point_id', data_structure))
    invoker.set_command(ModelAddAttribute(each_entity_name, 'cell_id', data_structure))

cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface']
for each_entity_name in cover_list:
    invoker.set_command(ModelGenerateGrid(each_entity_name, data_structure))
    invoker.set_command(ModelAddAttribute(each_entity_name, 'point_id', data_structure))
    invoker.set_command(ModelAddAttribute(each_entity_name, 'cell_id', data_structure))
    invoker.set_command(ModelAddAttribute(each_entity_name, 'cracked', data_structure))

invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_displacement', data_structure))
invoker.set_command(ModelInitialMathPoint())

crack_list = ['crack_surface', 'crack_edge', 'new_cover', 'new_element', 'new_surface']
for each_entity_name in crack_list:
    invoker.set_command(ModelAddAttribute(each_entity_name, 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'real', data_structure))
invoker.set_command(ModelInitialCrack())

invoker.set_command(ModelGenerateBoundaryCondition())
invoker.set_command(ModelInitialSpecialPoint())

for each_grid_name in entity_list + cover_list + crack_list + ['boundary_condition']:
    invoker.set_command(ModelWriteFile(each_grid_name, data_structure))

# invoker.set_command(ModelGenerateElementList('matrix_element'))
# invoker.set_command(ModelMatrixSolve())
# invoker.set_command(ModelAssembleTotalMatrix())
# invoker.set_command(ModelRefreshCover())

invoker.press_button()

