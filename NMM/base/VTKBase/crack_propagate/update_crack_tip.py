from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkLine, vtkCellArray


def update_crack_tip(input_grid: vtkUnstructuredGrid, displacement_vectors: list) -> vtkUnstructuredGrid:
    """
    位移输入的 vtkUnstructuredGrid 中所有多边形轮廓点，生成新的多边形轮廓。

    :param input_grid: 包含多条 vtkLine 的 vtkUnstructuredGrid，构成若干多边形轮廓
    :param displacement_vectors: 与所有顶点对应的位移向量列表，形式为 [[dx, dy, dz], ...]
    :return: 新的 vtkUnstructuredGrid，包含位移后的轮廓
    """

    # 原始点
    input_points = input_grid.GetPoints()
    num_points = input_points.GetNumberOfPoints()

    if len(displacement_vectors) != num_points:
        raise ValueError("位移向量数量与输入点数量不一致。")

    # 创建新的点集
    new_points = vtkPoints()
    for i in range(num_points):
        x, y, z = input_points.GetPoint(i)
        dx, dy, dz = displacement_vectors[i]
        new_points.InsertNextPoint(x + dx, y + dy, z + dz)

    # 新建UnstructuredGrid并复制cells结构
    output_grid = vtkUnstructuredGrid()
    output_grid.SetPoints(new_points)

    # 将原有的 cell（vtkLine）结构复制到新的 grid 中
    for i in range(input_grid.GetNumberOfCells()):
        cell = input_grid.GetCell(i)
        if isinstance(cell, vtkLine):
            pt_ids = cell.GetPointIds()
            line = vtkLine()
            line.GetPointIds().SetId(0, pt_ids.GetId(0))
            line.GetPointIds().SetId(1, pt_ids.GetId(1))
            output_grid.InsertNextCell(line.GetCellType(), line.GetPointIds())

    # 4. 复制 PointData
    output_point_data = output_grid.GetPointData()
    input_point_data = input_grid.GetPointData()
    output_point_data.DeepCopy(input_point_data)

    # 5. 复制 CellData
    output_cell_data = output_grid.GetCellData()
    input_cell_data = input_grid.GetCellData()
    output_cell_data.DeepCopy(input_cell_data)

    return output_grid

