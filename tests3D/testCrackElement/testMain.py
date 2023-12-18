import sys
from NMM.crack_3D.ElementBase3D import Element3D
from NMM.base.ModifyVtkCell import insert_a_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from tests3D.object.tetra_polyhedron import generate_tetra_polyhedron


temp_cell, temp_cell_list, temp_point_list = generate_tetra_polyhedron()

# new crack element
temp_element = Element3D(id_value=0)

# strain_total
temp_element.strain_total = (3, 2, 1, 0, 0, 0)

# stress_total
temp_element.stress_total = (1, 2, 3, 0, 1, 0)

# vtk_cell
temp_element.vtk_cell = temp_cell

# cracked flag
temp_element.cracked = 2

print(temp_element.stress.component_vector_1)
