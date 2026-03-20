from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints


def modify_point_coordinate(vtk_grid: vtkUnstructuredGrid, point_id: int, new_coordinate: tuple):
    """
    修改unstructuredgrid中指定点的坐标，不改变其他属性
    
    参数:
        vtk_grid: vtkUnstructuredGrid对象
        point_id: 要修改的点的ID
        new_coordinate: 新的坐标元组 (x, y, z)
    
    返回:
        bool: 是否成功修改
    
    异常:
        IndexError: 当point_id超出范围时
        ValueError: 当new_coordinate不是长度为3的元组时
    """
    # 验证输入参数
    if not isinstance(vtk_grid, vtkUnstructuredGrid):
        raise TypeError("vtk_grid必须是vtkUnstructuredGrid类型")
    
    if not isinstance(point_id, int) or point_id < 0:
        raise ValueError("point_id必须是非负整数")
    
    if not isinstance(new_coordinate, (tuple, list)) or len(new_coordinate) != 3:
        raise ValueError("new_coordinate必须是长度为3的元组或列表")
    
    # 检查点ID是否有效
    num_points = vtk_grid.GetNumberOfPoints()
    if point_id >= num_points:
        raise IndexError(f"point_id {point_id} 超出范围，网格只有 {num_points} 个点")
    
    # 获取点集
    points = vtk_grid.GetPoints()
    if points is None:
        raise RuntimeError("vtkUnstructuredGrid没有点数据")
    
    # 设置新坐标
    points.SetPoint(point_id, new_coordinate[0], new_coordinate[1], new_coordinate[2])
    
    # 标记数据已修改
    vtk_grid.Modified()
    points.Modified()
    
    return True


def batch_modify_point_coordinates(vtk_grid: vtkUnstructuredGrid, point_id_coord_pairs: list):
    """
    批量修改多个点的坐标
    
    参数:
        vtk_grid: vtkUnstructuredGrid对象
        point_id_coord_pairs: 点ID和坐标对的列表 [(point_id, (x, y, z)), ...]
    
    返回:
        int: 成功修改的点数量
    """
    if not isinstance(vtk_grid, vtkUnstructuredGrid):
        raise TypeError("vtk_grid必须是vtkUnstructuredGrid类型")
    
    if not isinstance(point_id_coord_pairs, list):
        raise TypeError("point_id_coord_pairs必须是列表")
    
    success_count = 0
    points = vtk_grid.GetPoints()
    num_points = vtk_grid.GetNumberOfPoints()
    
    if points is None:
        raise RuntimeError("vtkUnstructuredGrid没有点数据")
    
    for point_id, new_coordinate in point_id_coord_pairs:
        # 验证参数
        if not isinstance(point_id, int) or point_id < 0 or point_id >= num_points:
            continue
            
        if not isinstance(new_coordinate, (tuple, list)) or len(new_coordinate) != 3:
            continue
        
        # 设置坐标
        points.SetPoint(point_id, new_coordinate[0], new_coordinate[1], new_coordinate[2])
        success_count += 1
    
    # 标记数据已修改
    if success_count > 0:
        vtk_grid.Modified()
        points.Modified()
    
    return success_count


# 示例用法和测试函数
def test_modify_point_coordinate():
    """测试函数"""
    from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex
    from vtkmodules.vtkCommonCore import vtkPoints
    
    # 创建测试网格
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # 添加顶点单元
    for i in range(3):
        vertex = vtkVertex()
        vertex.GetPointIds().SetId(0, i)
        grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
    
    print("原始点坐标:")
    for i in range(grid.GetNumberOfPoints()):
        coord = grid.GetPoint(i)
        print(f"  点{i}: ({coord[0]}, {coord[1]}, {coord[2]})")
    
    # 修改点坐标
    modify_point_coordinate(grid, 1, (2.0, 3.0, 4.0))
    
    print("\n修改后点坐标:")
    for i in range(grid.GetNumberOfPoints()):
        coord = grid.GetPoint(i)
        print(f"  点{i}: ({coord[0]}, {coord[1]}, {coord[2]})")
    
    # 批量修改
    batch_pairs = [(0, (10.0, 10.0, 10.0)), (2, (20.0, 20.0, 20.0))]
    modified_count = batch_modify_point_coordinates(grid, batch_pairs)
    print(f"\n批量修改了 {modified_count} 个点")
    
    print("\n最终点坐标:")
    for i in range(grid.GetNumberOfPoints()):
        coord = grid.GetPoint(i)
        print(f"  点{i}: ({coord[0]}, {coord[1]}, {coord[2]})")


if __name__ == "__main__":
    test_modify_point_coordinate()