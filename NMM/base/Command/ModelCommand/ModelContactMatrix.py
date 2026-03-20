from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase import entrance_cache, relationship_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.ElementCreator.ElementDirector import ElementDirector
from NMM.base.Algorithm.ElementCreator.ContactElementBuilder import ContactElementBuilder
from NMM.base.Algorithm.ContactTheory.ContactMatrixAssembler import ContactAssembler
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariable import GlobalVariable


class ModelContactMatrix(AbstractCommand):

    def __init__(self):
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__crack_surface: VtkGrid = entrance_cache.get_item('crack_surface_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')
        self.__boundary_condition = entrance_cache.get_item('boundary_condition_VtkGrid')

        self.__global_variable: GlobalVariable = entrance_cache.get_item('global_variable_Part')

        self.__matrix_solver: MatrixSolver = entrance_cache.get_item('matrix_solver_Part')

    def execute(self):
        crack_surface = self.__crack_surface
        new_cover = self.__new_cover
        boundary_condition = self.__boundary_condition
        material_parameter = self.__global_variable.get_property('material_parameter')
        time_step: int = self.__global_variable.get_variable('time_step')
        contact_list = self.__matrix_solver.get_property('contact_list')

        director = ElementDirector()

        contact_builder = ContactElementBuilder(new_cover, crack_surface, boundary_condition, material_parameter)

        for each_id, each_surface in enumerate(crack_surface):

            director.builder = contact_builder
            director.build_contact_element(each_id)
            temp_element = contact_builder.get_element()

            assembler = ContactAssembler(temp_element, time_step)
            assembler.update()

            contact_list.append(temp_element)
