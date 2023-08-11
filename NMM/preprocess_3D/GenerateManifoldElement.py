import sqlite3
from NMM.control_3D.ElementIO3D import ElementIOer3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkGenericCell
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, reference, vtkDoubleArray, vtkIntArray


def generate_manifold_element(mesh_path: str, geometry_path: str, special_point=None):
    elementGrid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(geometry_path + 'geometry_tetrahedron.vtu')
    elementNumber = elementGrid.GetNumberOfCells()
    print('element_number:{}'.format(elementNumber))

    # crack_element_grid: vtkUnstructuredGrid = vtkUnstructuredGrid()
    # crack_element_grid.DeepCopy(elementGrid)
    # crack_element_number = crack_element_grid.GetNumberOfCells()
    # print('crack_element_number:{}'.format(crack_element_number))

    # connect to database
    with sqlite3.connect(geometry_path + 'manifold_mathcover.db') as connection:
        database_cursor = connection.cursor()
        database_statement = 'CREATE TABLE ElementMathcover(' \
                             'ID          INTEGER PRIMARY KEY AUTOINCREMENT ,' \
                             'ElementId   INT                 NOT NULL,' \
                             'MathcoverId INT                 NOT NULL);'
        database_statement_1 = 'CREATE TABLE ElementSpecialPoint(' \
                               'ID             INTEGER PRIMARY KEY AUTOINCREMENT ,' \
                               'ElementId      INT                 NOT NULL,' \
                               'SpecialPointId INT                 NOT NULL);'
        # create table
        try:
            database_cursor.execute(database_statement)
            database_cursor.execute(database_statement_1)
        except sqlite3.OperationalError:
            database_statement = 'DROP TABLE ElementMathcover;'
            database_statement_1 = 'DROP TABLE ElementSpecialPoint;'
            database_cursor.execute(database_statement)
            database_cursor.execute(database_statement_1)
            database_statement = 'CREATE TABLE ElementMathcover(' \
                                 'ID          INTEGER PRIMARY KEY AUTOINCREMENT ,' \
                                 'ElementId   INT                 NOT NULL,' \
                                 'MathcoverId INT                 NOT NULL);'
            database_statement_1 = 'CREATE TABLE ElementSpecialPoint(' \
                                   'ID             INTEGER PRIMARY KEY AUTOINCREMENT ,' \
                                   'ElementId      INT                 NOT NULL,' \
                                   'SpecialPointId INT                 NOT NULL);'
            database_cursor.execute(database_statement)
            database_cursor.execute(database_statement_1)

        # input element math cover relationship
        for each_id in range(elementNumber):
            temp_id_list = vtkIdList()
            elementGrid.GetCellPoints(each_id, temp_id_list)
            for each_point_id in range(temp_id_list.GetNumberOfIds()):
                temp_point_id = temp_id_list.GetId(each_point_id)
                database_statement = 'INSERT INTO ElementMathcover (ElementId, MathcoverId)' \
                                     'VALUES ({elementId}, {mathcoverId})' \
                    .format(elementId=each_id, mathcoverId=temp_point_id)
                database_cursor.execute(database_statement)

        # input element special point relationship
        if special_point is not None:

            specialPointGrid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(mesh_path + 'special_point.vtu')
            specialPointNumber = specialPointGrid.GetNumberOfPoints()
            print('special_point_number:{}'.format(specialPointNumber))

            special_point_element_grid = vtkUnstructuredGrid()
            id_set = set()
            for each_point_id in range(specialPointNumber):
                temp_special_points = specialPointGrid.GetPoint(each_point_id)
                generic_cell = vtkGenericCell()
                sub_id = reference(0)
                temp_cell: vtkTetra = elementGrid.FindAndGetCell(temp_special_points, generic_cell, 0, 0.00001, sub_id,
                                                                 [0, 0, 0], [0, 0, 0, 0])
                temp_id = elementGrid.FindCell(temp_special_points, generic_cell, 0, 0.00001, sub_id, [0, 0, 0],
                                               [0, 0, 0, 0])

                # There is a bug that when temp_id = 0, it will be mistake assign as -1.
                if elementGrid.GetNumberOfCells() == 1:
                    temp_id = 0
                    temp_cell: vtkTetra = elementGrid.GetCell(0)

                # special point in element
                if temp_id >= 0:
                    database_statement = 'INSERT INTO ElementSpecialPoint (ElementId, SpecialPointId)' \
                                         'VALUES ({elementId}, {pointId})' \
                        .format(elementId=temp_id, pointId=each_point_id)
                    database_cursor.execute(database_statement)

                    # delete duplicate element
                    if temp_id not in id_set:
                        special_point_element_grid.InsertNextCell(temp_cell.GetCellType(), temp_cell.GetPointIds())
                        id_set.add(temp_id)
            special_point_element_grid.SetPoints(elementGrid.GetPoints())
            temp_writer = vtkXMLUnstructuredGridWriter()
            temp_writer.SetFileName(geometry_path + 'special_point_element.vtu')
            temp_writer.SetInputData(special_point_element_grid)
            temp_writer.Write()

    elementScalar = vtkDoubleArray()
    elementScalar.SetName('test_element_value')
    for each_id in range(elementNumber):
        elementScalar.InsertValue(each_id, each_id * 100)

    elementMaterialId = vtkIntArray()
    elementMaterialId.SetName('material_id')
    [elementMaterialId.InsertValue(i, 0) for i in range(elementNumber)]

    elementStrain = vtkDoubleArray()
    elementStrain.SetName('strain_total')
    elementStrain.SetNumberOfComponents(6)
    [elementStrain.InsertTuple(i, (0, 0, 0, 0, 0, 0)) for i in range(elementNumber)]

    elementStrain1 = vtkDoubleArray()
    elementStrain1.SetName('strain_1')
    elementStrain1.SetNumberOfComponents(3)
    [elementStrain1.InsertTuple(i, (0, 0, 0)) for i in range(elementNumber)]

    elementStrain1Value = vtkDoubleArray()
    elementStrain1Value.SetName('strain_1_value')
    elementStrain1Value.SetNumberOfComponents(1)
    [elementStrain1Value.InsertValue(i, 0) for i in range(elementNumber)]

    elementStrain2 = vtkDoubleArray()
    elementStrain2.SetName('strain_2')
    elementStrain2.SetNumberOfComponents(3)
    [elementStrain2.InsertTuple(i, (0, 0, 0)) for i in range(elementNumber)]

    elementStrain2Value = vtkDoubleArray()
    elementStrain2Value.SetName('strain_2_value')
    elementStrain2Value.SetNumberOfComponents(1)
    [elementStrain2Value.InsertValue(i, 0) for i in range(elementNumber)]

    elementStrain3 = vtkDoubleArray()
    elementStrain3.SetName('strain_3')
    elementStrain3.SetNumberOfComponents(3)
    [elementStrain3.InsertTuple(i, (0, 0, 0)) for i in range(elementNumber)]

    elementStrain3Value = vtkDoubleArray()
    elementStrain3Value.SetName('strain_3_value')
    elementStrain3Value.SetNumberOfComponents(1)
    [elementStrain3Value.InsertValue(i, 0) for i in range(elementNumber)]

    elementStrainMax = vtkDoubleArray()
    elementStrainMax.SetName('strain_Max')
    elementStrainMax.SetNumberOfComponents(3)
    [elementStrainMax.InsertTuple(i, (0, 0, 0)) for i in range(elementNumber)]

    elementStrainMaxValue = vtkDoubleArray()
    elementStrainMaxValue.SetName('strain_Max_value')
    elementStrainMaxValue.SetNumberOfComponents(1)
    [elementStrainMaxValue.InsertValue(i, 0) for i in range(elementNumber)]

    elementCracked = vtkIntArray()
    elementCracked.SetName('cracked')
    [elementCracked.InsertValue(i, 0) for i in range(elementNumber)]

    # crack surface number
    # crackSurfaceNumber = vtkIntArray()
    # crackSurfaceNumber.SetName('crack_surface_id')
    # [crackSurfaceNumber.InsertValue(i, -1) for i in range(elementNumber)]
    #
    # crackSurfaceNumber0 = vtkIntArray()
    # crackSurfaceNumber0.SetName('crack_surface_id_0')
    # [crackSurfaceNumber0.InsertValue(i, -1) for i in range(elementNumber)]

    pointScalar = vtkDoubleArray()
    pointNumber = elementGrid.GetNumberOfPoints()
    pointScalar.SetName('test_point_value')
    [pointScalar.InsertValue(i, i * 100) for i in range(pointNumber)]

    pointDisplacementIncrementVector = vtkDoubleArray()
    pointDisplacementIncrementVector.SetName('point_displacement_increment')
    pointDisplacementIncrementVector.SetNumberOfComponents(3)
    [pointDisplacementIncrementVector.InsertTuple(i, (0, 0, 0)) for i in range(pointNumber)]

    pointDisplacementTotalVector = vtkDoubleArray()
    pointDisplacementTotalVector.SetName('point_displacement_total')
    pointDisplacementTotalVector.SetNumberOfComponents(3)
    [pointDisplacementTotalVector.InsertTuple(i, (0, 0, 0)) for i in range(pointNumber)]

    pointCoordinateVector= vtkDoubleArray()
    pointCoordinateVector.SetName('point_coordinate')
    pointCoordinateVector.SetNumberOfComponents(3)
    [pointCoordinateVector.InsertTuple(i, (0, 0, 0)) for i in range(pointNumber)]

    pointVelocityVector= vtkDoubleArray()
    pointVelocityVector.SetName('point_velocity')
    pointVelocityVector.SetNumberOfComponents(3)
    [pointVelocityVector.InsertTuple(i, (0, 0, 0)) for i in range(pointNumber)]

    elementGrid.GetCellData().AddArray(elementScalar)
    elementGrid.GetCellData().AddArray(elementMaterialId)
    elementGrid.GetCellData().AddArray(elementStrain)

    elementGrid.GetCellData().AddArray(elementStrain1)
    elementGrid.GetCellData().AddArray(elementStrain2)
    elementGrid.GetCellData().AddArray(elementStrain3)
    elementGrid.GetCellData().AddArray(elementStrainMax)

    elementGrid.GetCellData().AddArray(elementStrain1Value)
    elementGrid.GetCellData().AddArray(elementStrain2Value)
    elementGrid.GetCellData().AddArray(elementStrain3Value)
    elementGrid.GetCellData().AddArray(elementStrainMaxValue)

    elementGrid.GetCellData().AddArray(elementCracked)
    # elementGrid.GetCellData().AddArray(crackSurfaceNumber)
    # elementGrid.GetCellData().AddArray(crackSurfaceNumber0)

    elementGrid.GetPointData().AddArray(pointScalar)
    elementGrid.GetPointData().AddArray(pointDisplacementIncrementVector)
    elementGrid.GetPointData().AddArray(pointDisplacementTotalVector)
    elementGrid.GetPointData().AddArray(pointCoordinateVector)
    elementGrid.GetPointData().AddArray(pointVelocityVector)

    outputFile = 'manifold_element.vtu'
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName(geometry_path + outputFile)
    writer.SetInputData(elementGrid)
    writer.Write()
