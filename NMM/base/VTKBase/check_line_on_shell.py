from vtkmodules.vtkCommonDataModel import vtkLine, vtkCellLocator, vtkPolyData
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLPolyDataReader
from vtkmodules.vtkCommonCore import vtkMath, reference
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance
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


def classify_point_vs_closed_surface(point, surface, tol=1e-6):
    """
    判断点相对封闭外壳的位置：在壳上 / 壳内 / 壳外
    返回: "on_surface" | "inside" | "outside"

    tol: 距离容差（注意是“距离”，不是平方距离）
    适用于封闭、法向一致的 vtkPolyData 外壳（或可转为 polydata 的 surface）
    """

    # 1) 确保输入是 vtkPolyData（很多隐式距离/包含测试都要求 polydata）
    if not isinstance(surface, vtkPolyData):
        gf = vtkGeometryFilter()
        gf.SetInputData(surface)
        gf.Update()
        poly = gf.GetOutput()
    else:
        poly = surface

    # 2) 先判断是否在表面上：最近点距离 <= tol
    locator = vtkCellLocator()
    locator.SetDataSet(poly)
    locator.BuildLocator()

    closest_point = [0.0, 0.0, 0.0]
    cell_id = reference(0)
    sub_id = reference(0)
    dist2 = reference(0.0)

    locator.FindClosestPoint(point, closest_point, cell_id, sub_id, dist2)
    # dist2 是平方距离
    dist2_val = vtkMath.Distance2BetweenPoints(point, closest_point)
    if dist2_val <= tol * tol:
        return "on_surface"

    # 3) 不在表面上：用有符号距离判断内外
    #    注意：这个结果依赖 poly 的封闭性、法向一致性
    ipd = vtkImplicitPolyDataDistance()
    ipd.SetInput(poly)
    signed_dist = ipd.FunctionValue(point)  # 近似等于 signed distance（单位同坐标）

    # signed_dist < 0: inside, > 0: outside
    return "inside" if signed_dist < 0 else "outside"


if __name__ == "__main__":
    main()
