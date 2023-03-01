from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def write_error_vtu(u_grid: vtkUnstructuredGrid, id_number: int):
    writer = vtkXMLUnstructuredGridWriter()
    file_name = 'error_{}.vtu'.format(id_number)
    writer.SetFileName(file_name)
    writer.SetInputData(u_grid)
    writer.Write()

