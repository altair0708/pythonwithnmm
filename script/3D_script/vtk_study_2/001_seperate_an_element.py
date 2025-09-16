from vtkmodules.vtkCommonDataModel import vtkTetra, vtkTriangle, vtkLine, vtkVertex, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points_0 = vtkPoints()
points_0.InsertPoint(0, (0, 0, 0))
points_0.InsertPoint(1, (1, 0, 0))
points_0.InsertPoint(2, (0, 1, 0))
points_0.InsertPoint(3, (0, 0, 1))
print(type(points_0.GetPoint(0)))

tetra_0 = vtkTetra()
tetra_0.GetPointIds().SetId(0, 0)
tetra_0.GetPointIds().SetId(1, 1)
tetra_0.GetPointIds().SetId(2, 2)
tetra_0.GetPointIds().SetId(3, 3)

grid_0 = vtkUnstructuredGrid()
grid_0.SetPoints(points_0)
grid_0.InsertNextCell(tetra_0.GetCellType(), tetra_0.GetPointIds())

writer_0 = vtkXMLUnstructuredGridWriter()
writer_0.SetFileName('re001_0.vtu')
writer_0.SetInputData(grid_0)
writer_0.Write()

# ________Triangle_________
points_1 = vtkPoints()
points_1.InsertPoint(0, (0, 0, -0.5))
points_1.InsertPoint(1, (1, 0, -0.5))
points_1.InsertPoint(2, (0, 1, -0.5))

points_1.InsertPoint(3, (0, -0.5, 0))
points_1.InsertPoint(4, (1, -0.5, 0))
points_1.InsertPoint(5, (0, -0.5, 1))

points_1.InsertPoint(6, (-0.5, 0, 0))
points_1.InsertPoint(7, (-0.5, 1, 0))
points_1.InsertPoint(8, (-0.5, 0, 1))

points_1.InsertPoint(9, (1.3, 0.3, 0.3))
points_1.InsertPoint(10, (0.3, 1.3, 0.3))
points_1.InsertPoint(11, (0.3, 0.3, 1.3))

triangle_0 = vtkTriangle()
triangle_0.GetPointIds().SetId(0, 0)
triangle_0.GetPointIds().SetId(1, 1)
triangle_0.GetPointIds().SetId(2, 2)

triangle_1 = vtkTriangle()
triangle_1.GetPointIds().SetId(0, 3)
triangle_1.GetPointIds().SetId(1, 4)
triangle_1.GetPointIds().SetId(2, 5)

triangle_2 = vtkTriangle()
triangle_2.GetPointIds().SetId(0, 6)
triangle_2.GetPointIds().SetId(1, 7)
triangle_2.GetPointIds().SetId(2, 8)

triangle_3 = vtkTriangle()
triangle_3.GetPointIds().SetId(0, 9)
triangle_3.GetPointIds().SetId(1, 10)
triangle_3.GetPointIds().SetId(2, 11)

grid_1 = vtkUnstructuredGrid()
grid_1.SetPoints(points_1)
grid_1.InsertNextCell(triangle_0.GetCellType(), triangle_0.GetPointIds())
grid_1.InsertNextCell(triangle_1.GetCellType(), triangle_1.GetPointIds())
grid_1.InsertNextCell(triangle_2.GetCellType(), triangle_2.GetPointIds())
grid_1.InsertNextCell(triangle_3.GetCellType(), triangle_3.GetPointIds())

writer_1 = vtkXMLUnstructuredGridWriter()
writer_1.SetFileName('re001_1.vtu')
writer_1.SetInputData(grid_1)
writer_1.Write()

# _________Edge________
points_2 = vtkPoints()
points_2.InsertPoint(0, (-0.5, -0.5, 0))
points_2.InsertPoint(1, (-0.5, -0.5, 1))

points_2.InsertPoint(2, (0, -0.5, -0.5))
points_2.InsertPoint(3, (1, -0.5, -0.5))

points_2.InsertPoint(4, (-0.5, 0, -0.5))
points_2.InsertPoint(5, (-0.5, 1, -0.5))

points_2.InsertPoint(6, (0.35, -0.5, 1.35))
points_2.InsertPoint(7, (1.35, -0.5, 0.35))

points_2.InsertPoint(8, (-0.5, 0.35, 1.35))
points_2.InsertPoint(9, (-0.5, 1.35, 0.35))

points_2.InsertPoint(10, (0.35, 1.35, -0.5))
points_2.InsertPoint(11, (1.35, 0.35, -0.5))

edge_0 = vtkLine()
edge_0.GetPointIds().SetId(0, 0)
edge_0.GetPointIds().SetId(1, 1)

edge_1 = vtkLine()
edge_1.GetPointIds().SetId(0, 2)
edge_1.GetPointIds().SetId(1, 3)

edge_2 = vtkLine()
edge_2.GetPointIds().SetId(0, 4)
edge_2.GetPointIds().SetId(1, 5)

edge_3 = vtkLine()
edge_3.GetPointIds().SetId(0, 6)
edge_3.GetPointIds().SetId(1, 7)

edge_4 = vtkLine()
edge_4.GetPointIds().SetId(0, 8)
edge_4.GetPointIds().SetId(1, 9)

edge_5 = vtkLine()
edge_5.GetPointIds().SetId(0, 10)
edge_5.GetPointIds().SetId(1, 11)

grid_2 = vtkUnstructuredGrid()
grid_2.SetPoints(points_2)
grid_2.InsertNextCell(edge_0.GetCellType(), edge_0.GetPointIds())
grid_2.InsertNextCell(edge_1.GetCellType(), edge_1.GetPointIds())
grid_2.InsertNextCell(edge_2.GetCellType(), edge_2.GetPointIds())
grid_2.InsertNextCell(edge_3.GetCellType(), edge_3.GetPointIds())
grid_2.InsertNextCell(edge_4.GetCellType(), edge_4.GetPointIds())
grid_2.InsertNextCell(edge_5.GetCellType(), edge_5.GetPointIds())

writer_2 = vtkXMLUnstructuredGridWriter()
writer_2.SetFileName('re001_2.vtu')
writer_2.SetInputData(grid_2)
writer_2.Write()

# _________vertex__________
points_3 = vtkPoints()
points_3.InsertPoint(0, (-0.294, -0.294, -0.294))
points_3.InsertPoint(1, (1.5, -0.294, -0.294))
points_3.InsertPoint(2, (-0.294, 1.5, -0.294))
points_3.InsertPoint(3, (-0.294, -0.294, 1.5))

vertex_0 = vtkVertex()
vertex_0.GetPointIds().SetId(0, 0)

vertex_1 = vtkVertex()
vertex_1.GetPointIds().SetId(0, 1)

vertex_2 = vtkVertex()
vertex_2.GetPointIds().SetId(0, 2)

vertex_3 = vtkVertex()
vertex_3.GetPointIds().SetId(0, 3)

grid_3 = vtkUnstructuredGrid()
grid_3.SetPoints(points_3)
grid_3.InsertNextCell(vertex_0.GetCellType(), vertex_0.GetPointIds())
grid_3.InsertNextCell(vertex_1.GetCellType(), vertex_1.GetPointIds())
grid_3.InsertNextCell(vertex_2.GetCellType(), vertex_2.GetPointIds())
grid_3.InsertNextCell(vertex_3.GetCellType(), vertex_3.GetPointIds())

writer_3 = vtkXMLUnstructuredGridWriter()
writer_3.SetFileName('re001_3.vtu')
writer_3.SetInputData(grid_3)
writer_3.Write()
