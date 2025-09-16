from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


def create_test_unstructured_grid():
    """
    构造一个包含 5 个点和 3 个四面体单元的简单 vtkUnstructuredGrid。
    """
    points = vtkPoints()
    # 添加5个点
    point_coords = [
        (0, 0, 0),  # 0
        (1, 0, 0),  # 1
        (0, 1, 0),  # 2
        (0, 0, 1),  # 3
        (1, 1, 1),  # 4
    ]
    for p in point_coords:
        points.InsertNextPoint(p)

    # 定义3个四面体单元（tetrahedron）
    # 每个单元用4个点
    cells = vtkUnstructuredGrid()
    cells.SetPoints(points)

    def add_tetra(p0, p1, p2, p3):
        tetra = vtkTetra()
        tetra.GetPointIds().SetId(0, p0)
        tetra.GetPointIds().SetId(1, p1)
        tetra.GetPointIds().SetId(2, p2)
        tetra.GetPointIds().SetId(3, p3)
        cells.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())

    add_tetra(0, 1, 2, 3)
    add_tetra(1, 2, 3, 4)
    add_tetra(0, 2, 3, 4)

    return cells


def get_point_cell(unstructured_grid, point_id):
    """
    提取包含给定点ID的所有cell，并构建一个新的vtkUnstructuredGrid返回。
    """
    cell_ids = vtkIdList()
    unstructured_grid.GetPointCells(point_id, cell_ids)

    new_grid = vtkUnstructuredGrid()
    points = vtkPoints()
    point_map = {}

    for i in range(cell_ids.GetNumberOfIds()):
        cell_id = cell_ids.GetId(i)
        cell = unstructured_grid.GetCell(cell_id)
        point_ids = cell.GetPointIds()

        new_cell_point_ids = vtkIdList()
        for j in range(point_ids.GetNumberOfIds()):
            pid = point_ids.GetId(j)
            if pid not in point_map:
                coord = unstructured_grid.GetPoint(pid)
                new_pid = points.InsertNextPoint(coord)
                point_map[pid] = new_pid
            new_cell_point_ids.InsertNextId(point_map[pid])

        new_grid.InsertNextCell(cell.GetCellType(), new_cell_point_ids)

    new_grid.SetPoints(points)
    return new_grid


if __name__ == "__main__":
    # 构造测试用vtkUnstructuredGrid
    test_grid = create_test_unstructured_grid()

    # 指定要查询的点ID（例如：点0）
    point_id = 0
    extracted_grid = get_point_cell(test_grid, point_id)

    # 写入结果文件
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName("extracted_cells.vtu")
    writer.SetInputData(extracted_grid)
    writer.Write()

    print(f"原始网格单元数: {test_grid.GetNumberOfCells()}")
    print(f"提取后网格单元数（包含点ID {point_id}）: {extracted_grid.GetNumberOfCells()}")
    print("结果保存为 extracted_cells.vtu，可用 ParaView 打开查看。")
