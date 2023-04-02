from vtkmodules.vtkCommonDataModel import vtkQuadraticPolygon, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


quadraticPolygon = vtkQuadraticPolygon()

quadraticPolygon.GetPointIds().SetNumberOfIds(8)
quadraticPolygon.GetPointIds().SetId(0, 0)
quadraticPolygon.GetPointIds().SetId(1, 1)
quadraticPolygon.GetPointIds().SetId(2, 2)
quadraticPolygon.GetPointIds().SetId(3, 3)
quadraticPolygon.GetPointIds().SetId(4, 4)
quadraticPolygon.GetPointIds().SetId(5, 5)
quadraticPolygon.GetPointIds().SetId(6, 6)
quadraticPolygon.GetPointIds().SetId(7, 7)

quadraticPolygon.GetPoints().SetNumberOfPoints(8)
quadraticPolygon.GetPoints().SetPoint(0, 0.0, 0.0, 0.0)
quadraticPolygon.GetPoints().SetPoint(1, 2.0, 0.0, 0.0)
quadraticPolygon.GetPoints().SetPoint(2, 2.0, 2.0, 1.0)
quadraticPolygon.GetPoints().SetPoint(3, 0.0, 2.0, 0.0)
quadraticPolygon.GetPoints().SetPoint(4, 1.0, 0.0, 0.0)
quadraticPolygon.GetPoints().SetPoint(5, 2.0, 1.0, 1.0)
quadraticPolygon.GetPoints().SetPoint(6, 1.0, 2.0, 0.5)
quadraticPolygon.GetPoints().SetPoint(7, 0.0, 1.0, 0.0)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(quadraticPolygon.GetPoints())
u_grid.InsertNextCell(quadraticPolygon.GetCellType(),quadraticPolygon.GetPointIds())

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName('re019_0.vtu')
writer.Write()

