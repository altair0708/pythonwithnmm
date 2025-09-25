from NMM.preprocess_3D.Model.ModelBuilder import PreprocessModelBuilder
from NMM.base.Command.Invoker import Invoker, InvokerQueue, InvokerCycle
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
from NMM.base.Command.ModelCommand.ModelInitialNewElement import ModelInitialNewElement
from NMM.base.Command.ModelCommand.ModelInitialNewCover import ModelInitialNewCover
from NMM.base.Command.ModelCommand.ModelMatrixSolve import ModelMatrixSolve
from NMM.base.Command.ModelCommand.ModelGenerateElementList import ModelGenerateElementList
from NMM.base.Command.ModelCommand.ModelRefreshCover import ModelRefreshCover
from NMM.base.Command.ModelCommand.ModelRefreshElement import ModelRefreshElement
from NMM.base.Command.ModelCommand.ModelRefreshNewElement import ModelRefreshNewElement
from NMM.base.Command.ModelCommand.ModelRefreshBoundaryCondition import ModelRefreshBoundaryCondition
from NMM.base.Command.ModelCommand.ModelOutputResult import ModelOutputResult
from NMM.base.Command.ModelCommand.ModelCrackElement import ModelCrackElement
from NMM.base.Command.ModelCommand.ModelCrackElementGlobal import ModelCrackElementGlobal
from NMM.base.Command.ModelCommand.ModelCopyCoverAttribute import ModelCopyCoverAttribute
from NMM.base.Command.ModelCommand.ModelGenerateCrackTip import ModelGenerateCrackTip
from NMM.base.Command.ModelCommand.ModelInitialCrackTip import ModelInitialCrackTip
from NMM.base.Command.ModelCommand.ModelGenerateGeometricShell import ModelGenerateGeometricShell
from NMM.base.Command.ModelCommand.ModelCrackPropagate import ModelCrackPropagate


builder = PreprocessModelBuilder()
# model = builder.build('D:/science/NMM/python-NMM/example/example001')
model = builder.build('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example012')

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
invoker.set_command(ModelGenerateGeometricShell(data_structure))

invoker.set_command(ModelGenerateGrid('mathematics_cover', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_cover', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_cover', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_cover', 'cracked', data_structure))

invoker.set_command(ModelGenerateMathematicsPoint(data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'cracked', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('mathematics_point', 'math_cover_velocity', data_structure))
invoker.set_command(ModelInitialMathPoint())

invoker.set_command(ModelGenerateManifoldElement(data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'cracked', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'material_id', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'point_velocity', data_structure))
invoker.set_command(ModelAddAttribute('manifold_element', 'initial_strain_total', data_structure))
invoker.set_command(ModelInitialManifoldElement())

invoker.set_command(ModelGenerateGrid('element_surface', data_structure))
invoker.set_command(ModelAddAttribute('element_surface', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('element_surface', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('element_surface', 'cracked', data_structure))

invoker.set_command(ModelGenerateCrackTip(data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'line_on_shell', data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'point_on_shell', data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'crack_point_type', data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'propagate_direction', data_structure))
invoker.set_command(ModelAddAttribute('crack_tip', 'propagate_vector', data_structure))
invoker.set_command(ModelAddAttribute('crack_propagation', 'cell_id', data_structure))

invoker.set_command(ModelAddAttribute('crack_surface', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('crack_edge', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'real', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'total_id', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'cell_id', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'total_id', data_structure))
invoker.set_command(ModelAddAttribute('new_surface', 'cell_id', data_structure))
# invoker.set_command(ModelInitialCrack())
invoker.set_command(ModelInitialCrackTip())

# invoker.set_command(ModelAddAttribute('new_cover', 'point_id', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'math_cover_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'math_cover_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'math_cover_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('new_cover', 'math_cover_velocity', data_structure))
invoker.set_command(ModelCopyCoverAttribute())

invoker.set_command(ModelAddAttribute('new_element', 'material_id', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'point_coordinate', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'point_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'point_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'point_velocity', data_structure))
invoker.set_command(ModelAddAttribute('new_element', 'initial_strain_total', data_structure))
invoker.set_command(ModelRefreshNewElement())

invoker.set_command(ModelGenerateBoundaryCondition())
invoker.set_command(ModelAddAttribute('boundary_condition', 'special_point_displacement_total', data_structure))
invoker.set_command(ModelAddAttribute('boundary_condition', 'special_point_displacement_increment', data_structure))
invoker.set_command(ModelAddAttribute('boundary_condition', 'special_point_coordinate', data_structure))
invoker.set_command(ModelInitialSpecialPoint())

grid_list = ['crack_surface', 'crack_edge', 'new_cover', 'new_element', 'new_surface',
             'geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron', 'geometric_shell',
             'mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface',
             'boundary_condition', 'crack_tip', 'crack_propagation']
for each_grid_name in grid_list:
    invoker.set_command(ModelWriteFile(each_grid_name, data_structure))

invoker.press_button()

invoker_cycle = InvokerCycle()
invoker_cycle.set_command(ModelGenerateElementList())
invoker_cycle.set_command(ModelMatrixSolve())
invoker_cycle.set_command(ModelRefreshCover())
invoker_cycle.set_command(ModelRefreshElement())
invoker_cycle.set_command(ModelRefreshBoundaryCondition())

invoker_cycle.set_command(ModelCrackPropagate())
invoker_cycle.set_command(ModelCrackElementGlobal())
invoker_cycle.set_command(ModelCopyCoverAttribute())
invoker_cycle.set_command(ModelRefreshNewElement())

invoker_cycle.set_command(ModelGenerateElementList())
invoker_cycle.set_command(ModelMatrixSolve())
invoker_cycle.set_command(ModelRefreshCover())
invoker_cycle.set_command(ModelRefreshElement())
invoker_cycle.set_command(ModelRefreshBoundaryCondition())

invoker_cycle.set_command(ModelOutputResult('mathematics_point'))
invoker_cycle.set_command(ModelOutputResult('manifold_element'))
invoker_cycle.set_command(ModelOutputResult('new_cover'))
invoker_cycle.set_command(ModelOutputResult('new_element'))
invoker_cycle.set_command(ModelOutputResult('crack_surface'))
invoker_cycle.set_command(ModelOutputResult('crack_tip'))
invoker_cycle.set_command(ModelOutputResult('crack_propagation'))

invoker_cycle.press_button()

