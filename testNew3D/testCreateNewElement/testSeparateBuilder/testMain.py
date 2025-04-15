from NMM.base.Algorithm.ElementCreator.SeparateElementBuilder import SeparateElementBuilder
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

shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/new_cover.vtu', 'new_cover.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/new_element.vtu', 'new_element.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/boundary_condition.vtu', 'boundary_condition.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/geometry/database.db', 'database.db')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/material_parameter.toml', 'material_parameter.toml')

builder = NmmDatabaseBuilder()
nmm_database = builder.build('database.db', False)


def test_separate_element_builder():
    new_cover = VtkGrid('new_cover', 'new_cover.vtu')
    new_element = VtkGrid('new_element', 'new_element.vtu')
    boundary_condition = VtkGrid('boundary_condition', 'boundary_condition.vtu')
    material_parameter = PropertyMap.generate_from_toml('material_parameter.toml')

    element_builder = SeparateElementBuilder(new_cover, new_element, boundary_condition, material_parameter)
    element_builder.set_simple_properties(0)
    element_builder.set_vertexes(0)
    element_builder.set_material_parameters(0)
    element_builder.set_patches(0)
    element_builder.set_special_points(0)
    new_element = element_builder.get_element()
    print(new_element.get_property('point_coordinate').value)
