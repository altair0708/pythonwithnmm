from vtkmodules.vtkCommonDataModel import vtkLine, vtkCellLocator
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLPolyDataReader
from vtkmodules.vtkCommonCore import vtkMath, reference
from NMM.base.Property.Implement.VtkGrid import VtkGrid


def extract_line_endpoints(unstructured_grid):
    """从 vtkUnstructuredGrid 中提取 vtkLine 的两个端点"""
    if unstructured_grid.GetNumberOfCells() == 0:
        raise ValueError("输入的 UnstructuredGrid 中不包含任何单元。")

    cell = unstructured_grid.GetCell(0)
    if not isinstance(cell, vtkLine):
        raise TypeError(f"UnstructuredGrid 中的单元不是 vtkLine。: {cell.GetCellType()}")

    pids = [cell.GetPointId(i) for i in range(2)]
    points = unstructured_grid.GetPoints()
    return points.GetPoint(pids[0]), points.GetPoint(pids[1])


def is_point_on_surface(point, surface, tolerance=1e-10):
    """判断一个点是否在 surface 上（容差内）"""
    locator = vtkCellLocator()
    locator.SetDataSet(surface)
    locator.BuildLocator()

    closest_point = [0.0, 0.0, 0.0]
    cell_id = reference(0)
    sub_id = reference(0)
    dist2 = reference(0.0)

    locator.FindClosestPoint(point, closest_point, cell_id, sub_id, dist2)

    dist2 = vtkMath.Distance2BetweenPoints(point, closest_point)
    return dist2 <= tolerance


def check_line_on_shell(surface_polydata, line_grid, tolerance=1e-10):
    """判断 vtkLine 的两个端点是否都在 surface_polydata 上"""
    p0, p1 = extract_line_endpoints(line_grid)
    on0 = is_point_on_surface(p0, surface_polydata, tolerance)
    on1 = is_point_on_surface(p1, surface_polydata, tolerance)
    return on0 and on1


def main():
    lines = VtkGrid('crack_tip', 'crack_tip.vtu')

    # ===== 读取 surface polydata =====
    shell_reader = vtkXMLPolyDataReader()
    shell_reader.SetFileName("geometric_shell.vtp")
    shell_reader.Update()
    shell = shell_reader.GetOutput()

    # ===== 判断是否在表面上 =====
    tolerance = 1e-4
    for each_line in lines:
        result = check_line_on_shell(shell, each_line, tolerance)
        print("线段的两个端点是否都在表面上？", "是" if result else "否")


if __name__ == "__main__":
    main()
