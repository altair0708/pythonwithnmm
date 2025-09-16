import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkLine, vtkUnstructuredGrid, vtkGenericCell


def to_np(v):
    return np.array(v)


def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


def find_common_point_between_lines(grid):
    """
    查找两个 vtkLine 单元是否有一个公共点，返回公共点 ID。
    """
    cell1 = vtkGenericCell()
    cell1.SetCellType(grid.GetCellType(0))
    cell1.DeepCopy(grid.GetCell(0))
    cell2 = vtkGenericCell()
    cell2.SetCellType(grid.GetCellType(1))
    cell2.DeepCopy(grid.GetCell(1))

    pts1 = set(cell1.GetPointIds().GetId(i) for i in range(cell1.GetNumberOfPoints()))
    pts2 = set(cell2.GetPointIds().GetId(i) for i in range(cell2.GetNumberOfPoints()))

    common = pts1.intersection(pts2)
    if len(common) == 1:
        return common.pop()
    elif len(common) > 1:
        raise ValueError("两个 line 有多个公共点，可能是重复线。")
    else:
        return None


def get_other_point(cell, common_pid):
    """
    给定一个 vtkLine 单元和一个点 ID，返回另一个点 ID。
    """
    id0 = cell.GetPointId(0)
    id1 = cell.GetPointId(1)
    return id1 if id0 == common_pid else id0


def half_angle(grid):
    """
    给定两个 vtkLine 单元 ID，计算角平分面的相关信息。
    返回：origin, bisector_vector, normal_vector
    """
    assert grid.GetNumberOfCells() == 2

    common_pid = find_common_point_between_lines(grid)
    if common_pid is None:
        raise ValueError("两个 vtkLine 不共享公共点，无法计算角平分面。")

    cell1 = vtkGenericCell()
    cell1.SetCellType(grid.GetCellType(0))
    cell1.DeepCopy(grid.GetCell(0))
    cell2 = vtkGenericCell()
    cell2.SetCellType(grid.GetCellType(1))
    cell2.DeepCopy(grid.GetCell(1))

    p_common = to_np(grid.GetPoint(common_pid))
    p1 = to_np(grid.GetPoint(get_other_point(cell1, common_pid)))
    p2 = to_np(grid.GetPoint(get_other_point(cell2, common_pid)))

    v1 = normalize(p1 - p_common)
    v2 = normalize(p2 - p_common)

    bisector = normalize(v1 + v2)
    normal = np.cross(v1, v2)

    if np.linalg.norm(normal) == 0:
        raise ValueError("两条线共线，无法定义唯一的角平分面。")

    return p_common, bisector, normal

def create_test_grid():
    """
    构造包含两个首尾相连的 vtkLine 的 vtkUnstructuredGrid。
    """
    points = vtkPoints()
    pts = [
        (0, 0, 0),  # 0
        (1, 0, 0),  # 1 (公共点)
        (1, 1, 0),  # 2
    ]
    for p in pts:
        points.InsertNextPoint(p)

    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)

    def add_line(p1, p2):
        line = vtkLine()
        line.GetPointIds().SetId(0, p1)
        line.GetPointIds().SetId(1, p2)
        grid.InsertNextCell(line.GetCellType(), line.GetPointIds())

    add_line(0, 1)  # line 0
    add_line(1, 2)  # line 1

    cell1 = vtkGenericCell()
    cell1.SetCellType(grid.GetCellType(0))
    cell1.DeepCopy(grid.GetCell(0))
    cell2 = grid.GetCell(1)

    return grid

# ===================== 主程序 =====================
if __name__ == "__main__":
    grid = create_test_grid()

    try:
        origin, bisector, normal = half_angle(grid)

        print("✅ 成功计算角平分面！")
        print(f"公共点坐标 (origin): {origin}")
        print(f"角平分向量 (bisector): {bisector}")
        print(f"角所在平面法向量 (normal): {normal}")
    except Exception as e:
        print("❌ 错误:", e)
