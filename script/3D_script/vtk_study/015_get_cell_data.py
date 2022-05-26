from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData, vtkTetra, vtkGenericCell, vtkVertex
from vtkmodules.vtkCommonCore import vtkDataArray, reference, vtkPoints

gmsh_reader = vtkXMLUnstructuredGridReader()
gmsh_reader.SetFileName('../../../data_3D/manifold_element.vtu')
gmsh_reader.Update()
uGrid: vtkUnstructuredGrid = gmsh_reader.GetOutput()
tempCell = vtkGenericCell()
subId = reference(0)
result: vtkTetra = uGrid.FindAndGetCell((0.51, 0.51, 0.51), tempCell, 0, 0.0, subId, [0, 0, 0], [0, 0, 0, 0])

temp_list: vtkPoints = uGrid.GetPoints()
point_id = temp_list.GetNumberOfPoints()
temp_list.InsertPoint(point_id, (0.51, 0.51, 0.51))
print(point_id)
print(temp_list.GetNumberOfPoints())

temp_point = vtkVertex()
temp_point.GetPointIds().SetId(0, point_id)

cell_grid = vtkUnstructuredGrid()
cell_grid.InsertNextCell(result.GetCellType(), result.GetPointIds())
cell_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())
cell_grid.SetPoints(temp_list)

temp_cell_writer = vtkXMLUnstructuredGridWriter()
temp_cell_writer.SetFileName('temp_cell.vtu')
temp_cell_writer.SetInputData(cell_grid)
temp_cell_writer.Write()

