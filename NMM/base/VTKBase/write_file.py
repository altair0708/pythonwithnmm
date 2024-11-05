from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


def write_file(vtk_model: vtkUnstructuredGrid, file_path: str):
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName(file_path)
    writer.SetInputData(vtk_model)
    writer.Write()


def debug_write_file(vtk_model: vtkUnstructuredGrid, file_name: str):
    file_path = 'D:\\science\\NMM\\python-NMM\\debug\\' + file_name
    write_file(vtk_model, file_path)
