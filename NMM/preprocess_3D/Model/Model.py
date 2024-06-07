from NMM.base.Model.Model import Model
from NMM.base.singleton import singleton
from NMM.base.Command.Invoker import Invoker, InvokerQueue
from NMM.base.Command.ModelCommand.ModelGenerateGeometricGrid import ModelGenerateGeometricGrid
from NMM.base.Command.ModelCommand.ModelGenerateCover import ModelGenerateCover
from NMM.base.Command.ModelCommand.ModelAddAttribute import ModelAddAttribute
from NMM.base.Command.ModelCommand.ModelGetPath import ModelGetPath
from NMM.base.Command.ModelCommand.ModelWriteFile import ModelWriteFile
import os


@singleton
class PreprocessModel(Model):
    def initial(self):
        invoker = InvokerQueue()

        data_structure = self.get_property('data_structure')
        file_path = self.get_property('file_path')
        geometric_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
        for each_geometric_name in geometric_list:
            invoker.set_command(ModelGenerateGeometricGrid(each_geometric_name, data_structure))

        cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element']
        for each_cover_name in cover_list:
            invoker.set_command(ModelGenerateCover(each_cover_name, data_structure))
            invoker.set_command(ModelAddAttribute(each_cover_name, 'point_id', data_structure))
            invoker.set_command(ModelAddAttribute(each_cover_name, 'cell_id', data_structure))

        temp_invoker = Invoker()
        temp_invoker.set_command(ModelGetPath('geometry_path', file_path))
        geometry_path = temp_invoker.press_button()
        for each_grid_name in cover_list:
            path = os.path.normpath(f'{geometry_path}/{each_grid_name}.vtu')
            invoker.set_command(ModelWriteFile(each_grid_name, path, data_structure))

        invoker.press_button()
