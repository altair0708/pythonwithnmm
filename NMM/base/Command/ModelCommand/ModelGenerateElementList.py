from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase import entrance_cache, relationship_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCreator.ElementDirector import ElementDirector
from NMM.base.Algorithm.ElementCreator.CompleteElementBuilder import CompleteElementBuilder
from NMM.base.Algorithm.ElementCreator.SeparateElementBuilder import SeparateElementBuilder
from NMM.base.Algorithm.ElementMatrixAssembler.CompleteElementMatrixAssembler import CompleteAssembler
from NMM.base.Algorithm.ElementMatrixAssembler.SeparateElementMatrixAssembler import SeparateAssembler
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariable import GlobalVariable
from NMM.preprocess_3D.Part.ElementList.ElementList import ElementList
from NMM.base.Algorithm.ElementCreator.MatrixElementCreator import MatrixElementCreator


class ModelGenerateElementList(AbstractCommand):

    def __init__(self):
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')
        self.__boundary_condition = entrance_cache.get_item('boundary_condition_VtkGrid')

        self.__global_variable: GlobalVariable = entrance_cache.get_item('global_variable_Part')

        self.__matrix_solver: MatrixSolver = entrance_cache.get_item('matrix_solver_Part')

    def execute(self):
        mathematics_point = self.__mathematics_point
        manifold_element = self.__manifold_element
        new_cover = self.__new_cover
        new_element = self.__new_element
        boundary_condition = self.__boundary_condition
        element_list = self.__matrix_solver.get_property('element_list')
        material_parameter = self.__global_variable.get_property('material_parameter')
        time_step: int = self.__global_variable.get_variable('time_step')

        director = ElementDirector()

        complete_builder = CompleteElementBuilder(mathematics_point, manifold_element, boundary_condition, material_parameter)
        separate_builder = SeparateElementBuilder(new_cover, new_element, boundary_condition, material_parameter)

        for each_id in range(manifold_element.get_cell_number()):
            cracked_status = manifold_element.get_cell_attribute('cracked', each_id)[0]

            if cracked_status == -1 or cracked_status == 8:
                director.builder = complete_builder
                director.build_matrix_element(each_id)
                temp_element = complete_builder.get_element()

                assembler = CompleteAssembler(temp_element, time_step)
                assembler.update()

                element_list.append(temp_element )
            elif cracked_status == 9:
                relationship_list = relationship_cache.get_item(name_0='element', name_1='newelement', id_0=each_id, id_1=None)
                assert len(relationship_list) == 2
                for each_relationship in relationship_list:
                    new_id = each_relationship['newelement']
                    director.builder = separate_builder
                    director.build_matrix_element(new_id)
                    temp_element = separate_builder.get_element()

                    assembler = SeparateAssembler(temp_element, time_step)
                    assembler.update()

                    element_list.append(temp_element )
            else:
                raise Exception('Crack status error!!!')

