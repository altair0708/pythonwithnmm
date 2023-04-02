from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLUnstructuredGridReader
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkPolygon
from NMM.base.CheckPointInPolygon import check_point_in_polygon

reader_0 = vtkXMLUnstructuredGridReader()
reader_0.SetFileName('element.vtu')
reader_0.Update()
element_grid: vtkUnstructuredGrid = reader_0.GetOutput()

reader_1 = vtkXMLUnstructuredGridReader()
reader_1.SetFileName('surface.vtu')
reader_1.Update()
surface_grid: vtkUnstructuredGrid = reader_1.GetOutput()

element_vtk_cell: vtkTetra = element_grid.GetCell(0)
crack_surface_vtk_cell: vtkTetra = surface_grid.GetCell(0)

for each_surface in range(element_vtk_cell.GetNumberOfFaces()):
    surface_vtk_cell = element_vtk_cell.GetFace(each_surface)

    point_list = []
    for each_point_sequence in range(crack_surface_vtk_cell.GetNumberOfPoints()):
        temp_point = crack_surface_vtk_cell.GetPoints().GetPoint(each_point_sequence)
        if check_point_in_polygon(temp_point, surface_vtk_cell):
            point_list.append(temp_point)
    print(len(point_list))

reader_2 = vtkXMLUnstructuredGridReader()
reader_2.SetFileName('error_0.vtu')
reader_2.Update()
error_grid: vtkUnstructuredGrid = reader_2.GetOutput()

surface_vtk_cell: vtkPolygon = error_grid.GetCell(0)
crack_surface_vtk_cell: vtkTetra = error_grid.GetCell(1)

point_list = []
for each_point_sequence in range(crack_surface_vtk_cell.GetNumberOfPoints()):
    temp_point = crack_surface_vtk_cell.GetPoints().GetPoint(each_point_sequence)
    if check_point_in_polygon(temp_point, surface_vtk_cell):
        point_list.append(temp_point)
print(len(point_list))
