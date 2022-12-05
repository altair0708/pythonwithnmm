import numpy as np
from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridWriter,
    vtkXMLUnstructuredGridReader
)
from NMM.control_3D.ElementIO3D import ElementIOer3D
from NMM.base.CopyFunction import copy_vtk_cell, copy_polyhedron
from NMM.base.ElementClipFunction import clip_a_vtk_cell
from NMM.base.ModifyVtkCell import insert_a_cell
from NMM.base.PropertyGetSetFunction import set_property
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, vtkDoubleArray, vtkIntArray, reference
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid,
    vtkCellData,
    vtkTetra,
    vtkGenericCell,
    vtkCell,
    vtkPolyData,
    vtkPolygon,
    vtkVertex,
    VTK_VERTEX,
    VTK_LINE,
    VTK_TRIANGLE,
    VTK_POLYGON,
    VTK_TETRA,
    VTK_POLYHEDRON
)
import sqlite3


class GmshReader:
    # simple extraction
    @staticmethod
    def generate_geometry_info(gmsh_file_name: str, output_path: str, cell_type: int):
        uGridReader = vtkXMLUnstructuredGridReader()
        uGridReader.SetFileName(gmsh_file_name)
        uGridReader.Update()
        gmshGrid = uGridReader.GetOutput()

        geometryGrid = vtkUnstructuredGrid()
        cellNumber = gmshGrid.GetNumberOfCells()

        for cellId in range(cellNumber):
            if gmshGrid.GetCellType(cellId) == cell_type:
                tempCell: vtkCell = gmshGrid.GetCell(cellId)
                geometryGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
        geometryGrid.SetPoints(gmshGrid.GetPoints())
        if cell_type == VTK_VERTEX:
            outputFile = 'geometry_vertex.vtu'
        elif cell_type == VTK_LINE:
            outputFile = 'geometry_line.vtu'
        elif cell_type == VTK_TRIANGLE:
            outputFile = 'geometry_surface.vtu'
        elif cell_type == VTK_TETRA:
            outputFile = 'geometry_tetrahedron.vtu'
        else:
            raise Exception('Cell type error!!')

        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(output_path + outputFile)
        writer.SetInputData(geometryGrid)
        writer.Write()

    # generate relate math cover
    @staticmethod
    def generate_math_cover(gmsh_file_name: str, output_path: str):
        uGridReader = vtkXMLUnstructuredGridReader()
        uGridReader.SetFileName(gmsh_file_name)
        uGridReader.Update()
        gmshGrid: vtkUnstructuredGrid = uGridReader.GetOutput()
        mathCover = vtkUnstructuredGrid()

        mathPointId = vtkIntArray()
        mathPointId.SetName('math_cover_id')
        mathPointId.SetNumberOfComponents(1)

        mathPointCoordinate = vtkDoubleArray()
        mathPointCoordinate.SetName('math_cover_coordinate')
        mathPointCoordinate.SetNumberOfComponents(3)

        mathPointDisplacement = vtkDoubleArray()
        mathPointDisplacement.SetName('math_cover_displacement')
        mathPointDisplacement.SetNumberOfComponents(3)

        print('original mesh info:')
        print('number of points: {}'.format(gmshGrid.GetNumberOfPoints()))
        print('number of cells: {}'.format(gmshGrid.GetNumberOfCells()))
        for each_id in range(gmshGrid.GetNumberOfPoints()):
            cellIdList = vtkIdList()
            pointId = each_id
            gmshGrid.GetPointCells(pointId, cellIdList)

            # Generate new grid of selected cell
            mathGrid = vtkUnstructuredGrid()
            idNumber = cellIdList.GetNumberOfIds()
            for eachId in range(idNumber):
                cellId = cellIdList.GetId(eachId)
                tempCell: vtkCell = gmshGrid.GetCell(cellId)
                mathGrid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
            mathGrid.SetPoints(gmshGrid.GetPoints())

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

            mathCover.InsertNextCell(VTK_POLYHEDRON, faceIdList)
            mathPointId.InsertValue(each_id, each_id)
            mathPointCoordinate.InsertNextTuple(gmshGrid.GetPoint(each_id))
            temp_displacement = (0, 0, 0)
            mathPointDisplacement.InsertNextTuple(temp_displacement)
            # print(mathPointCoordinate.GetTuple(each_id) == gmshGrid.GetPoint(each_id))

        mathCover.SetPoints(gmshGrid.GetPoints())
        mathCover.GetCellData().AddArray(mathPointId)
        mathCover.GetCellData().AddArray(mathPointCoordinate)
        mathCover.GetCellData().AddArray(mathPointDisplacement)

        mathWriter = vtkXMLUnstructuredGridWriter()
        outputFile = output_path + 'math_cover.vtu'
        mathWriter.SetFileName(outputFile)
        mathWriter.SetInputData(mathCover)
        mathWriter.Write()

    @staticmethod
    def generate_math_point(gmsh_file_name: str, output_path: str):
        uGridReader = vtkXMLUnstructuredGridReader()
        uGridReader.SetFileName(gmsh_file_name)
        uGridReader.Update()
        gmshGrid: vtkUnstructuredGrid = uGridReader.GetOutput()
        pointNumber = gmshGrid.GetNumberOfPoints()
        print('math_cover_number:{}'.format(pointNumber))
        vertexGrid = vtkUnstructuredGrid()
        for each_id in range(pointNumber):
            vertex = vtkVertex()
            vertex.GetPointIds().SetId(0, each_id)
            vertexGrid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

        mathPointDisplacement = vtkDoubleArray()
        mathPointDisplacement.SetName('math_point_displacement')
        mathPointDisplacement.SetNumberOfComponents(3)

        vertexGrid.SetPoints(gmshGrid.GetPoints())
        vertexGrid.GetPointData().AddArray(mathPointDisplacement)

        outputFile = 'math_point.vtu'
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(output_path + outputFile)
        writer.SetInputData(vertexGrid)
        writer.Write()

    # generate relate manifold_element
    @staticmethod
    def generate_manifold_element(gmsh_file_name: str, special_point_file_name: str, output_path: str):

        elementGrid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(gmsh_file_name)
        elementNumber = elementGrid.GetNumberOfCells()
        print('element_number:{}'.format(elementNumber))

        # crack_element_grid: vtkUnstructuredGrid = vtkUnstructuredGrid()
        # crack_element_grid.DeepCopy(elementGrid)
        # crack_element_number = crack_element_grid.GetNumberOfCells()
        # print('crack_element_number:{}'.format(crack_element_number))

        # connect to database
        with sqlite3.connect(output_path + 'manifold_mathcover.db') as connection:
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
                                         'VALUES ({elementId}, {mathcoverId})'\
                        .format(elementId=each_id, mathcoverId=temp_point_id)
                    database_cursor.execute(database_statement)

            # input element special point relationship
            if special_point_file_name != '':

                specialPointGrid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(special_point_file_name)
                specialPointNumber = specialPointGrid.GetNumberOfPoints()
                print('special_point_number:{}'.format(specialPointNumber))

                special_point_element_grid = vtkUnstructuredGrid()
                for each_point_id in range(specialPointNumber):
                    temp_special_points = specialPointGrid.GetPoint(each_point_id)
                    generic_cell = vtkGenericCell()
                    sub_id = reference(0)
                    temp_cell: vtkTetra = elementGrid.FindAndGetCell(temp_special_points, generic_cell, 0, 0.0, sub_id, [0, 0, 0], [0, 0, 0, 0])
                    temp_id = elementGrid.FindCell(temp_special_points, generic_cell, 0, 0.0, sub_id, [0, 0, 0], [0, 0, 0, 0])
                    database_statement = 'INSERT INTO ElementSpecialPoint (ElementId, SpecialPointId)' \
                                         'VALUES ({elementId}, {pointId})' \
                        .format(elementId=temp_id, pointId=each_point_id)
                    database_cursor.execute(database_statement)
                    special_point_element_grid.InsertNextCell(temp_cell.GetCellType(), temp_cell.GetPointIds())
                special_point_element_grid.SetPoints(elementGrid.GetPoints())
                temp_writer = vtkXMLUnstructuredGridWriter()
                temp_writer.SetFileName(output_path + 'special_point_element.vtu')
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

        elementCracked = vtkIntArray()
        elementCracked.SetName('cracked')
        [elementCracked.InsertValue(i, 0) for i in range(elementNumber)]

        # crack edge number
        crackEdgeNumber = vtkIntArray()
        crackEdgeNumber.SetName('crack_edge_number')
        [crackEdgeNumber.InsertValue(i, 0) for i in range(elementNumber)]

        # crack surface number
        crackSurfaceNumber = vtkIntArray()
        crackSurfaceNumber.SetName('crack_surface_id')
        [crackSurfaceNumber.InsertValue(i, 0) for i in range(elementNumber)]

        # crack edges
        crackEdge1 = vtkDoubleArray()
        crackEdge1.SetName('crack_edge_1')
        crackEdge1.SetNumberOfComponents(6)
        [crackEdge1.InsertTuple(i, (0, 0, 0, 0, 0, 0)) for i in range(elementNumber)]

        crackEdge2 = vtkDoubleArray()
        crackEdge2.SetName('crack_edge_2')
        crackEdge2.SetNumberOfComponents(6)
        [crackEdge2.InsertTuple(i, (0, 0, 0, 0, 0, 0)) for i in range(elementNumber)]

        crackEdge3 = vtkDoubleArray()
        crackEdge3.SetName('crack_edge_3')
        crackEdge3.SetNumberOfComponents(6)
        [crackEdge3.InsertTuple(i, (0, 0, 0, 0, 0, 0)) for i in range(elementNumber)]

        crackEdge4 = vtkDoubleArray()
        crackEdge4.SetName('crack_edge_4')
        crackEdge4.SetNumberOfComponents(6)
        [crackEdge4.InsertTuple(i, (0, 0, 0, 0, 0, 0)) for i in range(elementNumber)]

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

        elementGrid.GetCellData().AddArray(elementScalar)
        elementGrid.GetCellData().AddArray(elementMaterialId)
        elementGrid.GetCellData().AddArray(elementStrain)

        elementGrid.GetCellData().AddArray(elementCracked)
        elementGrid.GetCellData().AddArray(crackEdgeNumber)
        elementGrid.GetCellData().AddArray(crackSurfaceNumber)
        elementGrid.GetCellData().AddArray(crackEdge1)
        elementGrid.GetCellData().AddArray(crackEdge2)
        elementGrid.GetCellData().AddArray(crackEdge3)
        elementGrid.GetCellData().AddArray(crackEdge4)

        elementGrid.GetPointData().AddArray(pointScalar)
        elementGrid.GetPointData().AddArray(pointDisplacementIncrementVector)
        elementGrid.GetPointData().AddArray(pointDisplacementTotalVector)

        outputFile = 'manifold_element.vtu'
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(output_path + outputFile)
        writer.SetInputData(elementGrid)
        writer.Write()

    @staticmethod
    def generate_crack_surface_file(initial_crack_file: str, manifold_element_file: str, output_path: str):
        crack_surface_grid = vtkUnstructuredGrid()
        crackElementId = vtkIntArray()
        crackElementId.SetName('element_id')
        crackElementId.SetNumberOfComponents(1)
        crack_surface_grid.GetCellData().AddArray(crackElementId)

        initial_crack_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(initial_crack_file)
        initial_crack_polygon: vtkPolygon = initial_crack_grid.GetCell(0)
        initial_crack_polygon: vtkPolygon = copy_vtk_cell(initial_crack_polygon, initial_crack_grid.GetPoints())

        # compute the normal vector and origin point of the plane of the initial crack polygon
        normal = [0, 0, 0]
        temp_polygon_points: vtkPoints = initial_crack_polygon.GetPoints()
        vtkPolygon.ComputeNormal(temp_polygon_points, normal)
        origin = temp_polygon_points.GetPoint(0)

        manifold_element_grid: vtkUnstructuredGrid = ElementIOer3D.load_vtk_model(manifold_element_file)
        element_number = manifold_element_grid.GetNumberOfCells()

        for each_id in range(element_number):
            temp_vtk_cell = manifold_element_grid.GetCell(each_id)
            temp_vtk_cell = copy_polyhedron(temp_vtk_cell, manifold_element_grid.GetPoints())
            if temp_vtk_cell.IntersectWithCell(initial_crack_polygon):
                try:
                    temp_crack_surface, _, _ = clip_a_vtk_cell(temp_vtk_cell, origin_point=origin, normal_vector=normal)
                except AssertionError:
                    continue

                crack_surface_id = crack_surface_grid.GetNumberOfCells()
                set_property(manifold_element_grid, 'cracked', each_id, np.array((3,)))
                set_property(manifold_element_grid, 'crack_surface_id', each_id, np.array((crack_surface_id,)))

                insert_a_cell(crack_surface_grid, temp_crack_surface)
                crackElementId.InsertNextValue(each_id)

        def write_vtk_model(vtk_model, vtk_file_name, path):
            crackWriter = vtkXMLUnstructuredGridWriter()
            crackWriter.SetFileName(path + vtk_file_name)
            crackWriter.SetInputData(vtk_model)
            crackWriter.Write()

        write_vtk_model(manifold_element_grid, 'manifold_element.vtu', output_path)
        write_vtk_model(crack_surface_grid, 'crack_surface.vtu', output_path)


        # if crack_surface_file is not None:
        #     crackReader = vtkXMLUnstructuredGridReader()
        #     crackReader.SetFileName(crack_surface_file)
        #     crackReader.Update()
        #     crackGrid: vtkUnstructuredGrid = crackReader.GetOutput()
        # else:
        #     crackGrid = vtkUnstructuredGrid()
        #
        # crackElementId = vtkIntArray()
        # crackElementId.SetName('element_id')
        # crackElementId.SetNumberOfComponents(1)
        # crackGrid.GetCellData().AddArray(crackElementId)
        #

    @staticmethod
    def generate_all_vtu_file(gmsh_file_name, special_point_file_name, output_path):
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_VERTEX)
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_LINE)
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_TRIANGLE)
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_TETRA)

        tetrahedron_file = 'geometry_tetrahedron.vtu'
        gmsh_tetrahedron_file_name = output_path + tetrahedron_file

        GmshReader.generate_math_cover(gmsh_tetrahedron_file_name, output_path)
        GmshReader.generate_math_point(gmsh_tetrahedron_file_name, output_path)
        GmshReader.generate_manifold_element(gmsh_tetrahedron_file_name, special_point_file_name, output_path)

        element_manifold_file_name = output_path + 'manifold_element.vtu'
        initial_crack_file_name = output_path + 'initial_crack.vtu'
        GmshReader.generate_crack_surface_file(initial_crack_file_name, element_manifold_file_name, output_path)


if __name__ == '__main__':
    # file_name = 'simplex.vtu'
    # special_point_file = 'special_points_simplex.vtu'
    file_name = 'cylinder.vtu'
    # special_point_file = 'special_point_1.vtu'
    special_point_file = 'special_point.vtu'
    work_path = '../../data_3D/'
    gmsh_file = work_path + file_name
    special_point_file = work_path + special_point_file

    GmshReader.generate_all_vtu_file(gmsh_file, special_point_file, work_path)

