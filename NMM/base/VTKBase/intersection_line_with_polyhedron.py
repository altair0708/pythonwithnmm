from vtkmodules.vtkCommonDataModel import vtkLine, vtkUnstructuredGrid, vtkPolyhedron, VTK_LINE, VTK_POLYHEDRON, vtkEmptyCell
from vtkmodules.vtkCommonCore import reference, vtkPoints, vtkIdList


def get_line_points(line_grid):
    """提取vtkLine两个端点"""
    cell = line_grid.GetCell(0)
    assert isinstance(cell, vtkLine), "应为vtkLine"
    p0 = line_grid.GetPoint(cell.GetPointId(0))
    p1 = line_grid.GetPoint(cell.GetPointId(1))
    return p0, p1


def intersection_line_with_polyhedron(line_grid, poly_grid, tolerance=1e-6):
    """判断一个vtkPolyhedron是否与vtkLine相交"""
    poly_cell = poly_grid.GetCell(0)
    assert isinstance(poly_cell, vtkPolyhedron), "应为vtkPolyhedron"
    polyhedron = vtkPolyhedron.SafeDownCast(poly_cell)

    p0, p1 = get_line_points(line_grid)

    t = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    subId = reference(0)

    result = polyhedron.IntersectWithLine(p0, p1, tolerance, t, x, pcoords, subId)
    return result == 1


def create_line_unstructuredgrid(p0, p1):
    """创建一个包含 vtkLine 的 UnstructuredGrid"""
    points = vtkPoints()
    points.InsertNextPoint(p0)
    points.InsertNextPoint(p1)

    line = vtkLine()
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 1)

    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(VTK_LINE, line.GetPointIds())
    return ugrid


def create_cube_polyhedron_unstructuredgrid():
    """创建一个立方体 vtkPolyhedron 的 UnstructuredGrid"""
    points = vtkPoints()
    for p in [
        (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),  # bottom
        (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)   # top
    ]:
        points.InsertNextPoint(p)

    faces = vtkIdList()
    face_definitions = [
        [4, 0, 1, 2, 3],
        [4, 4, 5, 6, 7],
        [4, 0, 4, 5, 1],
        [4, 1, 5, 6, 2],
        [4, 2, 6, 7, 3],
        [4, 3, 7, 4, 0]
    ]
    faces.InsertNextId(len(face_definitions))
    for face in face_definitions:
        for fid in face:
            faces.InsertNextId(fid)

    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    grid.InsertNextCell(VTK_POLYHEDRON, faces)
    return grid


def main():
    # 创建立方体 Polyhedron grid
    poly_grid = create_cube_polyhedron_unstructuredgrid()

    # 创建穿过立方体的线
    p0 = [-1, 1.5, 0.5]
    p1 = [2, 1.5, 0.5]
    p0 = [-1, -1, -1]
    p1 = [0, 0, 0]
    line_grid = create_line_unstructuredgrid(p0, p1)

    # 调用测试函数
    intersection_line_with_polyhedron(poly_grid, line_grid)


if __name__ == "__main__":
    main()
