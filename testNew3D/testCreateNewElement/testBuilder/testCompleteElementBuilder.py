from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabaseBuilder import NmmDatabaseBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from NMM.base.Algorithm.ElementCreator.ElementDirector import ElementDirector
from NMM.base.Algorithm.ElementCreator.CompleteElementBuilder import CompleteElementBuilder
from NMM.base.Algorithm.ElementMatrixAssembler.CompleteElementMatrixAssembler import CompleteAssembler
from NMM.base.Algorithm.TotalMatrixAssembler import TotalMatrixAssembler
from NMM.base.Algorithm.CoverRefresher.CoverRefresher import CoverRefresher
from NMM.base.Algorithm.ElementRefresher.ElementRefresher import ElementRefresher
from NMM.base.Algorithm.SpecialPointRefresher.SpecialPointRefresher import SpecialPointRefresher
from NMM.base.LogBase.matrix_save import new_matrix_save
from scipy.sparse.linalg import cg, spsolve
import numpy as np
import shutil

shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/boundary_condition.vtu', '/Users/suboyi/PycharmProjects/pythonwithnmm/testNew3D/testCreateNewElement/testBuilder/boundary_condition.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/mathematics_point.vtu', '/Users/suboyi/PycharmProjects/pythonwithnmm/testNew3D/testCreateNewElement/testBuilder/mathematics_point.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/manifold_element.vtu', '/Users/suboyi/PycharmProjects/pythonwithnmm/testNew3D/testCreateNewElement/testBuilder/manifold_element.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/database.db', '/Users/suboyi/PycharmProjects/pythonwithnmm/testNew3D/testCreateNewElement/testBuilder/database.db')


builder = NmmDatabaseBuilder()
nmm_database = builder.build('database.db', False)


def test_complete_element_builder():
    mathematics_point = VtkGrid('mathematics_point', 'mathematics_point.vtu')
    manifold_element = VtkGrid('manifold_element', 'manifold_element.vtu')
    boundary_condition = VtkGrid('boundary_condition', 'boundary_condition.vtu')
    material_parameter = PropertyMap.generate_from_toml('material_parameter.toml')

    for step in range(1):

        director = ElementDirector()

        total_assembler = TotalMatrixAssembler(mathematics_point.get_cell_number())
        for each_id in range(manifold_element.get_cell_number()):

            complete_builder = CompleteElementBuilder(mathematics_point, manifold_element, boundary_condition, material_parameter)
            director.builder = complete_builder
            director.build_matrix_element(each_id)

            new_element = complete_builder.get_element()

            assembler = CompleteAssembler(new_element, step)
            assembler.update()

            total_assembler.add_element_matrix(new_element)
            total_assembler.add_force_vector(new_element)

        total_matrix, total_force = total_assembler.update()
        displacement_vector = spsolve(total_matrix, total_force)

        cover_refresher = CoverRefresher(displacement_vector, mathematics_point)
        cover_refresher.update()

        element_refresher = ElementRefresher(mathematics_point, manifold_element)
        element_refresher.update()

        special_point_refresher = SpecialPointRefresher(mathematics_point, boundary_condition)
        special_point_refresher.update()

    boundary_condition.write_file('test_boundary_condition.vtu')
    mathematics_point.write_file('test_mathematics_point.vtu')
    manifold_element.write_file('test_manifold_element.vtu')
