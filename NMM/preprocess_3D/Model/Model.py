from NMM.base.Model.Model import Model
from NMM.base.singleton import singleton
from NMM.base.Command.Invoker import Invoker, InvokerQueue
from NMM.base.Command.ModelCommand.ModelAddAttribute import ModelAddAttribute
from NMM.base.Command.ModelCommand.ModelGetPath import ModelGetPath
from NMM.base.Command.ModelCommand.ModelWriteFile import ModelWriteFile
from NMM.base.Command.ModelCommand.ModelGenerateGrid import ModelGenerateGrid


@singleton
class PreprocessModel(Model):
    def initial(self):
        invoker = InvokerQueue()

        data_structure = self.get_property('data_structure')
        file_path = self.get_property('file_path')
        element_list = self.get_property('preprocess_element_list')
        nmm_database = self.get_property('database')

        entity_list = ['geometric_vertex', 'geometric_line', 'geometric_surface', 'geometric_tetrahedron']
        for each_entity_name in entity_list:
            invoker.set_command(ModelGenerateGrid(each_entity_name, data_structure))
            invoker.set_command(ModelAddAttribute(each_entity_name, 'point_id', data_structure))
            invoker.set_command(ModelAddAttribute(each_entity_name, 'cell_id', data_structure))

        cover_list = ['mathematics_cover', 'mathematics_point', 'manifold_element', 'element_surface']
        for each_entity_name in cover_list:
            invoker.set_command(ModelGenerateGrid(each_entity_name, data_structure))
            invoker.set_command(ModelAddAttribute(each_entity_name, 'cracked', data_structure))

        # crack_list = ['crack_surface', 'crack_edge', 'new_cover', 'new_element', 'new_surface']
        # crack_list = ['crack_surface', 'crack_edge', 'new_element']
        crack_list = ['crack_surface', 'crack_edge']
        # crack_list = ['crack_surface']
        for each_entity_name in crack_list:
            invoker.set_command(ModelGenerateGrid(each_entity_name, data_structure))

        temp_invoker = Invoker()
        for each_grid_name in entity_list + cover_list + crack_list + ['new_element']:
            temp_invoker.set_command(ModelGetPath(each_grid_name, file_path))
            geometry_path = temp_invoker.press_button()
            invoker.set_command(ModelWriteFile(each_grid_name, geometry_path, data_structure))

        invoker.press_button()
