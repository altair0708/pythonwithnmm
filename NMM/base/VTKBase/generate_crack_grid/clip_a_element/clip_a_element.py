from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPlane, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkCutter, vtkAppendFilter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from NMM.base.VTKBase import write_file


def clip_a_element(element_grid: vtkUnstructuredGrid, origin, normal):
    assert element_grid.GetNumberOfCells() == 1

    normal = tuple(i for i in normal)
    clip_plane_1 = vtkPlane()
    clip_plane_1.SetOrigin(origin)
    clip_plane_1.SetNormal(normal)

    counter_normal = tuple(-i for i in normal)
    clip_plane_2 = vtkPlane()
    clip_plane_2.SetOrigin(origin)
    clip_plane_2.SetNormal(counter_normal)

    def clip(grid: vtkUnstructuredGrid, plane: vtkPlane):
        clipper = vtkClipDataSet()
        clipper.SetClipFunction(plane)
        clipper.SetInputData(grid)
        clipper.Update()
        result: vtkUnstructuredGrid = clipper.GetOutput()
        return result

    # total of three times cut/clip
    # first clip: generate the cross section of the element
    cutter = vtkCutter()
    cutter.SetCutFunction(clip_plane_1)
    cutter.SetInputData(element_grid)

    # triangle or polygon
    cutter.GenerateTrianglesOff()
    # cutter.GenerateTrianglesOn()

    appender = vtkAppendFilter()
    appender.SetInputConnection(cutter.GetOutputPort())
    appender.Update()
    cut_plane: vtkUnstructuredGrid = appender.GetOutput()

    # second and third cut: generate two new vtk cell of the element
    grid_1 = clip(element_grid, clip_plane_1)
    grid_2 = clip(element_grid, clip_plane_2)

    assert grid_1.GetNumberOfCells() != 0
    assert grid_2.GetNumberOfCells() != 0
    assert cut_plane.GetNumberOfCells() != 0

    return cut_plane, grid_1, grid_2
