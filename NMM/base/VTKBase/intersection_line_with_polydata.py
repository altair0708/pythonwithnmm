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
    #
    # npts = triangulated_polydata.GetNumberOfPoints()
    #
    # pts_d = vtkPoints()
    # pts_d.SetDataTypeToDouble()
    # pts_d.SetNumberOfPoints(npts)
    # for i in range(npts):
    #     pts_d.SetPoint(i, triangulated_polydata.GetPoint(i))
    #
    # poly_d = vtkPolyData()
    # poly_d.DeepCopy(triangulated_polydata)
    # poly_d.SetPoints(pts_d)

    # obb = vtkOBBTree()
    # obb.SetDataSet(poly_d)
    # obb.BuildLocator()

    obb = vtkOBBTree()
    obb.SetDataSet(triangulated_polydata)
    obb.BuildLocator()
    obb.SetTolerance(1e-6)

    id_list = vtkIdList()
    line_grid.GetCellPoints(0, id_list)

    point_0 = line_grid.GetPoint(id_list.GetId(0))
    point_1 = line_grid.GetPoint(id_list.GetId(1))

    # print("p0=", point_0)
    # print("p1=", point_1)
    # print("cell0 type=", line_grid.GetCell(0).GetCellType())
    # print("cell0 npts=", id_list.GetNumberOfIds())
    #
    # print(f'point_0: {point_0}')
    # print(f'point_1: {point_1}')
    # print(f'triangulated_polydata.GetBounds(): {triangulated_polydata.GetBounds()}')
    # print(f'triangulated_polydata.GetPoints().GetDataType(): {triangulated_polydata.GetPoints().GetDataType()}')
    # print(f'triangulated_polydata.GetNumberOfPolys(): {triangulated_polydata.GetNumberOfPolys()}')
    # tol = 0.00001
    # t = reference(0)
    # x = [0, 0, 0]
    # coord = [0, 0, 0]
    # subId = reference(0)
    # if obb.IntersectWithLine(point_0, point_1, tol, t, x, coord, subId):
    #     return True, x
    # else:
    #     return False, None
    # 直接调用（max_cells 可按需调大）
    # _debug_print_poly_triangles(triangulated_polydata, max_cells=20)
    # ====== END DEBUG ======

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


# ====== DEBUG: print triangle vertices in triangulated_polydata ======

def _debug_print_poly_triangles(poly, max_cells: int = 10):
    print("\n[DEBUG] ---- triangulated_polydata summary ----")
    print(f"[DEBUG] points={poly.GetNumberOfPoints()}, cells={poly.GetNumberOfCells()}, polys={poly.GetNumberOfPolys()}")
    b = poly.GetBounds()
    print(f"[DEBUG] bounds=({b[0]:.15g}, {b[1]:.15g}, {b[2]:.15g}, {b[3]:.15g}, {b[4]:.15g}, {b[5]:.15g})")
    try:
        dt = poly.GetPoints().GetDataType()
    except Exception:
        dt = None
    print(f"[DEBUG] points dtype={dt}  (10 means VTK_FLOAT)")

    id_list = vtkIdList()
    n = min(poly.GetNumberOfCells(), max_cells)

    print(f"[DEBUG] ---- first {n} cells (only triangles printed) ----")
    for ci in range(n):
        cell = poly.GetCell(ci)
        ctype = cell.GetCellType()
        npts = cell.GetNumberOfPoints()

        # 只打印三角形（npts==3）
        if npts != 3:
            print(f"[DEBUG] Cell {ci}: type={ctype}, npts={npts} (skip)")
            continue

        poly.GetCellPoints(ci, id_list)
        pids = [id_list.GetId(i) for i in range(id_list.GetNumberOfIds())]

        print(f"\n[DEBUG] Triangle cell {ci}: type={ctype}, pointIds={pids}")
        for vi, pid in enumerate(pids):
            x, y, z = poly.GetPoint(pid)
            print(f"[DEBUG]   v{vi}: pid={pid}, coord=({x:.15g}, {y:.15g}, {z:.15g})")


