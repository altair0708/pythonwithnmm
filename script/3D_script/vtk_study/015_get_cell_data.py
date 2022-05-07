from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData
from vtkmodules.vtkCommonCore import vtkDataArray

gmsh_reader = vtkXMLUnstructuredGridReader()
gmsh_reader.SetFileName('../../../data_3D/manifold_element.vtu')
gmsh_reader.Update()
uGrid: vtkUnstructuredGrid = gmsh_reader.GetOutput()
cellData: vtkCellData = uGrid.GetCellData()
cellArray: vtkDataArray = cellData.GetArray(1)
print(cellArray.GetName())

