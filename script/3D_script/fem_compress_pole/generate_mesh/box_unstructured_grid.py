from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkVertex,
                                           vtkBox,
                                           vtkPlane,
                                           vtkTetra,
                                           vtkCell, vtkPolyData, vtkPolygon,
                                           VTK_POLYHEDRON,
                                           vtkHexahedron)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIntArray
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from itertools import combinations

# number of skeleton point
row_point_number = 11
column_point_number = 11
layer_point_number = 11
# start point
start_point = (0.001, 0.001, 0.001)
# start_point = (0, 0, 0)

'''
Generate point file
'''
# distance of two adjacent point
point_distance = 1

# generate point file
point_coord_list = vtkPoints()
point_grid = vtkUnstructuredGrid()
for z in range(layer_point_number):
    for y in range(column_point_number):
        for x in range(row_point_number):
            point_id = x + y * row_point_number + z * row_point_number * column_point_number
            point_coord_list.InsertPoint(point_id, (x * point_distance + start_point[0],
                                                    y * point_distance + start_point[1],
                                                    z * point_distance + start_point[2]))
            temp_point = vtkVertex()
            temp_point.GetPointIds().SetId(0, point_id)
            point_grid.InsertNextCell(temp_point.GetCellType(), temp_point.GetPointIds())

point_grid.SetPoints(point_coord_list)

# point_writer = vtkXMLUnstructuredGridWriter()
# point_writer.SetFileName('box_1.vtu')
# point_writer.SetInputData(point_grid)
# point_writer.Write()

'''
Generate cube element file and tetrahedron element file
'''
# number of element
row_element_number = row_point_number - 1
column_element_number = column_point_number - 1
layer_element_number = layer_point_number - 1
element_grid = vtkUnstructuredGrid()
tetra_grid = vtkUnstructuredGrid()

element_type_id = vtkIntArray()
element_type_id.SetName('element_type')
element_type_id.SetNumberOfComponents(1)

for z in range(layer_element_number):
    for y in range(column_element_number):
        for x in range(row_element_number):

            element_id = x + y * row_element_number + z * row_element_number * column_element_number
            element_type = (x + y + z) % 2
            element_type_id.InsertValue(element_id, element_type)

            point_id_0 = x + y * row_point_number + z * row_point_number * column_point_number
            point_id_1 = (x + 1) + y * row_point_number + z * row_point_number * column_point_number
            point_id_2 = (x + 1) + (y + 1) * row_point_number + z * row_point_number * column_point_number
            point_id_3 = x + (y + 1) * row_point_number + z * row_point_number * column_point_number
            point_id_4 = x + y * row_point_number + (z + 1) * row_point_number * column_point_number
            point_id_5 = (x + 1) + y * row_point_number + (z + 1) * row_point_number * column_point_number
            point_id_6 = (x + 1) + (y + 1) * row_point_number + (z + 1) * row_point_number * column_point_number
            point_id_7 = x + (y + 1) * row_point_number + (z + 1) * row_point_number * column_point_number

            temp_element = vtkHexahedron()
            temp_element.GetPointIds().SetId(0, point_id_0)
            temp_element.GetPointIds().SetId(1, point_id_1)
            temp_element.GetPointIds().SetId(2, point_id_2)
            temp_element.GetPointIds().SetId(3, point_id_3)
            temp_element.GetPointIds().SetId(4, point_id_4)
            temp_element.GetPointIds().SetId(5, point_id_5)
            temp_element.GetPointIds().SetId(6, point_id_6)
            temp_element.GetPointIds().SetId(7, point_id_7)

            element_grid.InsertNextCell(temp_element.GetCellType(), temp_element.GetPointIds())

            temp_tetra_0 = vtkTetra()
            temp_tetra_1 = vtkTetra()
            temp_tetra_2 = vtkTetra()
            temp_tetra_3 = vtkTetra()
            temp_tetra_4 = vtkTetra()
            if element_type:
                temp_tetra_0.GetPointIds().SetId(0, point_id_0)
                temp_tetra_0.GetPointIds().SetId(1, point_id_1)
                temp_tetra_0.GetPointIds().SetId(2, point_id_3)
                temp_tetra_0.GetPointIds().SetId(3, point_id_4)

                temp_tetra_1.GetPointIds().SetId(0, point_id_2)
                temp_tetra_1.GetPointIds().SetId(1, point_id_1)
                temp_tetra_1.GetPointIds().SetId(2, point_id_3)
                temp_tetra_1.GetPointIds().SetId(3, point_id_6)

                temp_tetra_2.GetPointIds().SetId(0, point_id_5)
                temp_tetra_2.GetPointIds().SetId(1, point_id_1)
                temp_tetra_2.GetPointIds().SetId(2, point_id_4)
                temp_tetra_2.GetPointIds().SetId(3, point_id_6)

                temp_tetra_3.GetPointIds().SetId(0, point_id_7)
                temp_tetra_3.GetPointIds().SetId(1, point_id_4)
                temp_tetra_3.GetPointIds().SetId(2, point_id_6)
                temp_tetra_3.GetPointIds().SetId(3, point_id_3)

                temp_tetra_4.GetPointIds().SetId(0, point_id_1)
                temp_tetra_4.GetPointIds().SetId(1, point_id_3)
                temp_tetra_4.GetPointIds().SetId(2, point_id_4)
                temp_tetra_4.GetPointIds().SetId(3, point_id_6)
            else:
                temp_tetra_0.GetPointIds().SetId(0, point_id_1)
                temp_tetra_0.GetPointIds().SetId(1, point_id_0)
                temp_tetra_0.GetPointIds().SetId(2, point_id_2)
                temp_tetra_0.GetPointIds().SetId(3, point_id_5)

                temp_tetra_1.GetPointIds().SetId(0, point_id_3)
                temp_tetra_1.GetPointIds().SetId(1, point_id_2)
                temp_tetra_1.GetPointIds().SetId(2, point_id_0)
                temp_tetra_1.GetPointIds().SetId(3, point_id_7)

                temp_tetra_2.GetPointIds().SetId(0, point_id_4)
                temp_tetra_2.GetPointIds().SetId(1, point_id_5)
                temp_tetra_2.GetPointIds().SetId(2, point_id_7)
                temp_tetra_2.GetPointIds().SetId(3, point_id_0)

                temp_tetra_3.GetPointIds().SetId(0, point_id_6)
                temp_tetra_3.GetPointIds().SetId(1, point_id_7)
                temp_tetra_3.GetPointIds().SetId(2, point_id_5)
                temp_tetra_3.GetPointIds().SetId(3, point_id_2)

                temp_tetra_4.GetPointIds().SetId(0, point_id_0)
                temp_tetra_4.GetPointIds().SetId(1, point_id_2)
                temp_tetra_4.GetPointIds().SetId(2, point_id_5)
                temp_tetra_4.GetPointIds().SetId(3, point_id_7)
            tetra_grid.InsertNextCell(temp_tetra_0.GetCellType(), temp_tetra_0.GetPointIds())
            tetra_grid.InsertNextCell(temp_tetra_1.GetCellType(), temp_tetra_1.GetPointIds())
            tetra_grid.InsertNextCell(temp_tetra_2.GetCellType(), temp_tetra_2.GetPointIds())
            tetra_grid.InsertNextCell(temp_tetra_3.GetCellType(), temp_tetra_3.GetPointIds())
            tetra_grid.InsertNextCell(temp_tetra_4.GetCellType(), temp_tetra_4.GetPointIds())

element_grid.SetPoints(point_coord_list)
element_grid.GetCellData().AddArray(element_type_id)

# element_writer = vtkXMLUnstructuredGridWriter()
# element_writer.SetFileName('box_2.vtu')
# element_writer.SetInputData(element_grid)
# element_writer.Write()

tetra_grid.SetPoints(point_coord_list)
tetra_writer = vtkXMLUnstructuredGridWriter()
tetra_writer.SetFileName('../mesh/gmsh_file.vtu')
tetra_writer.SetInputData(tetra_grid)
tetra_writer.Write()

# turn tetra to polyhedron
tetra_polyhedron_grid = vtkUnstructuredGrid()
element_number = tetra_grid.GetNumberOfCells()
temp_tetra: vtkTetra = tetra_grid.GetCell(0)

for element_id in range(element_number):
    temp_tetra: vtkTetra = tetra_grid.GetCell(element_id)
    temp_vtk_list: vtkIdList = temp_tetra.GetPointIds()
    temp_list = []
    if temp_tetra.GetNumberOfPoints() != 4:
        raise Exception('Element point number error!')
    for i in range(temp_tetra.GetNumberOfPoints()):
        temp_list.append(temp_vtk_list.GetId(i))
    temp_face_list = combinations(temp_list, 3)
    temp_vtk_list = vtkIdList()
    temp_vtk_list.InsertNextId(4)
    for each_face in temp_face_list:
        temp_vtk_list.InsertNextId(3)
        for each_point in each_face:
            temp_vtk_list.InsertNextId(each_point)
    if temp_vtk_list.GetNumberOfIds() != 17:
        raise Exception('ID list number error!')
    tetra_polyhedron_grid.InsertNextCell(VTK_POLYHEDRON, temp_vtk_list)
tetra_polyhedron_grid.SetPoints(point_coord_list)
# tetra_polyhedron_writer = vtkXMLUnstructuredGridWriter()
# tetra_polyhedron_writer.SetFileName('box_5.vtu')
# tetra_polyhedron_writer.SetInputData(tetra_polyhedron_grid)
# tetra_polyhedron_writer.Write()

# # clip the unstructured grid by planes
# clipPlane1 = vtkPlane()
# clipPlane1.SetOrigin(4.5, 0, 0)
# clipPlane1.SetNormal(1, 0, 0)
#
# clipPlane2 = vtkPlane()
# clipPlane2.SetOrigin(5.5, 0, 0)
# clipPlane2.SetNormal(-1, 0.5, 0.5)
#
# clipper1 = vtkClipDataSet()
# clipper1.SetClipFunction(clipPlane1)
# clipper1.SetInputData(tetra_polyhedron_grid)
# clipper1.SetValue(0.0)
# clipper1.GenerateClippedOutputOn()
#
# clipper2 = vtkClipDataSet()
# clipper2.SetClipFunction(clipPlane2)
# clipper2.SetInputConnection(clipper1.GetOutputPort())
# clipper2.SetValue(0.0)
# clipper2.GenerateClippedOutputOn()
# clipper2.Update()
# result: vtkUnstructuredGrid = clipper2.GetOutput()
#
# clipper_writer = vtkXMLUnstructuredGridWriter()
# clipper_writer.SetFileName('box_6.vtu')
# clipper_writer.SetInputData(result)
# clipper_writer.Write()

'''
Generate math cover file
'''
print('original mesh info:')
print('number of points: {}'.format(tetra_grid.GetNumberOfPoints()))
print('number of cells: {}'.format(tetra_grid.GetNumberOfCells()))
# print('number of clipped points: {}'.format(result.GetNumberOfPoints()))
math_cover_grid = vtkUnstructuredGrid()
for each_id in range(tetra_grid.GetNumberOfPoints()):
    cellIdList = vtkIdList()
    pointId = each_id
    tetra_grid.GetPointCells(pointId, cellIdList)

    # Generate new grid of selected cell
    mathGrid = vtkUnstructuredGrid()
    idNumber = cellIdList.GetNumberOfIds()
    for eachId in range(idNumber):
        cellId = cellIdList.GetId(eachId)
        tempCell: vtkCell =tetra_grid.GetCell(cellId)
        mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
    mathGrid.SetPoints(tetra_grid.GetPoints())

    surface = vtkGeometryFilter()
    surface.PassThroughPointIdsOn()
    surface.SetInputData(mathGrid)
    surface.MergingOff()
    surface.Update()
    result: vtkPolyData = surface.GetOutput()

    faceIdList = vtkIdList()
    faceIdList.InsertNextId(result.GetNumberOfCells())
    for face_id in range(result.GetNumberOfCells()):
        temp_face: vtkPolygon = result.GetCell(face_id)
        faceIdList.InsertNextId(temp_face.GetNumberOfPoints())
        for i in range(temp_face.GetNumberOfPoints()):
            faceIdList.InsertNextId(temp_face.GetPointId(i))

    math_cover_grid.InsertNextCell(VTK_POLYHEDRON, faceIdList)
print('number of math covers: {}'.format(math_cover_grid.GetNumberOfCells()))

# math_cover_grid.SetPoints(point_coord_list)
# math_cover_writer = vtkXMLUnstructuredGridWriter()
# math_cover_writer.SetFileName('box_4.vtu')
# math_cover_writer.SetInputData(math_cover_grid)
# math_cover_writer.Write()

