from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon, vtkPlane, vtkTriangle, vtkTetra, vtkPolyData, vtkCellArray, vtkPolyLine, vtkStaticPointLocator, vtkMergePoints, vtkPointLocator
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkIdListCollection, vtkVersion, reference
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet, vtkCleanUnstructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersCore import vtkClipPolyData, vtkAppendFilter, vtkFeatureEdges, vtkStripper, vtkAppendPolyData, vtkPolyDataPlaneCutter, vtkCleanPolyData
from vtkmodules.vtkFiltersGeneric import vtkGenericClip
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter
from vtkmodules.vtkCommonMisc import vtkPolygonBuilder
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
from NMM.base.VTKBase import write_file


points = vtkPoints()
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(-1, 1, 1)
points.InsertNextPoint(-3, 0.5, 2)
points.InsertNextPoint(-1, 0, 1)

polygon = vtkPolygon()
polygon.GetPointIds().SetNumberOfIds(5)
polygon.GetPointIds().SetId(0, 0)
polygon.GetPointIds().SetId(1, 1)
polygon.GetPointIds().SetId(2, 2)
polygon.GetPointIds().SetId(3, 3)
polygon.GetPointIds().SetId(4, 4)

origin = (0, 0, 10)
normal = (1, 0, 0)

clip_plane = vtkPlane()
clip_plane.SetOrigin(origin)
clip_plane.SetNormal(normal)

u_grid = vtkUnstructuredGrid()
u_grid.InsertNextCell(polygon.GetCellType(), polygon.GetPointIds())
u_grid.SetPoints(points)

geometry = vtkGeometryFilter()
geometry.SetInputData(u_grid)

edges = vtkFeatureEdges()
edges.SetInputConnection(geometry.GetOutputPort())
edges.BoundaryEdgesOn()
edges.FeatureEdgesOff()
edges.ManifoldEdgesOff()
edges.NonManifoldEdgesOff()

clipper = vtkClipPolyData()
clipper.GenerateClippedOutputOn()
# clipper.InsideOutOn()
clipper.SetClipFunction(clip_plane)
clipper.SetInputConnection(edges.GetOutputPort())

cutter = vtkPolyDataPlaneCutter()
cutter.SetInputConnection(geometry.GetOutputPort())
cutter.SetPlane(clip_plane)

appender = vtkAppendPolyData()
appender.AddInputConnection(cutter.GetOutputPort())
appender.AddInputConnection(clipper.GetOutputPort(1))

cleaner = vtkCleanPolyData()
cleaner.PointMergingOn()
cleaner.SetInputConnection(appender.GetOutputPort())

stripper = vtkStripper()
stripper.SetInputConnection(cleaner.GetOutputPort())

extractor = vtkContourLoopExtraction()
extractor.SetInputConnection(stripper.GetOutputPort())

u_appender = vtkAppendFilter()
u_appender.SetInputConnection(extractor.GetOutputPort())
u_appender.Update()

write_file(u_appender.GetOutput(), 're014_0.vtu')

appender_0 = vtkAppendPolyData()
appender_0.AddInputConnection(cutter.GetOutputPort())
appender_0.AddInputConnection(clipper.GetOutputPort(0))

cleaner_0 = vtkCleanPolyData()
cleaner_0.PointMergingOn()
cleaner_0.SetInputConnection(appender_0.GetOutputPort())

stripper_0 = vtkStripper()
stripper_0.SetInputConnection(cleaner_0.GetOutputPort())

extractor_0 = vtkContourLoopExtraction()
extractor_0.SetInputConnection(stripper_0.GetOutputPort())

u_appender_0 = vtkAppendFilter()
u_appender_0.SetInputConnection(extractor_0.GetOutputPort())
u_appender_0.Update()

write_file(u_appender_0.GetOutput(), 're014_1.vtu')

u_appender_1 = vtkAppendFilter()
u_appender_1.SetInputConnection(cutter.GetOutputPort())
u_appender_1.Update()

write_file(u_appender_1.GetOutput(), 're014_2.vtu')
