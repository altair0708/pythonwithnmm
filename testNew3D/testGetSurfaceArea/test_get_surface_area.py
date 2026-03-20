import pytest
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid, 
    vtkTriangle, 
    vtkQuad, 
    vtkPolygon,
    vtkTetra,
    VTK_TRIANGLE, 
    VTK_QUAD, 
    VTK_POLYGON,
    VTK_TETRA
)
from NMM.base.VTKBase.get_surface_area import get_surface_area, check_coplanar


def create_test_triangle():
    """创建测试用的三角形单元"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 三角形顶点 (0,0,0), (1,0,0), (0,1,0) - 面积 = 0.5
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    
    grid.SetPoints(points)
    
    # 创建三角形单元
    triangle_ids = vtkIdList()
    triangle_ids.InsertNextId(0)
    triangle_ids.InsertNextId(1)
    triangle_ids.InsertNextId(2)
    grid.InsertNextCell(VTK_TRIANGLE, triangle_ids)
    
    return grid


def create_test_quad():
    """创建测试用的四边形单元"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 四边形顶点 (0,0,0), (2,0,0), (2,1,0), (0,1,0) - 面积 = 2.0
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(2, 1, 0)
    points.InsertNextPoint(0, 1, 0)
    
    grid.SetPoints(points)
    
    # 创建四边形单元
    quad_ids = vtkIdList()
    quad_ids.InsertNextId(0)
    quad_ids.InsertNextId(1)
    quad_ids.InsertNextId(2)
    quad_ids.InsertNextId(3)
    grid.InsertNextCell(VTK_QUAD, quad_ids)
    
    return grid


def create_test_polygon():
    """创建测试用的多边形单元"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 五边形顶点 - 面积 = 2.0
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(2.5, 1, 0)
    points.InsertNextPoint(1, 2, 0)
    points.InsertNextPoint(0, 1, 0)
    
    grid.SetPoints(points)
    
    # 创建多边形单元
    polygon_ids = vtkIdList()
    polygon_ids.InsertNextId(0)
    polygon_ids.InsertNextId(1)
    polygon_ids.InsertNextId(2)
    polygon_ids.InsertNextId(3)
    polygon_ids.InsertNextId(4)
    grid.InsertNextCell(VTK_POLYGON, polygon_ids)
    
    return grid


def create_3d_cell_grid():
    """创建包含3D单元的网格（用于测试拒绝情况）"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 四面体顶点
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(0, 0, 1)
    
    grid.SetPoints(points)
    
    # 创建四面体单元
    tetra = vtkTetra()
    for i in range(4):
        tetra.GetPointIds().SetId(i, i)
    grid.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
    
    return grid


def create_non_coplanar_grid():
    """创建包含非共面点的网格"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 四边形点，其中一个点稍微偏离平面
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(0, 0, 0.01)  # 稍微偏离XY平面
    
    grid.SetPoints(points)
    
    # 创建四边形单元
    quad_ids = vtkIdList()
    quad_ids.InsertNextId(0)
    quad_ids.InsertNextId(1)
    quad_ids.InsertNextId(2)
    quad_ids.InsertNextId(3)
    grid.InsertNextCell(VTK_QUAD, quad_ids)
    
    return grid


def test_triangle_area_calculation():
    """测试三角形单元面积计算"""
    grid = create_test_triangle()
    
    # 测试单元0（三角形）
    area = get_surface_area(grid, 0)
    expected_area = 0.5  # 底×高÷2 = 1×1÷2 = 0.5
    
    assert abs(area - expected_area) < 1e-10, f"三角形面积计算错误: 期望 {expected_area}, 实际 {area}"


def test_quad_area_calculation():
    """测试四边形单元面积计算"""
    grid = create_test_quad()
    
    # 测试单元0（四边形）
    area = get_surface_area(grid, 0)
    expected_area = 2.0  # 长×宽 = 2×1 = 2.0
    
    assert abs(area - expected_area) < 1e-10, f"四边形面积计算错误: 期望 {expected_area}, 实际 {area}"


def test_polygon_area_calculation():
    """测试多边形单元面积计算"""
    grid = create_test_polygon()
    
    # 测试单元0（五边形）
    area = get_surface_area(grid, 0)
    
    # 验证面积为正数
    assert area > 0, f"多边形面积应为正数，实际得到 {area}"
    
    # 验证面积合理性（应该大于三角形面积0.5，小于包围矩形面积4.0）
    assert 0.5 < area < 4.0, f"多边形面积不合理: {area}"


def test_invalid_element_id():
    """测试无效单元ID"""
    grid = create_test_triangle()
    
    # 测试超出范围的ID
    with pytest.raises(ValueError, match="Invalid element_id"):
        get_surface_area(grid, 1)  # 网格只有1个单元
    
    # 测试负数ID
    with pytest.raises(ValueError, match="Invalid element_id"):
        get_surface_area(grid, -1)


def test_3d_cell_rejection():
    """测试3D单元被拒绝"""
    grid = create_3d_cell_grid()
    
    # 3D单元（四面体）应该被拒绝
    with pytest.raises(ValueError, match="not a 2D cell"):
        get_surface_area(grid, 0)


def test_non_coplanar_points_detection():
    """测试非共面点检测"""
    grid = create_non_coplanar_grid()
    
    # 非共面点应该被检测到并抛出异常
    with pytest.raises(ValueError, match="not coplanar"):
        get_surface_area(grid, 0)


def test_check_coplanar_function():
    """测试共面性检查函数"""
    # 测试共面点
    coplanar_points = vtkPoints()
    coplanar_points.InsertNextPoint(0, 0, 0)
    coplanar_points.InsertNextPoint(1, 0, 0)
    coplanar_points.InsertNextPoint(0, 1, 0)
    coplanar_points.InsertNextPoint(1, 1, 0)
    
    assert check_coplanar(coplanar_points) == True, "共面点应该返回True"
    
    # 测试非共面点
    non_coplanar_points = vtkPoints()
    non_coplanar_points.InsertNextPoint(0, 0, 0)
    non_coplanar_points.InsertNextPoint(1, 0, 0)
    non_coplanar_points.InsertNextPoint(0, 1, 0)
    non_coplanar_points.InsertNextPoint(0, 0, 0.1)
    
    assert check_coplanar(non_coplanar_points, tolerance=1e-3) == False, "非共面点应该返回False"
    
    # 测试三点总是共面
    three_points = vtkPoints()
    three_points.InsertNextPoint(0, 0, 0)
    three_points.InsertNextPoint(1, 0, 0)
    three_points.InsertNextPoint(0, 1, 0)
    
    assert check_coplanar(three_points) == True, "三点应该总是共面"


def test_multiple_valid_cells():
    """测试包含多个有效2D单元的网格"""
    # 创建包含多种2D单元的网格
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 添加所有点
    point_coords = [
        (0, 0, 0),    # 0 - 三角形
        (1, 0, 0),    # 1 - 三角形
        (0, 1, 0),    # 2 - 三角形
        (2, 0, 0),    # 3 - 四边形
        (3, 0, 0),    # 4 - 四边形
        (3, 1, 0),    # 5 - 四边形
        (2, 1, 0),    # 6 - 四边形
        (4, 0, 0),    # 7 - 多边形
        (5, 0, 0),    # 8 - 多边形
        (5, 1, 0),    # 9 - 多边形
        (4, 1, 0),    # 10 - 多边形
    ]
    
    for coord in point_coords:
        points.InsertNextPoint(coord)
    
    grid.SetPoints(points)
    
    # 添加三角形单元 (点 0,1,2)
    triangle_ids = vtkIdList()
    triangle_ids.InsertNextId(0)
    triangle_ids.InsertNextId(1)
    triangle_ids.InsertNextId(2)
    grid.InsertNextCell(VTK_TRIANGLE, triangle_ids)
    
    # 添加四边形单元 (点 3,4,5,6)
    quad_ids = vtkIdList()
    quad_ids.InsertNextId(3)
    quad_ids.InsertNextId(4)
    quad_ids.InsertNextId(5)
    quad_ids.InsertNextId(6)
    grid.InsertNextCell(VTK_QUAD, quad_ids)
    
    # 添加多边形单元 (点 7,8,9,10)
    polygon_ids = vtkIdList()
    polygon_ids.InsertNextId(7)
    polygon_ids.InsertNextId(8)
    polygon_ids.InsertNextId(9)
    polygon_ids.InsertNextId(10)
    grid.InsertNextCell(VTK_POLYGON, polygon_ids)
    
    # 测试每个单元
    # 三角形面积 = 0.5
    triangle_area = get_surface_area(grid, 0)
    assert abs(triangle_area - 0.5) < 1e-10, f"三角形面积错误: {triangle_area}"
    
    # 四边形面积 = 1.0
    quad_area = get_surface_area(grid, 1)
    assert abs(quad_area - 1.0) < 1e-10, f"四边形面积错误: {quad_area}"
    
    # 多边形面积 = 1.0
    polygon_area = get_surface_area(grid, 2)
    assert polygon_area > 0, f"多边形面积应为正数: {polygon_area}"


def test_edge_case_single_point():
    """测试边界情况：单点（虽然不会构成有效单元，但测试容错性）"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    grid.SetPoints(points)
    
    # 创建一个只有一个点的"单元"（实际上无效）
    single_point_ids = vtkIdList()
    single_point_ids.InsertNextId(0)
    
    # 这应该会因为点数不足而失败
    from vtkmodules.vtkCommonDataModel import vtkVertex
    grid.InsertNextCell(vtkVertex().GetCellType(), single_point_ids)
    
    # 测试是否会正确处理
    try:
        area = get_surface_area(grid, 0)
        # 如果没有抛异常，面积应该非常小或者为0
        assert area <= 0 or area < 1e-10, f"单点单元面积异常: {area}"
    except ValueError:
        # 这是可以接受的
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])