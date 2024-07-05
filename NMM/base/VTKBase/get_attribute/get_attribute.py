# TODO
# Entrance of the function
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from NMM.base.VTKBase.get_attribute.get_cover_element_id import get_cover_element_relationship


def get_attribute(vtk_model: vtkUnstructuredGrid, id_value: int, attribute_name: str):
    if 'cover_element' == attribute_name:
        return get_cover_element_relationship(vtk_model, id_value)
