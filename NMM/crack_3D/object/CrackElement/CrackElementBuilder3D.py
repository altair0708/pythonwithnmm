from NMM.base.GeometricEntity.Property.Implement.CrackStatus import CrackStatus
from NMM.base.GeometricEntity.Property.Implement.ObjectId import ObjectId
from NMM.base.GeometricEntity.GeometricEntityBase import GeometricEntityBase
from NMM.crack_3D.object.ObjectBuilderInterface import AbstractObjectBuilder
from NMM.GlobalVariable import DataStructure
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell


# todo: try to create a crack element.
class CrackElement3D(AbstractObjectBuilder):
    def builder(self, id_value, data_structure: DataStructure):
        new_element = GeometricEntityBase()

        element_id = ObjectId(id_value)
        new_element.add_property(element_id)

        element_crack_status = CrackStatus(0)
        new_element.add_property(element_crack_status)

        # element_vtk_cell_grid
        element_grid: vtkUnstructuredGrid = data_structure.manifold_element.content
        element_vtk_cell: vtkCell = element_grid.GetCell(element_id)
        element_grid_points: vtkPoints = element_grid.GetPoints()
        element_cell.vtk_cell = copy_polyhedron(element_vtk_cell, element_grid_points)

        return new_element
