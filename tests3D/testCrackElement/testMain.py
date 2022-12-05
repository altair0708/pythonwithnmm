import sys

from NMM.crack_3D.CrackElementBase3D import CrackedElement3D
from NMM.base.ModifyVtkCell import insert_a_cell
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from tests3D.object.tetra_polyhedron import generate_tetra_polyhedron


temp_cell, temp_cell_list, temp_point_list = generate_tetra_polyhedron()

# new crack element
temp_element = CrackedElement3D(id_value=0)

# strain_total
temp_element.strain_total = (3, 2, 1, 0, 0, 0)

# vtk_cell
temp_element.vtk_cell = temp_cell

# cracked flag
temp_element.cracked = 2
temp_element.crack_edge_number = 1

# crack edge
temp_element.crack_edge[0].append((0.5, 0, 0))
temp_element.crack_edge[0].append((0.5, 0, 0.5))

# temp_element.crack_edge[1].append((0.5, 0, 0))
# temp_element.crack_edge[1].append((0.25, 0, 0.75))

# adjacent element
points_1 = vtkPoints()
points_1.InsertNextPoint((0, 0, 0))
points_1.InsertNextPoint((1, 0, 0))
points_1.InsertNextPoint((0, 1, 0))
points_2 = vtkPoints()
points_2.InsertNextPoint((0, 0, 0))
points_2.InsertNextPoint((1, 0, 0))
points_2.InsertNextPoint((0, 0, 1))
points_3 = vtkPoints()
points_3.InsertNextPoint((0, 0, 0))
points_3.InsertNextPoint((0, 1, 0))
points_3.InsertNextPoint((0, 0, 1))
points_4 = vtkPoints()
points_4.InsertNextPoint((1, 0, 0))
points_4.InsertNextPoint((0, 1, 0))
points_4.InsertNextPoint((0, 0, 1))
face_dictionary = [{'face_id': 0, 'adjacent_cell_id': 0, 'face_points': points_1},
                   {'face_id': 1, 'adjacent_cell_id': 1, 'face_points': points_2},
                   {'face_id': 2, 'adjacent_cell_id': 2, 'face_points': points_3},
                   {'face_id': 3, 'adjacent_cell_id': 3, 'face_points': points_4}]
temp_element.adjacent_element = face_dictionary

temp_element.generate_crack_surface()
[print(i) for i in face_dictionary]

# write into file
# element
u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(temp_point_list)
u_grid.InsertNextCell(VTK_POLYHEDRON, temp_cell_list)

# surface
insert_a_cell(u_grid, temp_element.crack_surface)

# writer
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('test.vtu')
writer.SetInputData(u_grid)
writer.Write()

