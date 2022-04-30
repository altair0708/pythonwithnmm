from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridWriter,
    vtkXMLUnstructuredGridReader
)
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, vtkFloatArray
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid,
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
        gmshGrid = uGridReader.GetOutput()
        mathCover = vtkUnstructuredGrid()
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

        mathCover.SetPoints(gmshGrid.GetPoints())
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
        vertexGrid = vtkUnstructuredGrid()
        for each_id in range(pointNumber):
            vertex = vtkVertex()
            vertex.GetPointIds().SetId(0, each_id)
            vertexGrid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

        vertexGrid.SetPoints(gmshGrid.GetPoints())

        outputFile = 'math_point.vtu'
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(output_path + outputFile)
        writer.SetInputData(vertexGrid)
        writer.Write()

    # generate relate manifold_element
    @staticmethod
    def generate_manifold_element(gmsh_file_name: str, output_path: str):
        uGridReader = vtkXMLUnstructuredGridReader()
        uGridReader.SetFileName(gmsh_file_name)
        uGridReader.Update()
        elementGrid: vtkUnstructuredGrid = uGridReader.GetOutput()

        elementScalar = vtkFloatArray()
        elementNumber = elementGrid.GetNumberOfCells()
        elementScalar.SetName('test_element_value')
        for each_id in range(elementNumber):
            elementScalar.InsertValue(each_id, each_id * 100)

        pointScalar = vtkFloatArray()
        pointNumber = elementGrid.GetNumberOfPoints()
        pointScalar.SetName('test_point_value')
        [pointScalar.InsertValue(i, i * 100) for i in range(pointNumber)]

        elementGrid.GetCellData().SetScalars(elementScalar)
        elementGrid.GetPointData().SetScalars(pointScalar)

        outputFile = 'manifold_element.vtu'
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(output_path + outputFile)
        writer.SetInputData(elementGrid)
        writer.Write()

    @staticmethod
    def generate_all_vtu_file(gmsh_file_name, output_path):
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_VERTEX)
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_LINE)
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_TRIANGLE)
        GmshReader.generate_geometry_info(gmsh_file_name, output_path, VTK_TETRA)

        tetrahedron_file = 'geometry_tetrahedron.vtu'
        gmsh_tetrahedron_file_name = output_path + tetrahedron_file

        GmshReader.generate_math_cover(gmsh_tetrahedron_file_name, output_path)
        GmshReader.generate_math_point(gmsh_tetrahedron_file_name, output_path)

        GmshReader.generate_manifold_element(gmsh_tetrahedron_file_name, output_path)


if __name__ == '__main__':
    file_name = 'original_gmsh.vtu'
    work_path = '../../data_3D/'
    gmsh_file = work_path + file_name

    GmshReader.generate_all_vtu_file(gmsh_file, work_path)
