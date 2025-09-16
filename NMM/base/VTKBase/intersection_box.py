from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkBoundingBox
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersGeneral import vtkOBBTree, vtkIntersectionPolyDataFilter


def unstructuredgrid_to_polydata(unstructured_grid: vtkUnstructuredGrid):
    surface_filter = vtkDataSetSurfaceFilter()
    surface_filter.SetInputData(unstructured_grid)
    surface_filter.Update()
    polydata = surface_filter.GetOutput()
    return polydata


def intersection_grid(grid_0: vtkUnstructuredGrid, grid_1: vtkUnstructuredGrid):
    polydata_0 = unstructuredgrid_to_polydata(grid_0)
    polydata_1 = unstructuredgrid_to_polydata(grid_1)

    # intersection = vtkIntersectionPolyDataFilter()
    # intersection.SetInputData(0, polydata_0)
    # intersection.SetInputData(1, polydata_1)
    # intersection.Update()
    intersection_0 = vtkOBBTree()
    intersection_0.SetDataSet(polydata_0)
    intersection_0.BuildLocator()

    intersection_1 = vtkOBBTree()
    intersection_1.SetDataSet(polydata_1)
    intersection_1.BuildLocator()

    print(intersection_0.IntersectWithOBBTree(intersection_1))


def intersection_box(u_grid_0: vtkUnstructuredGrid, u_grid_1: vtkUnstructuredGrid):
    box_0 = vtkBoundingBox(u_grid_0.GetBounds())
    box_1 = vtkBoundingBox(u_grid_1.GetBounds())
    return box_0.Intersects(box_1)


