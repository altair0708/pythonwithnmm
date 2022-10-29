from vtkmodules.vtkCommonDataModel import vtkPolygon, vtkUnstructuredGrid, vtkCellArray, VTK_POLYHEDRON, vtkEmptyCell
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray, vtkIdList, vtkIdTypeArray

polygon_1 = vtkPolygon()
polygon_1.GetPointIds().SetNumberOfIds(3)
polygon_1.GetPointIds().SetId(0, 0)
polygon_1.GetPointIds().SetId(1, 1)
polygon_1.GetPointIds().SetId(2, 2)

polygon_2 = vtkPolygon()
polygon_2.GetPointIds().SetNumberOfIds(3)
polygon_2.GetPointIds().SetId(0, 1)
polygon_2.GetPointIds().SetId(1, 2)
polygon_2.GetPointIds().SetId(2, 3)

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0.5, 0.5, 1)

polyhedron_list = vtkIdList()
polyhedron_list.InsertNextId(4)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(0)
polyhedron_list.InsertNextId(1)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(1)
polyhedron_list.InsertNextId(2)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(2)
polyhedron_list.InsertNextId(0)

polyhedron_list.InsertNextId(3)
polyhedron_list.InsertNextId(2)
polyhedron_list.InsertNextId(1)
polyhedron_list.InsertNextId(0)

poly_data = vtkUnstructuredGrid()
poly_data.SetPoints(points)
poly_data.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())
poly_data.InsertNextCell(polygon_2.GetCellType(), polygon_2.GetPointIds())

poly_data_writer = vtkXMLUnstructuredGridWriter()
poly_data_writer.SetInputData(poly_data)
poly_data_writer.SetFileName('poly_data.vtu')
poly_data_writer.Write()

polygon_3 = vtkPolygon()
polygon_3.GetPointIds().SetNumberOfIds(3)
polygon_3.GetPointIds().SetId(0, 4)
polygon_3.GetPointIds().SetId(1, 5)
polygon_3.GetPointIds().SetId(2, 6)

points_1 = vtkPoints()
points_1.InsertNextPoint(0, 0, 1)
points_1.InsertNextPoint(1, 0, 1)
points_1.InsertNextPoint(0, 1, 1)

poly_data_1 = vtkUnstructuredGrid()
poly_data_1.DeepCopy(poly_data)
poly_data_1.EditableOn()

cell_array = vtkCellArray()
cell_array.ShallowCopy(poly_data_1.GetCells())
cell_array.InsertNextCell(polygon_3)

points_list = vtkPoints()
points_list.ShallowCopy(poly_data_1.GetPoints())
points_list.InsertNextPoint(0, 0, 1)
points_list.InsertNextPoint(1, 0, 1)
points_list.InsertNextPoint(0, 1, 1)

# type_array = vtkUnsignedCharArray()
# type_array.ShallowCopy(poly_data_1.GetCellTypesArray())
type_array: vtkUnsignedCharArray = poly_data_1.GetCellTypesArray()
type_array.InsertNextValue(7)

poly_data_1.InsertNextCell(VTK_POLYHEDRON, polyhedron_list)
print(poly_data_1.GetFaces().GetNumberOfValues())

type_array.SetValue(3, 0)
temp_cell: vtkEmptyCell = poly_data_1.GetCell(3)
print(temp_cell.GetNumberOfPoints())
print(poly_data_1.GetNumberOfCells())

poly_data_writer_1 = vtkXMLUnstructuredGridWriter()
poly_data_writer_1.SetInputData(poly_data_1)
poly_data_writer_1.SetFileName('poly_data_1.vtu')
poly_data_writer_1.Write()
