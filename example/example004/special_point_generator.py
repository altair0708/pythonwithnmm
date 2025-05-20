from vtkmodules.vtkCommonDataModel import vtkVertex, vtkUnstructuredGrid
import os
from vtkmodules.vtkCommonCore import vtkPoints, vtkIntArray, vtkDoubleArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

output_path = './mesh/'
output_path = os.path.abspath(output_path)
tol = 0.01
start_point = (0, 0, 0)

special_point_grid = vtkUnstructuredGrid()

special_points_coordinate = vtkPoints()

point_type = vtkIntArray()
point_type.SetName('point_type')

fixed_type = vtkIntArray()
fixed_type.SetName('fixed_type')
fixed_type.SetNumberOfComponents(3)

point_group = vtkIntArray()
point_group.SetName('group')

point_velocity = vtkDoubleArray()
point_velocity.SetName('velocity')
point_velocity.SetNumberOfComponents(3)

point_force = vtkDoubleArray()
point_force.SetName('force')
point_force.SetNumberOfComponents(3)

point_displacement = vtkDoubleArray()
point_displacement.SetName('displacement_total')
point_displacement.SetNumberOfComponents(3)

point_displacement_difference = vtkDoubleArray()
point_displacement_difference.SetName('displacement_difference')
point_displacement_difference.SetNumberOfComponents(3)


class SpecialPointGenerator:
    def __init__(self):
        self.__origin = (0, 0, 0)

        self.__x_number = -1
        self.__dx = 0

        self.__y_number = -1
        self.__dy = 0

        self.__z_number = -1
        self.__dz = 0

        self.__point_group_value = -1
        self.__point_type_value = -1
        self.__fixed_type_value = (1, 1, 1)
        self.__point_velocity_value = (0, 0, 0)
        self.__point_force_value = (0, 0, 0)

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, value):
        self.__origin = value

    @property
    def size(self):
        return self.__dx, self.__dy, self.__dz

    @size.setter
    def size(self, value):
        self.__dx, self.__dy, self.__dz = value

    @property
    def number(self):
        return self.__x_number, self.__y_number, self.__z_number

    @number.setter
    def number(self, value):
        self.__x_number, self.__y_number, self.__z_number = value

    @property
    def point_group_value(self):
        return self.__point_group_value

    @point_group_value.setter
    def point_group_value(self, value):
        self.__point_group_value = value

    @property
    def point_type_value(self):
        return self.__point_type_value

    @point_type_value.setter
    def point_type_value(self, value):
        self.__point_type_value = value

    @property
    def fixed_type_value(self):
        return self.__fixed_type_value

    @fixed_type_value.setter
    def fixed_type_value(self, value):
        self.__fixed_type_value = value

    @property
    def point_velocity_value(self):
        return self.__point_velocity_value

    @point_velocity_value.setter
    def point_velocity_value(self, value):
        self.__point_velocity_value = value

    @property
    def point_force_value(self):
        return self.__point_force_value

    @point_force_value.setter
    def point_force_value(self, value):
        self.__point_force_value = value

    def update(self):
        row = self.__x_number
        column = self.__y_number
        vertical = self.__z_number
        point_number = column * row * vertical

        origin = self.__origin

        dx = self.__dx
        dy = self.__dy
        dz = self.__dz

        for each_point_id in range(point_number):
            temp_point = vtkVertex()
            temp_point_id = special_point_grid.GetNumberOfCells()
            temp_point.GetPointIds().InsertId(0, temp_point_id)
            special_point_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())

        for each_row in range(row):
            for each_col in range(column):
                for each_ver in range(vertical):
                    x = origin[0] + (dx / max(row - 1, 1)) * each_row
                    y = origin[1] + (dy / max(column - 1, 1)) * each_col
                    z = origin[2] + (dz / max(vertical - 1, 1)) * each_ver
                    special_points_coordinate.InsertNextPoint((x, y, z))

        # id = 0 loading point
        # id = 1 fixed point
        # id = 2 measured point
        point_group_value = self.__point_group_value
        [point_group.InsertNextValue(point_group_value) for each in range(point_number)]

        point_type_value = self.__point_type_value
        [point_type.InsertNextValue(point_type_value) for each in range(point_number)]

        # fixed direction: (0, 0, 1) mean to fixed z.
        fixed_type_value = self.__fixed_type_value
        [fixed_type.InsertNextTuple(fixed_type_value) for each in range(point_number)]

        # fixed point: velocity
        point_velocity_value = self.__point_velocity_value
        [point_velocity.InsertNextTuple(point_velocity_value) for each in range(point_number)]

        # loading point: loading force
        point_force_value = self.__point_force_value
        [point_force.InsertNextTuple(point_force_value) for each in range(point_number)]

        [point_displacement.InsertNextTuple((0, 0, 0)) for each in range(point_number)]
        [point_displacement_difference.InsertNextTuple((0, 0, 0)) for each in range(point_number)]

generator = SpecialPointGenerator()

generator.origin = (0, 0.01, 0)
generator.size = (4, 0, 8)
generator.number = (31, 1, 31)
generator.point_group_value = 0
generator.point_type_value = 1
generator.point_velocity_value = (0, 0.00001, 0)
generator.update()

generator.origin = (0, 0, 0.01)
generator.size = (4, 20, 0)
generator.number = (31, 31, 1)
generator.point_group_value = 1
generator.point_type_value = 1
generator.point_velocity_value = (0, 0.00001, 0)
generator.update()

generator.origin = (0, 19.99, 0)
generator.size = (4, 0, 8)
generator.number = (31, 1, 31)
generator.point_group_value = 2
generator.point_type_value = 1
generator.point_velocity_value = (0, 0.00001, 0)
generator.update()

generator.origin = (0, 19.99, 12)
generator.size = (4, 0, 8)
generator.number = (31, 1, 31)
generator.point_group_value = 3
generator.point_type_value = 1
generator.point_velocity_value = (0, 0, 0)
generator.update()

generator.origin = (0, 0.01, 12)
generator.size = (4, 0, 8)
generator.number = (31, 1, 31)
generator.point_group_value = 4
generator.point_type_value = 1
generator.point_velocity_value = (0, 0, 0)
generator.update()

generator.origin = (0, 0, 19.99)
generator.size = (4, 20, 0)
generator.number = (31, 31, 1)
generator.point_group_value = 5
generator.point_type_value = 1
generator.point_velocity_value = (0, 0, 0)
generator.update()

special_point_grid.SetPoints(special_points_coordinate)
special_point_grid.GetCellData().AddArray(point_type)
special_point_grid.GetCellData().AddArray(fixed_type)
special_point_grid.GetCellData().AddArray(point_velocity)
special_point_grid.GetCellData().AddArray(point_force)
special_point_grid.GetCellData().AddArray(point_displacement)

special_point_grid.GetCellData().AddArray(point_group)
special_point_grid.GetCellData().AddArray(point_displacement_difference)

point_writer = vtkXMLUnstructuredGridWriter()
point_writer.SetFileName(output_path + '/special_point.vtu')
point_writer.SetInputData(special_point_grid)
point_writer.Write()


