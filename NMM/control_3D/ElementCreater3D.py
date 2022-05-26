import numpy as np
import json
import sqlite3
from typing import List
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkCellData
from vtkmodules.vtkCommonCore import vtkDataArray, vtkPoints, vtkIdList
from NMM.fem_3D.ElementBase_3D import Element3D
from NMM.fem_3D.PointBase_3D import EPoint3D, PointType


def create_an_element(id_value: int,
                      cursor: sqlite3.Cursor,
                      element_grid: vtkUnstructuredGrid,
                      mathcover_grid: vtkUnstructuredGrid,
                      special_point_grid: vtkUnstructuredGrid,
                      material_coefficient: str) -> Element3D:
    element = Element3D(id_value)

    # get joint point info
    temp_cell: vtkTetra = element_grid.GetCell(id_value)
    temp_cell_data_list: vtkCellData = element_grid.GetCellData()
    material_id_list: vtkDataArray = temp_cell_data_list.GetArray(1)
    if material_id_list.GetName() != 'material_id':
        raise Exception('DataArray Index Error!')
    element.material_id = material_id_list.GetTuple(id_value)

    joint_list: vtkPoints = temp_cell.GetPoints()
    joint_id_list = vtkIdList()
    element_grid.GetCellPoints(id_value, joint_id_list)
    # print('element vertex coordinate:')
    for each_joint in range(joint_id_list.GetNumberOfIds()):
        joint_id = joint_id_list.GetId(each_joint)
        element.joint_id[each_joint] = joint_id
        element.joint_list[each_joint] = joint_list.GetPoint(each_joint)
        # print(joint_list.GetPoint(each_joint))

    # get patch info
    temp_math_data_list: vtkCellData = mathcover_grid.GetCellData()
    math_id: vtkDataArray = temp_math_data_list.GetArray(0)
    math_coordinate: vtkDataArray = temp_math_data_list.GetArray(1)
    math_displacement: vtkDataArray = temp_math_data_list.GetArray(2)
    if math_id.GetName() != 'math_cover_id':
        raise Exception('math_cover_id dataArray Index Error!')
    if math_coordinate.GetName() != 'math_cover_coordinate':
        raise Exception('math_cover_coordinate dataArray Index Error!')
    if math_displacement.GetName() != 'math_cover_displacement':
        raise Exception('math_cover_displacement dataArray Index Error!')

    database_statement = 'SELECT MathCoverId FROM ElementMathcover WHERE ElementId={elementId}'.format(elementId=id_value)
    patch_id_list = cursor.execute(database_statement)
    patch_id_list = patch_id_list.fetchall()
    # print('math cover coordinate:')
    for each_patch_id in range(4):
        temp_math_id = patch_id_list[each_patch_id][0]
        element.patch_id[each_patch_id] = temp_math_id
        temp_coordinate = math_coordinate.GetTuple(temp_math_id)
        element.patch_list[each_patch_id] = temp_coordinate
        temp_displacement = math_displacement.GetTuple(temp_math_id)
        element.patch_displacement[each_patch_id] = temp_displacement
        # print('coordinate:{}'.format(temp_coordinate))
        # print('displacement:{}'.format(temp_displacement))

    # get material info
    with open(material_coefficient) as material_coefficient:
        element.material_dict = json.load(material_coefficient)

    # get special point info
    special_point_data: vtkCellData = special_point_grid.GetCellData()
    point_type_list: vtkDataArray = special_point_data.GetArray(0)
    if point_type_list.GetName() != 'point_type':
        raise Exception('special_point_type dataArray Index error!')
    velocity_list: vtkDataArray = special_point_data.GetArray(1)
    if velocity_list.GetName() != 'velocity':
        raise Exception('special_point_velocity dataArray Index error!')
    force_list: vtkDataArray = special_point_data.GetArray(2)
    if force_list.GetName() != 'force':
        raise Exception('special_point_force dataArray Index error!')
    database_statement = 'SELECT SpecialPointId FROM ElementSpecialPoint WHERE ElementId={elementId}'.format(elementId=id_value)
    special_point_list = cursor.execute(database_statement)
    special_point_list = special_point_list.fetchall()
    if len(special_point_list) != 0:
        # print('element id: {}, special point id: {}'.format(id_value, special_point_list))
        for each_id in special_point_list:
            each_id = each_id[0]
            temp_type = point_type_list.GetTuple(each_id)
            temp_type = temp_type[0]
            if temp_type == 0:
                temp_special_point = EPoint3D(PointType.loading_point)
                element.loading_point_list.append(temp_special_point)
            elif temp_type == 1:
                temp_special_point = EPoint3D(PointType.fixed_point)
                element.fixed_point_list.append(temp_special_point)
            elif temp_type == 2:
                temp_special_point = EPoint3D(PointType.measured_point)
                element.measured_point_list.append(temp_special_point)
            else:
                raise Exception('special_point type error! type value is {}'.format(temp_type))
            # temp_special_point.coord = np.array([[1, 2, 3]], dtype=np.float64)
            # temp_special_point.velocity = np.array([[1, 2, 3]], dtype=np.float64)
            # temp_special_point.force = np.array([[1, 2, 3]], dtype=np.float64)
            temp_points: vtkPoints = special_point_grid.GetPoints()
            temp_special_point.coord = np.array(temp_points.GetPoint(each_id), dtype=np.float64).reshape(1, 3)
            temp_special_point.velocity = np.array(velocity_list.GetTuple(each_id), dtype=np.float64).reshape(1, 3)
            temp_special_point.force = np.array(force_list.GetTuple(each_id), dtype=np.float64).reshape(1, 3)
            # print(temp_points.GetPoint(each_id))
            # print(velocity_list.GetTuple(each_id))
            # print(force_list.GetTuple(each_id))
        # print(element.fixed_point_list[0].coord)

    return element


class ElementCreator3D:

    @staticmethod
    def create_all_element(database_name: str,
                           element_file_name: str,
                           mathcover_file_name: str,
                           special_point_file_name: str,
                           material_coefficient_file_name: str) -> List[Element3D]:
        with sqlite3.connect(database_name) as connection:
            database_cursor = connection.cursor()

        math_reader = vtkXMLUnstructuredGridReader()
        math_reader.SetFileName(mathcover_file_name)
        math_reader.Update()
        mathGrid: vtkUnstructuredGrid = math_reader.GetOutput()
        math_number = mathGrid.GetNumberOfCells()
        print('math_cover_number:{}'.format(math_number))

        element_reader = vtkXMLUnstructuredGridReader()
        element_reader.SetFileName(element_file_name)
        element_reader.Update()
        elementGrid: vtkUnstructuredGrid = element_reader.GetOutput()
        element_number = elementGrid.GetNumberOfCells()
        print('element_number:{}'.format(element_number))

        special_point_reader = vtkXMLUnstructuredGridReader()
        special_point_reader.SetFileName(special_point_file_name)
        special_point_reader.Update()
        specialPointGrid: vtkUnstructuredGrid = special_point_reader.GetOutput()
        special_point_number = specialPointGrid.GetNumberOfCells()
        print('special_point_number:{}'.format(special_point_number))

        element_list = []
        for each_element_id in range(element_number):
            temp = create_an_element(each_element_id, database_cursor, elementGrid, mathGrid, specialPointGrid, material_coefficient_file_name)
            element_list.append(temp)
        return element_list


'''
class ElementCreator(object):
    def __init__(self, cursor: sqlite3.Cursor):
        self.__database_cursor = cursor
        self.__element_number = get_element_number(self.__database_cursor)
        self.__element_list = []

    def create_an_element(self, id_value: int) -> Element:
        element = Element(id_value)
        element.material_id = get_one_element_material(id_value=id_value, cursor=self.__database_cursor)
        with open('../data/material_coefficient.json') as material_coefficient:
            element.material_dict = json.load(material_coefficient)
        return element

    def assembly_joint_point(self, element):
        joint_list = get_one_element_joint(id_value=element.id, cursor=self.__database_cursor)
        for each_joint in joint_list:
            element.joint_id.append(each_joint[0])
            element.joint_list.append(each_joint[1:3])

    def assembly_patch(self, element):
        patch_list = get_one_element_patch(id_value=element.id, cursor=self.__database_cursor)
        for each_patch in patch_list:
            element.patch_id.append(each_patch[0])
            element.patch_list.append(each_patch[1:3])

    def assembly_special_point(self, element):
        special_point_list = get_one_special_point(id_value=element.id, cursor=self.__database_cursor)
        if len(special_point_list) != 0:
            for each_point in special_point_list:
                temp_point = EPoint(PointType(each_point[4]))
                temp_point.element_id = element.id
                temp_point.id = int(each_point[0])
                temp_point.coord = np.array([each_point[1:3]])
                temp_point.velocity = np.array([each_point[7:9]])
                if temp_point.point_type == PointType.fixed_point:
                    element.fixed_point_list.append(temp_point)
                elif temp_point.point_type == PointType.loading_point:
                    element.loading_point_list.append(temp_point)
                elif temp_point.point_type == PointType.measured_point:
                    element.measured_point_list.append(temp_point)
                else:
                    raise Exception('point type error:{point_type}'.format(point_type=temp_point.point_type))

    def assembly_patch_displacement(self, element: Element):
        for each_id in element.patch_id:
            id_value, x, y, u, v = get_one_patch(each_id, self.__database_cursor)
            element.patch_displacement.append([u, v])

    def assembly_joint_displacement(self, element: Element):
        for each_id in element.joint_id:
            id_value, x, y, u, v = get_one_joint(each_id, self.__database_cursor)
            element.joint_displacement_increment.append([u, v])

    def start(self):
        print('element number is {}'.format(self.__element_number))
        for each_id in range(1, self.__element_number + 1):
            temp_element = self.create_an_element(each_id)
            self.assembly_patch(temp_element)
            self.assembly_special_point(temp_element)
            self.assembly_joint_point(temp_element)
            self.assembly_patch_displacement(temp_element)
            self.__element_list.append(temp_element)
        return self.__element_list

    def run(self):
        for each_element in self.__element_list:
            each_element.clean_all()
            self.assembly_patch_displacement(each_element)
        return self.__element_list

    @staticmethod
    def clean(element_list: List[Element]):
        for each_element in element_list:
            each_element.clean_all()
'''
if __name__ == '__main__':
    element_id = 737
    element_file = '../../data_3D/manifold_element.vtu'
    mathcover_file = '../../data_3D/math_cover.vtu'
    special_point_file = '../../data_3D/special_point.vtu'
    database_name = '../../data_3D/manifold_mathcover.db'
    material_coefficient_file = '../../data_3D/material_coefficient.json'

    temp_element_list = ElementCreator3D.create_all_element(database_name, element_file, mathcover_file, special_point_file, material_coefficient_file)

