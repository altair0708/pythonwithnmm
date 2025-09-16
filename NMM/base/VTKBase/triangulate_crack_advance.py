from vtkmodules.vtkCommonDataModel import vtkTriangle, vtkUnstructuredGrid, VTK_TRIANGLE
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter


def triangulate_crack_advance(input_ugrid):
    triangle_filter = vtkDataSetTriangleFilter()
    triangle_filter.SetInputData(input_ugrid)
    triangle_filter.Update()

    output_ugrid = vtkUnstructuredGrid()
    output_ugrid.ShallowCopy(triangle_filter.GetOutput())
    return output_ugrid


def iterate_triangles_from_ugrid(input_ugrid):
    """
    将由 vtkTriangle 组成的 vtkUnstructuredGrid 转换为迭代器，
    每次返回一个包含单个 vtkTriangle 的 vtkUnstructuredGrid。

    Parameters:
        input_ugrid (vtkUnstructuredGrid): 只包含 vtkTriangle 的网格

    Yields:
        vtkUnstructuredGrid: 每个单独三角形组成的子网格
    """
    num_cells = input_ugrid.GetNumberOfCells()
    points = input_ugrid.GetPoints()

    for i in range(num_cells):
        cell = input_ugrid.GetCell(i)
        if cell.GetCellType() != VTK_TRIANGLE:
            continue  # 可选：也可以 raise 错误

        ids = [cell.GetPointId(j) for j in range(3)]
        p_coords = [points.GetPoint(pt_id) for pt_id in ids]

        # 创建新点集
        new_points = vtkPoints()
        new_points.InsertNextPoint(p_coords[0])
        new_points.InsertNextPoint(p_coords[1])
        new_points.InsertNextPoint(p_coords[2])

        # 创建新三角形单元（局部点 ID）
        triangle = vtkTriangle()
        triangle.GetPointIds().SetId(0, 0)
        triangle.GetPointIds().SetId(1, 1)
        triangle.GetPointIds().SetId(2, 2)

        # 封装为 UnstructuredGrid
        subgrid = vtkUnstructuredGrid()
        subgrid.SetPoints(new_points)
        subgrid.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())

        yield subgrid


def triangle_and_iterate_grid(vtk_model: vtkUnstructuredGrid):
    triangulate_result = triangulate_crack_advance(vtk_model)
    iteration = iterate_triangles_from_ugrid(triangulate_result)
    return iteration
