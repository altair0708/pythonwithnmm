from NMM.control_3D.ElementIO3D import ElementIOer3D
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, VTK_VERTEX, VTK_LINE, VTK_TRIANGLE, VTK_TETRA
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.GlobalVariable import PATH


def generate_geometry_info(mesh_path: str, geometry_path: str, cell_type: int):
    gmshGrid = ElementIOer3D.load_vtk_model(mesh_path + PATH.gmsh_file)
    # print(gmshGrid.GetNumberOfCells())
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
    writer.SetFileName(geometry_path + outputFile)
    writer.SetInputData(geometryGrid)
    writer.Write()
