from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabaseBuilder import NmmDatabaseBuilder
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariableBuilder import GlobalVariableBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from NMM.base.Algorithm.ElementCreator.ElementDirector import ElementDirector
from NMM.base.Algorithm.ElementCreator.CompleteElementBuilder import CompleteElementBuilder
from NMM.base.Algorithm.ElementCreator.SeparateElementBuilder import SeparateElementBuilder
from NMM.base.Algorithm.ElementMatrixAssembler.CompleteElementMatrixAssembler import CompleteAssembler
from NMM.base.Algorithm.ElementMatrixAssembler.SeparateElementMatrixAssembler import SeparateAssembler
from NMM.base.Algorithm.TotalMatrixAssembler import TotalMatrixAssembler
from NMM.base.Algorithm.CoverRefresher.CoverRefresherNew import CoverRefresher
from NMM.base.Algorithm.ElementRefresher.ElementRefresherNew import ElementRefresher
from NMM.base.Algorithm.SpecialPointRefresher.SpecialPointRefresher import SpecialPointRefresher
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.LogBase.matrix_save import new_matrix_save
from scipy.sparse.linalg import cg, spsolve
import numpy as np
import shutil

shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/boundary_condition.vtu', './boundary_condition.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/mathematics_point.vtu', './mathematics_point.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/manifold_element.vtu', './manifold_element.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/new_cover.vtu', './new_cover.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/new_element.vtu', './new_element.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/database.db', './database.db')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/global_variable.toml', 'global_variable.toml')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/grid_attribute.toml', 'grid_attribute.toml')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/material_parameter.toml', 'material_parameter.toml')

builder = NmmDatabaseBuilder()
nmm_database = builder.build('database.db', False)


def test_complete_element_builder():
    mathematics_point = VtkGrid('mathematics_point', 'mathematics_point.vtu')
    boundary_condition = VtkGrid('boundary_condition', 'boundary_condition.vtu')
    manifold_element = VtkGrid('manifold_element', 'manifold_element.vtu')
    new_element = VtkGrid('new_element', 'new_element.vtu')
    new_cover = VtkGrid('new_cover', 'new_cover.vtu')
    material_parameter = PropertyMap.generate_from_toml('material_parameter.toml')

    cover_number = mathematics_point.get_cell_number() + int(new_cover.get_cell_number() / 2)

    for step in range(3):

        director = ElementDirector()

        complete_builder = CompleteElementBuilder(mathematics_point, manifold_element, boundary_condition, material_parameter)
        separate_builder = SeparateElementBuilder(new_cover, new_element, boundary_condition, material_parameter)

        total_assembler = TotalMatrixAssembler(cover_number)
        element_list = []
        for each_id in range(manifold_element.get_cell_number()):
            cracked_status = manifold_element.get_cell_attribute('cracked', each_id)[0]

            if cracked_status == -1 or cracked_status == 8:
                director.builder = complete_builder
                director.build_matrix_element(each_id)
                temp_element = complete_builder.get_element()

                assembler = CompleteAssembler(temp_element, step)
                assembler.update()

                element_list.append(temp_element)
            elif cracked_status == 9:
                relationship_list = relationship_cache.get_item(name_0='element', name_1='newelement', id_0=each_id, id_1=None)
                assert len(relationship_list) == 2
                for each_relationship in relationship_list:
                    new_id = each_relationship['newelement']
                    director.builder = separate_builder
                    director.build_matrix_element(new_id)
                    temp_element = separate_builder.get_element()

                    assembler = SeparateAssembler(temp_element, step)
                    assembler.update()

                    element_list.append(temp_element)
            else:
                raise Exception('Crack status error!!!')

        for each_element in element_list:
            total_assembler.add_element_matrix(each_element)
            total_assembler.add_force_vector(each_element)

        total_matrix, total_force = total_assembler.update()
        displacement_vector = spsolve(total_matrix, total_force)

        cover_refresher = CoverRefresher(displacement_vector, mathematics_point, new_cover)
        cover_refresher.update()

        element_refresher = ElementRefresher(mathematics_point, manifold_element, new_cover, new_element)
        element_refresher.update()

        special_point_refresher = SpecialPointRefresher(mathematics_point, boundary_condition)
        special_point_refresher.update()

    mathematics_point.write_file('test_mathematics_point.vtu')
    new_cover.write_file('test_new_cover.vtu')
    manifold_element.write_file('test_manifold_element.vtu')
    new_element.write_file('test_new_element.vtu')
