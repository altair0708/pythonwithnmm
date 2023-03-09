from vtkmodules.vtkCommonDataModel import vtkTetra, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)
points.InsertNextPoint(-1, 0, 0)
points.InsertNextPoint(0, -1, 0)
points.InsertNextPoint(0, 0, -1)

tetra_0 = vtkTetra()
tetra_0.GetPointIds().SetId(0, 0)
tetra_0.GetPointIds().SetId(1, 1)
tetra_0.GetPointIds().SetId(2, 2)
tetra_0.GetPointIds().SetId(3, 3)

tetra_1 = vtkTetra()
tetra_1.GetPointIds().SetId(0, 0)
tetra_1.GetPointIds().SetId(1, 4)
tetra_1.GetPointIds().SetId(2, 2)
tetra_1.GetPointIds().SetId(3, 3)

tetra_2 = vtkTetra()
tetra_2.GetPointIds().SetId(0, 0)
tetra_2.GetPointIds().SetId(1, 1)
tetra_2.GetPointIds().SetId(2, 5)
tetra_2.GetPointIds().SetId(3, 3)

tetra_3 = vtkTetra()
tetra_3.GetPointIds().SetId(0, 0)
tetra_3.GetPointIds().SetId(1, 1)
tetra_3.GetPointIds().SetId(2, 2)
tetra_3.GetPointIds().SetId(3, 6)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(tetra_0.GetCellType(), tetra_0.GetPointIds())
u_grid.InsertNextCell(tetra_1.GetCellType(), tetra_1.GetPointIds())
u_grid.InsertNextCell(tetra_2.GetCellType(), tetra_2.GetPointIds())
u_grid.InsertNextCell(tetra_3.GetCellType(), tetra_3.GetPointIds())

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('gmsh_file.vtu')
writer.SetInputData(u_grid)
writer.Write()

