from vtkmodules.vtkIOXML import vtkXMLDataSetWriter
from vtkmodules.vtkCommonCore import vtkPoints, vtkFloatArray
from vtkmodules.vtkFiltersCore import vtk3DLinearGridPlaneCutter
from vtkmodules.vtkFiltersGeneral import vtkClipVolume
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPlanes,
    vtkCellArray,
    vtkHexahedron,
    vtkUnstructuredGrid,
    VTK_HEXAHEDRON
)
from vtkmodules.vtkCommonCore import vtkIdList

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)
points.InsertNextPoint(1, 0, 1)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(0, 1, 1)
points.InsertNextPoint(0, 0, 2)
points.InsertNextPoint(1, 0, 2)
points.InsertNextPoint(1, 1, 2)
points.InsertNextPoint(0, 1, 2)

polygon1 = vtkHexahedron()
[polygon1.GetPointIds().SetId(i, i) for i in range(8)]
polygon2 = vtkHexahedron()
[polygon2.GetPointIds().SetId(i, i + 4) for i in range(8)]

polygons = vtkCellArray()
polygons.InsertNextCell(polygon1)
polygons.InsertNextCell(polygon2)

scalar2 = vtkFloatArray()
scalar2.SetName('Test_point_value')
[scalar2.InsertValue(i, i) for i in range(12)]


polyData = vtkUnstructuredGrid()
polyData.SetPoints(points)
polyData.SetCells(VTK_HEXAHEDRON, polygons)
polyData.GetPointData().SetScalars(scalar2)

cuttingPlane = vtkPlane()
cuttingPlane.SetOrigin(0.3, 0, 0)
cuttingPlane.SetNormal(1, 0, 0)
cuttingPlane1 = vtkPlane()
cuttingPlane1.SetOrigin(0.7, 0, 0)
cuttingPlane1.SetNormal(1, 0, 0)

cutter = vtk3DLinearGridPlaneCutter()
cutter.SetPlane(cuttingPlane1)
cutter.SetInputData(polyData)
cutter.Update()
polyData = cutter.GetOutput()
print(polyData)

writer = vtkXMLDataSetWriter()
writer.SetFileName('polyData_test.vtp')
writer.SetInputData(polyData)
writer.Write()
