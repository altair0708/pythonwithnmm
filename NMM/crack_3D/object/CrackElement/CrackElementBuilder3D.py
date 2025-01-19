from NMM.base.Property.Implement.CrackStatus import CrackStatus
from NMM.base.Property.Implement.PropertyId import PropertyIndex
from NMM.base.GeometricEntity.GeometricEntityBase import GeometricEntityBase
from NMM.crack_3D.object.ObjectBuilderInterface import AbstractObjectBuilder
from NMM.GlobalVariable import DataStructure
from NMM.base.VTKBase.Implement.VTKBase import VTKBase
from NMM.base.PropertyGetSetFunction import get_property
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


class CrackElement3D(AbstractObjectBuilder):
    def builder(self, id_value, data_structure: DataStructure):
        # new_element
        new_element = GeometricEntityBase()

        # vtk_grid
        element_grid: vtkUnstructuredGrid = data_structure.manifold_element.content

        element_id = PropertyIndex(id_value)
        new_element.add_property(element_id)

        crack_status = get_property(element_grid, 'cracked', id_value)
        element_crack_status = CrackStatus(crack_status)
        new_element.add_property(element_crack_status)

        # element_vtk_cell_grid
        element_vtk_cell_grid = VTKBase.get_a_vtk_cell_grid(element_grid, id_value)
        new_element.add_property(element_vtk_cell_grid)

        return new_element
