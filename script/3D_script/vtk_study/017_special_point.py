from vtkmodules.vtkCommonDataModel import vtkVertex, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray, vtkDoubleArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

special_point_grid = vtkUnstructuredGrid()
for each_point_id in range(2):
    temp_point = vtkVertex()
    temp_point.GetPointIds().InsertId(0, each_point_id)
    special_point_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())

special_points_coordinate = vtkPoints()
special_points_coordinate.InsertPoint(0, (1, 0, 9.9))
special_points_coordinate.InsertPoint(1, (1, 0, -9.9))

# id = 0 loading point
# id = 1 fixed point
# id = 2 measured point
point_type = vtkIntArray()
point_type.SetName('point_type')
[point_type.InsertValue(i, 1) for i in range(2)]

# fixed point: velocity
point_velocity = vtkDoubleArray()
point_velocity.SetName('velocity')
point_velocity.SetNumberOfComponents(3)
# [point_velocity.InsertTuple(i, (i, i, i)) for i in range(6)]
point_velocity.InsertTuple(0, (0, 0, -0.0001))
point_velocity.InsertTuple(1, (0, 0, 0.0001))

# loading point: loading force
point_force = vtkDoubleArray()
point_force.SetName('force')
point_force.SetNumberOfComponents(3)
[point_force.InsertTuple(i, (i, i, i)) for i in range(2)]

special_point_grid.SetPoints(special_points_coordinate)
special_point_grid.GetCellData().AddArray(point_type)
special_point_grid.GetCellData().AddArray(point_velocity)
special_point_grid.GetCellData().AddArray(point_force)

point_writer = vtkXMLUnstructuredGridWriter()
point_writer.SetFileName('special_point_1.vtu')
point_writer.SetInputData(special_point_grid)
point_writer.Write()


