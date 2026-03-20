import pytest
from vtkmodules.all import vtkUnstructuredGrid, vtkPoints, vtkVertex
from NMM.base.VTKBase.modify_point_coordinate import (
    modify_point_coordinate, 
    batch_modify_point_coordinates
)


def create_test_grid():
    """创建测试用的vtkUnstructuredGrid"""
    points = vtkPoints()
    # 添加测试点
    test_coords = [
        (0.0, 0.0, 0.0),    # 点0
        (1.0, 0.0, 0.0),    # 点1
        (0.0, 1.0, 0.0),    # 点2
        (1.0, 1.0, 0.0),    # 点3
        (0.5, 0.5, 0.5),    # 点4
    ]
    
    for coord in test_coords:
        points.InsertNextPoint(coord)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # 添加顶点单元
    for i in range(len(test_coords)):
        vertex = vtkVertex()
        vertex.GetPointIds().SetId(0, i)
        grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
    
    return grid


def test_single_point_modification():
    """测试单个点坐标修改"""
    grid = create_test_grid()
    
    # 测试修改点1的坐标
    original_coord = grid.GetPoint(1)
    assert original_coord == (1.0, 0.0, 0.0)
    
    # 修改坐标
    success = modify_point_coordinate(grid, 1, (2.0, 3.0, 4.0))
    assert success is True
    
    # 验证修改结果
    new_coord = grid.GetPoint(1)
    assert new_coord == (2.0, 3.0, 4.0)
    
    # 验证其他点未被修改
    assert grid.GetPoint(0) == (0.0, 0.0, 0.0)
    assert grid.GetPoint(2) == (0.0, 1.0, 0.0)


def test_invalid_point_id():
    """测试无效点ID"""
    grid = create_test_grid()
    
    # 测试负数ID
    with pytest.raises(ValueError):
        modify_point_coordinate(grid, -1, (1.0, 1.0, 1.0))
    
    # 测试超出范围的ID
    with pytest.raises(IndexError):
        modify_point_coordinate(grid, 10, (1.0, 1.0, 1.0))
    
    # 测试边界情况
    with pytest.raises(IndexError):
        modify_point_coordinate(grid, 5, (1.0, 1.0, 1.0))  # 刚好超出范围


def test_invalid_coordinates():
    """测试无效坐标"""
    grid = create_test_grid()
    
    # 测试错误的坐标格式
    with pytest.raises(ValueError):
        modify_point_coordinate(grid, 0, (1.0, 2.0))  # 缺少z坐标
    
    with pytest.raises(ValueError):
        modify_point_coordinate(grid, 0, (1.0, 2.0, 3.0, 4.0))  # 多余坐标
    
    with pytest.raises(ValueError):
        modify_point_coordinate(grid, 0, "invalid")  # 非元组类型


def test_invalid_grid():
    """测试无效网格"""
    # 测试非vtkUnstructuredGrid类型
    with pytest.raises(TypeError):
        modify_point_coordinate("not_a_grid", 0, (1.0, 1.0, 1.0))
    
    # 测试None网格
    with pytest.raises(TypeError):
        modify_point_coordinate(None, 0, (1.0, 1.0, 1.0))


def test_batch_modification():
    """测试批量坐标修改"""
    grid = create_test_grid()
    
    # 准备批量修改数据
    modifications = [
        (0, (10.0, 10.0, 10.0)),  # 修改点0
        (2, (20.0, 20.0, 20.0)),  # 修改点2
        (4, (30.0, 30.0, 30.0)),  # 修改点4
    ]
    
    # 执行批量修改
    modified_count = batch_modify_point_coordinates(grid, modifications)
    assert modified_count == 3
    
    # 验证修改结果
    assert grid.GetPoint(0) == (10.0, 10.0, 10.0)
    assert grid.GetPoint(2) == (20.0, 20.0, 20.0)
    assert grid.GetPoint(4) == (30.0, 30.0, 30.0)
    
    # 验证未修改的点
    assert grid.GetPoint(1) == (1.0, 0.0, 0.0)
    assert grid.GetPoint(3) == (1.0, 1.0, 0.0)


def test_batch_with_invalid_data():
    """测试批量修改中的无效数据"""
    grid = create_test_grid()
    
    # 包含无效数据的批量修改
    modifications = [
        (0, (10.0, 10.0, 10.0)),      # 有效
        (-1, (20.0, 20.0, 20.0)),     # 无效ID
        (2, (30.0, 30.0)),            # 无效坐标
        (10, (40.0, 40.0, 40.0)),     # 超出范围ID
        (1, (50.0, 50.0, 50.0)),      # 有效
    ]
    
    modified_count = batch_modify_point_coordinates(grid, modifications)
    assert modified_count == 2  # 只有两个有效修改
    
    # 验证有效的修改已应用
    assert grid.GetPoint(0) == (10.0, 10.0, 10.0)
    assert grid.GetPoint(1) == (50.0, 50.0, 50.0)
    
    # 验证无效的修改被忽略
    assert grid.GetPoint(2) == (0.0, 1.0, 0.0)  # 未被修改


def test_empty_batch():
    """测试空批量修改"""
    grid = create_test_grid()
    
    # 空列表
    modified_count = batch_modify_point_coordinates(grid, [])
    assert modified_count == 0
    
    # 验证网格未被修改
    original_coords = []
    for i in range(grid.GetNumberOfPoints()):
        original_coords.append(grid.GetPoint(i))
    
    # 再次测试空修改
    modified_count = batch_modify_point_coordinates(grid, [])
    assert modified_count == 0
    
    # 验证坐标未变
    for i, coord in enumerate(original_coords):
        assert grid.GetPoint(i) == coord


def test_modified_flag():
    """测试Modified标志设置"""
    grid = create_test_grid()
    
    # 记录修改前的状态
    mtime_before = grid.GetMTime()
    
    # 修改坐标
    modify_point_coordinate(grid, 0, (1.0, 1.0, 1.0))
    
    # 验证Modified标志已设置
    mtime_after = grid.GetMTime()
    assert mtime_after > mtime_before
    
    # 验证点集的Modified标志
    points = grid.GetPoints()
    points_mtime = points.GetMTime()
    assert points_mtime >= mtime_after


def test_preserve_cell_structure():
    """测试修改坐标不改变单元结构"""
    grid = create_test_grid()
    
    # 记录原始单元信息
    original_cell_count = grid.GetNumberOfCells()
    original_cell_types = []
    original_point_ids = []
    
    for i in range(original_cell_count):
        cell = grid.GetCell(i)
        original_cell_types.append(cell.GetCellType())
        original_point_ids.append([cell.GetPointId(j) for j in range(cell.GetNumberOfPoints())])
    
    # 修改点坐标
    modify_point_coordinate(grid, 2, (100.0, 100.0, 100.0))
    
    # 验证单元结构未变
    assert grid.GetNumberOfCells() == original_cell_count
    
    for i in range(original_cell_count):
        cell = grid.GetCell(i)
        assert cell.GetCellType() == original_cell_types[i]
        
        point_ids = [cell.GetPointId(j) for j in range(cell.GetNumberOfPoints())]
        assert point_ids == original_point_ids[i]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])