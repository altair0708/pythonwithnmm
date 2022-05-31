import numpy as np
from typing import List
from NMM.fem_3D.ElementBase_3D import Element3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData
from vtkmodules.vtkCommonCore import vtkDataArray


class ElementRefresher3D:

    # refresh the math cover file math_cover.vtu
    @staticmethod
    def refresh_math_cover_file_displacement(patch_displacement: np.ndarray, math_cover_file: str):
        temp_math_displacement = patch_displacement.reshape((-1, 3))
        math_grid_reader = vtkXMLUnstructuredGridReader()
        math_grid_reader.SetFileName(math_cover_file)
        math_grid_reader.Update()
        math_grid: vtkUnstructuredGrid = math_grid_reader.GetOutput()
        math_grid_data: vtkCellData = math_grid.GetCellData()
        math_grid_displacement: vtkDataArray = math_grid_data.GetArray(2)
        if math_grid_displacement.GetName() != 'math_cover_displacement':
            raise Exception('math cover displacement index error!')
        for each_math_cover in range(len(temp_math_displacement)):
            math_grid_displacement.SetTuple(each_math_cover, temp_math_displacement[each_math_cover])
            # math_grid_displacement.SetTuple(each_math_cover, (each_math_cover * 1000, each_math_cover * 1000, each_math_cover * 1000))
        math_grid_writer = vtkXMLUnstructuredGridWriter()
        math_grid_writer.SetFileName(math_cover_file)
        math_grid_writer.SetInputData(math_grid)
        math_grid_writer.Write()

    # refresh the manifold elements list
    @staticmethod
    def refresh_element_list_displacement(element_list: List[Element3D], math_cover_file: str):
        math_grid_reader = vtkXMLUnstructuredGridReader()
        math_grid_reader.SetFileName(math_cover_file)
        math_grid_reader.Update()
        math_grid: vtkUnstructuredGrid = math_grid_reader.GetOutput()
        math_cell_data: vtkCellData = math_grid.GetCellData()
        math_displacement_list: vtkDataArray = math_cell_data.GetArray(2)
        if math_displacement_list.GetName() != 'math_cover_displacement':
            raise Exception('math_cover_displacement dataArray Index Error!')
        for element in element_list:
            temp_element_math_cover_id = element.patch_id
            if len(element.patch_displacement) != 4:
                raise Exception('math_displacement size error, length: {}'.format(len(element.patch_displacement)))
            for math_id in range(len(temp_element_math_cover_id)):
                temp_math_displacement = math_displacement_list.GetTuple(temp_element_math_cover_id[math_id])
                element.patch_displacement[math_id] = temp_math_displacement

    @staticmethod
    def refresh_manifold_element_file_displacement(element_list: List[Element3D], manifold_element_file: str):
        manifold_element_reader = vtkXMLUnstructuredGridReader()
        manifold_element_reader.SetFileName(manifold_element_file)
        manifold_element_reader.Update()
        manifold_element_grid: vtkUnstructuredGrid = manifold_element_reader.GetOutput()
        manifold_element_cell_data: vtkCellData = manifold_element_grid.GetPointData()
        manifold_element_displacement_increment_list: vtkDataArray = manifold_element_cell_data.GetArray(1)
        if manifold_element_displacement_increment_list.GetName() != 'point_displacement_increment':
            raise Exception('point_displacement_increment dataArray Index Error!')
        manifold_element_number = manifold_element_grid.GetNumberOfCells()
        for element_id in range(manifold_element_number):
            temp_displacement_list = element_list[element_id].joint_displacement_increment
            point_number = len(element_list[0].joint_list)
            for point_id in range(point_number):
                temp_point_id = element_list[element_id].joint_id[point_id]
                manifold_element_displacement_increment_list.InsertTuple(temp_point_id, temp_displacement_list[point_id])

        manifold_element_displacement_total_list: vtkDataArray = manifold_element_cell_data.GetArray(2)
        if manifold_element_displacement_total_list.GetName() != 'point_displacement_total':
            raise Exception('point_displacement_total dataArray Index Error!')
        for each_point_id in range(manifold_element_grid.GetNumberOfPoints()):
            temp_increment = manifold_element_displacement_increment_list.GetTuple(each_point_id)
            temp_total = manifold_element_displacement_total_list.GetTuple(each_point_id)
            temp_total = np.array(temp_increment, dtype=np.float64) + np.array(temp_total, dtype=np.float64)
            manifold_element_displacement_total_list.InsertTuple(each_point_id, temp_total)

        manifold_element_grid_writer = vtkXMLUnstructuredGridWriter()
        manifold_element_grid_writer.SetFileName(manifold_element_file)
        manifold_element_grid_writer.SetInputData(manifold_element_grid)
        manifold_element_grid_writer.Write()

    @staticmethod
    def clean_all(element_list: List[Element3D]):
        for each_element in element_list:
            each_element.clean_all()


    # @staticmethod
    # def assembly_patch_displacement(element: Element, database_cursor: sqlite3.Cursor):
    #     pass
    #
    # @staticmethod
    # def refresh_joint_displacement(element_list: List[Element], cursor: sqlite3.Cursor):
    #     pass
    #
    # @staticmethod
    # def refresh_special_point_displacement(element_list: List[Element], cursor: sqlite3.Cursor):
    #     pass
