from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra
from vtkmodules.vtkCommonCore import vtkPoints

points = vtkPoints()
points.InsertPoint(0, (0, 0, 0))
points.InsertPoint(1, (1, 0, 0))
points.InsertPoint(2, (0, 1, 0))
points.InsertPoint(3, (0, 0, 1))

tetras = vtkTetra()
tetras.GetPointIds().SetId(0, 0)
tetras.GetPointIds().SetId(1, 1)
tetras.GetPointIds().SetId(2, 2)
tetras.GetPointIds().SetId(3, 3)

ugrid = vtkUnstructuredGrid()
ugrid.InsertNextCell(tetras.GetCellType(), tetras.GetPointIds())
ugrid.SetPoints(points)

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('simplex.vtu')
writer.SetInputData(ugrid)
writer.Write()

ugrid = vtkUnstructuredGrid()
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('special_points_simplex.vtu')
writer.SetInputData(ugrid)
writer.Write()
