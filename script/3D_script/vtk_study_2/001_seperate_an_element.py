from vtkmodules.vtkCommonDataModel import vtkTetra, vtkTriangle, vtkLine, vtkVertex, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points_0 = vtkPoints()
points_0.InsertPoint(0, (0, 0, 0))
points_0.InsertPoint(1, (1, 0, 0))
points_0.InsertPoint(2, (0, 1, 0))
points_0.InsertPoint(3, (0, 0, 1))

tetra_0 = vtkTetra()
tetra_0.GetPointIds().SetId(0, 0)
tetra_0.GetPointIds().SetId(1, 1)
tetra_0.GetPointIds().SetId(2, 2)
tetra_0.GetPointIds().SetId(3, 3)

gird_0 = vtkUnstructuredGrid()
gird_0.SetPoints(points_0)
gird_0.InsertNextCell(tetra_0.GetCellType(), tetra_0.GetPointIds())

writer_0 = vtkXMLUnstructuredGridWriter()
writer_0.SetFileName('re001_0.vtu')
writer_0.SetInputData(gird_0)
writer_0.Write()

# ________Triangle_0_________
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

gird_1 = vtkUnstructuredGrid()
gird_1.SetPoints(points_1)
gird_1.InsertNextCell(triangle_0.GetCellType(), triangle_0.GetPointIds())
gird_1.InsertNextCell(triangle_1.GetCellType(), triangle_1.GetPointIds())
gird_1.InsertNextCell(triangle_2.GetCellType(), triangle_2.GetPointIds())
gird_1.InsertNextCell(triangle_3.GetCellType(), triangle_3.GetPointIds())

writer_1 = vtkXMLUnstructuredGridWriter()
writer_1.SetFileName('re001_1.vtu')
writer_1.SetInputData(gird_1)
writer_1.Write()
