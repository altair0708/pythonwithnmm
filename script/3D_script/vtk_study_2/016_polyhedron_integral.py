from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyhedron, VTK_POLYHEDRON, VTK_TETRA
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, reference
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from NMM.base.VTKBase.write_file import write_file
import numpy as np


vtk_points = vtkPoints()
vtk_points.InsertNextPoint((0, 0, 0))
vtk_points.InsertNextPoint((1, 0, 0))
vtk_points.InsertNextPoint((1, 1, 0))
vtk_points.InsertNextPoint((0, 1, 0))
vtk_points.InsertNextPoint((0, 0, 5))
vtk_points.InsertNextPoint((1, 0, 5))
vtk_points.InsertNextPoint((1, 1, 5))
vtk_points.InsertNextPoint((0, 1, 5))

face_list = [6,
             4, 0, 1, 3, 2,
             4, 0, 1, 5, 4,
             4, 0, 3, 7, 4,
             4, 2, 3, 7, 6,
             4, 1, 2, 6, 5,
             4, 4, 5, 6, 7]

face_id = vtkIdList()
[face_id.InsertNextId(i) for i in face_list]

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(vtk_points)
u_grid.InsertNextCell(VTK_POLYHEDRON, face_id)

delaunay = vtkDelaunay3D()
delaunay.SetInputData(u_grid)
delaunay.Update()
new_grid: vtkUnstructuredGrid = delaunay.GetOutput()
print([new_grid.GetCellTypesArray().GetValue(i) for i in range(6)])
new_grid.GetCellTypesArray().SetValue(0, 0)
print([new_grid.GetCellTypesArray().GetValue(i) for i in range(6)])

print(u_grid.GetCell(0).GetNumberOfFaces())
vtk_cell = u_grid.GetCell(0)
points = vtk_cell.GetPoints()

s = 0
p0 = (0, 0, 0)
for each_surface_id in range(vtk_cell.GetNumberOfFaces()):
    surface = vtk_cell.GetFace(each_surface_id)
    p1_id = surface.GetPointId(0)
    p1 = points.GetPoint(p1_id)
    for each_edge_id in range(surface.GetNumberOfEdges()):
        edge = surface.GetEdge(each_edge_id)
        p2_id = edge.GetPointId(0)
        p2 = points.GetPoint(p2_id)
        p3_id = edge.GetPointId(1)
        p3 = points.GetPoint(p3_id)
        temp_matrix = np.array([[p1[0], p1[1], p1[2]],
                                [p2[0], p2[1], p2[2]],
                                [p3[0], p3[1], p3[2]]])
        temp_s = (1 / 6) * (np.linalg.det(temp_matrix))
        s = s + temp_s

print(s)


write_file(u_grid, 're016_0.vtu')
write_file(new_grid, 're016_1.vtu')


