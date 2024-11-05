from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon, vtkPlane, vtkTriangle, vtkTetra, vtkPolyData, vtkCellArray, vtkPolyLine, vtkStaticPointLocator, vtkMergePoints, vtkPointLocator
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersCore import vtkClipPolyData, vtkAppendFilter, vtkFeatureEdges, vtkStripper, vtkAppendPolyData, vtkPolyDataPlaneCutter, vtkCleanPolyData
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
from NMM.base.VTKBase import debug_write_file


def clip_a_surface(surface_grid: vtkUnstructuredGrid, origin_point, normal_vector):

    clip_plane = vtkPlane()
    clip_plane.SetOrigin(origin_point)
    clip_plane.SetNormal(normal_vector)

    geometry = vtkGeometryFilter()
    geometry.SetInputData(surface_grid)

    cutter = vtkPolyDataPlaneCutter()
    cutter.SetInputConnection(geometry.GetOutputPort())
    cutter.SetPlane(clip_plane)

    u_appender_1 = vtkAppendFilter()
    u_appender_1.SetInputConnection(cutter.GetOutputPort())
    u_appender_1.Update()

    cut_line = u_appender_1.GetOutput()

    if cut_line.GetNumberOfCells() == 0:
        return cut_line, None, None

    edges = vtkFeatureEdges()
    edges.SetInputConnection(geometry.GetOutputPort())
    edges.BoundaryEdgesOn()
    edges.FeatureEdgesOff()
    edges.ManifoldEdgesOff()
    edges.NonManifoldEdgesOff()

    clipper = vtkClipPolyData()
    clipper.GenerateClippedOutputOn()
    clipper.InsideOutOn()
    clipper.SetClipFunction(clip_plane)
    clipper.SetInputConnection(edges.GetOutputPort())

    debug_write_file(cut_line, 'cut_line.vtu')
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

    new_surface_0 = u_appender.GetOutput()

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

    new_surface_1 = u_appender_0.GetOutput()

    assert cut_line.GetNumberOfCells() == 1
    assert new_surface_0.GetNumberOfCells() == 1
    assert new_surface_1.GetNumberOfCells() == 1

    return cut_line, new_surface_0, new_surface_1

