from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader


def load_a_grid(file_name):
    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(file_name)
    reader.Update()
    return reader.GetOutput()
