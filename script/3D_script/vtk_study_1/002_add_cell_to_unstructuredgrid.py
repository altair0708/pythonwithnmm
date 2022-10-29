from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.CopyFunction import copy_polyhedron
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell
from vtkmodules.vtkCommonCore import vtkPoints

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName('manifold_element.vtu')
reader.Update()
origin_data: vtkUnstructuredGrid = reader.GetOutput()
cell_number = origin_data.GetNumberOfCells()

origin_points_list = vtkPoints()
origin_points_list.DeepCopy(origin_data.GetPoints())

modify_data = vtkUnstructuredGrid()
for each_cell in range(cell_number):
    temp_cell: vtkCell = origin_data.GetCell(each_cell)
    # temp_cell: vtkCell = copy_polyhedron(temp_cell, origin_points_list)
    insert_a_cell(modify_data, temp_cell)

cell_0: vtkCell = origin_data.GetCell(0)
points_0 = cell_0.GetPoints()
cell_1: vtkCell = modify_data.GetCell(0)
points_1 = cell_1.GetPoints()
for i in range(4):
    print('__________out___________')
    print(points_0.GetPoint(i))
    print(points_1.GetPoint(i))

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(modify_data)
writer.SetFileName('manifold_element_1.vtu')
writer.Write()

