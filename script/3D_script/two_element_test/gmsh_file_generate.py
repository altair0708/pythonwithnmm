from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


vtk_points = vtkPoints()
vtk_points.InsertNextPoint(0, 0, 0)
vtk_points.InsertNextPoint(1, 0, 0)
vtk_points.InsertNextPoint(0, 1, 0)
vtk_points.InsertNextPoint(0, 0, 1)
vtk_points.InsertNextPoint(-1, 0, 0)

cell_0 = vtkTetra()
cell_0.GetPointIds().SetId(0, 0)
cell_0.GetPointIds().SetId(1, 1)
cell_0.GetPointIds().SetId(2, 2)
cell_0.GetPointIds().SetId(3, 3)

cell_1 = vtkTetra()
cell_1.GetPointIds().SetId(0, 0)
cell_1.GetPointIds().SetId(1, 4)
cell_1.GetPointIds().SetId(2, 2)
cell_1.GetPointIds().SetId(3, 3)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(vtk_points)
u_grid.InsertNextCell(cell_0.GetCellType(), cell_0.GetPointIds())
u_grid.InsertNextCell(cell_1.GetCellType(), cell_1.GetPointIds())

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName('gmsh_file.vtu')
writer.Write()






