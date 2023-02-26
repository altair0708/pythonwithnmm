from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader, vtkXMLPolyDataWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPlane, vtkCell, vtkPolyData, vtkPolygon, vtkGenericCell
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkMath
from vtkmodules.vtkFiltersCore import vtkCutter

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(3)
# polygon_0.GetPointIds().SetId(0, 0)
polygon_0.GetPointIds().SetId(0, 1)
polygon_0.GetPointIds().SetId(1, 2)
polygon_0.GetPointIds().SetId(2, 3)

polygon_1 = vtkPolygon()
polygon_1.GetPointIds().SetNumberOfIds(3)
polygon_1.GetPointIds().SetId(0, 2)
polygon_1.GetPointIds().SetId(1, 3)
polygon_1.GetPointIds().SetId(2, 4)

test_points = vtkPoints()
test_points.InsertNextPoint(-1, 1, 0)
test_points.InsertNextPoint(-1, 0, 0)
test_points.InsertNextPoint(0, 0, 0)
test_points.InsertNextPoint(0, 1, 0)
test_points.InsertNextPoint(1, 0, 1)

test_grid = vtkUnstructuredGrid()
test_grid.SetPoints(test_points)
test_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())
test_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('re015_1.vtu')
writer.SetInputData(test_grid)
writer.Write()

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName('re015_1.vtu')
reader.Update()
u_grid: vtkUnstructuredGrid = reader.GetOutput()

assert u_grid.GetNumberOfCells() == 2
new_grid = vtkUnstructuredGrid()
new_grid.DeepCopy(u_grid)

cell_0 = vtkGenericCell()
cell_0.DeepCopy(u_grid.GetCell(0))
cell_1 = vtkGenericCell()
cell_1.DeepCopy(u_grid.GetCell(1))

id_list_0 = vtkIdList()
id_list_0.DeepCopy(cell_0.GetPointIds())
id_list_1 = vtkIdList()
id_list_1.DeepCopy(cell_1.GetPointIds())

id_list_0.IntersectWith(id_list_1)
assert id_list_0.GetNumberOfIds() == 2

point_0 = u_grid.GetPoints().GetPoint(id_list_0.GetId(0))
point_1 = u_grid.GetPoints().GetPoint(id_list_0.GetId(1))

point_2 = ((point_0[0] + point_1[0]) / 2, (point_0[1] + point_1[1]) / 2, (point_0[2] + point_1[2]) / 2)
vector_0 = (point_0[0] - point_1[0], point_0[1] - point_1[1], point_0[2] - point_1[2])

# print(point_2)
# print(vector_0)

plane = vtkPlane()
plane.SetNormal(vector_0)
plane.SetOrigin(point_2)

cutter = vtkCutter()
cutter.SetInputData(new_grid)
cutter.SetCutFunction(plane)
cutter.Update()
angle: vtkPolyData = cutter.GetOutput()
assert angle.GetNumberOfPoints() == 3

edge_0_point_0 = angle.GetCell(0).GetPointIds().GetId(0)
edge_0_point_1 = angle.GetCell(0).GetPointIds().GetId(1)
edge_1_point_0 = angle.GetCell(1).GetPointIds().GetId(0)
edge_1_point_1 = angle.GetCell(1).GetPointIds().GetId(1)
print(angle.GetPoint(0))
print(angle.GetPoint(1))
print(angle.GetPoint(2))


def generate_vector(vtk_grid, id_0, id_1):
    result = (vtk_grid.GetPoint(id_0)[0] - vtk_grid.GetPoint(id_1)[0],
              vtk_grid.GetPoint(id_0)[1] - vtk_grid.GetPoint(id_1)[1],
              vtk_grid.GetPoint(id_0)[2] - vtk_grid.GetPoint(id_1)[2])
    return result


if edge_0_point_0 == edge_1_point_0:
    ray_0 = generate_vector(angle, edge_0_point_1, edge_0_point_0)
    ray_1 = generate_vector(angle, edge_1_point_1, edge_1_point_0)
elif edge_0_point_0 == edge_1_point_1:
    ray_0 = generate_vector(angle, edge_0_point_1, edge_0_point_0)
    ray_1 = generate_vector(angle, edge_1_point_0, edge_1_point_1)
elif edge_0_point_1 == edge_1_point_0:
    ray_0 = generate_vector(angle, edge_0_point_0, edge_0_point_1)
    ray_1 = generate_vector(angle, edge_1_point_1, edge_1_point_0)
elif edge_0_point_1 == edge_1_point_1:
    ray_0 = generate_vector(angle, edge_0_point_0, edge_0_point_1)
    ray_1 = generate_vector(angle, edge_1_point_0, edge_1_point_1)
else:
    raise Exception('Angle do not have vertex!')
print(ray_0)
print(ray_1)
print(vtkMath.Dot(ray_0, ray_1))

writer = vtkXMLPolyDataWriter()
writer.SetInputData(angle)
writer.SetFileName('re015_2.vtp')
writer.Write()


