from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyData, vtkGenericCell
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, reference
from vtkmodules.vtkFiltersGeneral import vtkOBBTree, vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter, vtkGeometryFilter
from NMM.base.VTKBase.write_file import debug_write_file
from NMM.base.VTKBase.test_example import generate_point_grid


def grid_to_polydata(vtk_model: vtkUnstructuredGrid):
    geometry_filter = vtkGeometryFilter()
    geometry_filter.SetInputData(vtk_model)
    geometry_filter.Update()
    return geometry_filter.GetOutput()


def outer():
    initial_obb = vtkOBBTree()
    function_cache = {'hash': -1, 'obb': initial_obb}

    def inner(vtk_model: vtkUnstructuredGrid, line_grid: vtkUnstructuredGrid):
        if function_cache['hash'] == hash(vtk_model):
            obb = function_cache['obb']
        else:
            triangle_filter = vtkDataSetTriangleFilter()
            triangle_filter.SetInputData(vtk_model)

            geometry_filter = vtkGeometryFilter()
            geometry_filter.SetInputConnection(triangle_filter.GetOutputPort())
            geometry_filter.Update()

            triangulated_polydata: vtkPolyData = geometry_filter.GetOutput()

            obb = vtkOBBTree()
            obb.SetDataSet(triangulated_polydata)
            obb.BuildLocator()

            function_cache['hash'] = hash(vtk_model)
            function_cache['obb'] = obb

        id_list = vtkIdList()
        line_grid.GetCellPoints(0, id_list)

        point_0 = line_grid.GetPoint(id_list.GetId(0))
        point_1 = line_grid.GetPoint(id_list.GetId(1))

        points = vtkPoints()
        obb.IntersectWithLine(point_0, point_1, points, None)
        point_number = points.GetNumberOfPoints()
        if point_number == 0:
            return False, None
        elif point_number == 1:
            return True, points.GetPoint(0)
        else:
            raise Exception(f'Intersection_number_error!!!: {point_number}')

    return inner


intersection_line_with_polydata_cache = outer()


def intersection_line_with_polydata(vtk_model: vtkUnstructuredGrid, line_grid: vtkUnstructuredGrid):
    hash_cache = hash(vtk_model)

    triangle_filter = vtkDataSetTriangleFilter()
    triangle_filter.SetInputData(vtk_model)

    geometry_filter = vtkGeometryFilter()
    geometry_filter.SetInputConnection(triangle_filter.GetOutputPort())
    geometry_filter.Update()

    triangulated_polydata: vtkPolyData = geometry_filter.GetOutput()

    obb = vtkOBBTree()
    obb.SetDataSet(triangulated_polydata)
    obb.BuildLocator()

    id_list = vtkIdList()
    line_grid.GetCellPoints(0, id_list)

    point_0 = line_grid.GetPoint(id_list.GetId(0))
    point_1 = line_grid.GetPoint(id_list.GetId(1))
    # tol = 0.00001
    # t = reference(0)
    # x = [0, 0, 0]
    # coord = [0, 0, 0]
    # subId = reference(0)
    # if obb.IntersectWithLine(point_0, point_1, tol, t, x, coord, subId):
    #     return True, x
    # else:
    #     return False, None

    points = vtkPoints()
    obb.IntersectWithLine(point_0, point_1, points, None)
    point_number = points.GetNumberOfPoints()
    if point_number == 0:
        return False, None
    elif point_number == 1:
        return True, points.GetPoint(0)
    elif point_number == 2:
        return False, None
    else:
        debug_write_file(line_grid, 'edge_intersect_with_crack_propagation.vtu')
        debug_write_file(triangulated_polydata, 'crack_propagate.vtp')
        for each in range(point_number):
            point_grid = generate_point_grid(points.GetPoint(each))
            debug_write_file(point_grid, f'point_grid_{each}.vtu')
        raise Exception(f'Intersection_number_error!!!: {point_number}')
