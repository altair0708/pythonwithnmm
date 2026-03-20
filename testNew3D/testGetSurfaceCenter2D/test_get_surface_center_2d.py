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
from NMM.base.VTKBase.get_surface_center import get_surface_center_2d, check_coplanar


def create_test_triangle():
    """创建测试用的三角形单元"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 三角形顶点 (0,0,0), (2,0,0), (1,2,0) - 几何中心 = (1, 2/3, 0)
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(1, 2, 0)
    
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
    
    # 四边形顶点 (0,0,0), (2,0,0), (2,2,0), (0,2,0) - 几何中心 = (1, 1, 0)
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(2, 2, 0)
    points.InsertNextPoint(0, 2, 0)
    
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
    
    # 五边形顶点 - 几何中心约 = (1, 0.8, 0)
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
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(2, 2, 0)
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


def test_triangle_center_calculation():
    """测试三角形单元几何中心计算"""
    grid = create_test_triangle()
    
    # 测试单元0（三角形）
    center = get_surface_center_2d(grid, 0)
    expected_center = (1.0, 2/3, 0.0)  # (0+2+1)/3, (0+0+2)/3, (0+0+0)/3
    
    assert abs(center[0] - expected_center[0]) < 1e-10, f"三角形中心X坐标错误: 期望 {expected_center[0]}, 实际 {center[0]}"
    assert abs(center[1] - expected_center[1]) < 1e-10, f"三角形中心Y坐标错误: 期望 {expected_center[1]}, 实际 {center[1]}"
    assert abs(center[2] - expected_center[2]) < 1e-10, f"三角形中心Z坐标错误: 期望 {expected_center[2]}, 实际 {center[2]}"


def test_quad_center_calculation():
    """测试四边形单元几何中心计算"""
    grid = create_test_quad()
    
    # 测试单元0（四边形）
    center = get_surface_center_2d(grid, 0)
    expected_center = (1.0, 1.0, 0.0)  # (0+2+2+0)/4, (0+0+2+2)/4, (0+0+0+0)/4
    
    assert abs(center[0] - expected_center[0]) < 1e-10, f"四边形中心X坐标错误: 期望 {expected_center[0]}, 实际 {center[0]}"
    assert abs(center[1] - expected_center[1]) < 1e-10, f"四边形中心Y坐标错误: 期望 {expected_center[1]}, 实际 {center[1]}"
    assert abs(center[2] - expected_center[2]) < 1e-10, f"四边形中心Z坐标错误: 期望 {expected_center[2]}, 实际 {center[2]}"


def test_polygon_center_calculation():
    """测试多边形单元几何中心计算"""
    grid = create_test_polygon()
    
    # 测试单元0（五边形）
    center = get_surface_center_2d(grid, 0)
    expected_center = (1.1, 0.8, 0.0)  # (0+2+2.5+1+0)/5, (0+0+1+2+1)/5, (0+0+0+0+0)/5
    
    assert abs(center[0] - expected_center[0]) < 1e-10, f"多边形中心X坐标错误: 期望 {expected_center[0]}, 实际 {center[0]}"
    assert abs(center[1] - expected_center[1]) < 1e-10, f"多边形中心Y坐标错误: 期望 {expected_center[1]}, 实际 {center[1]}"
    assert abs(center[2] - expected_center[2]) < 1e-10, f"多边形中心Z坐标错误: 期望 {expected_center[2]}, 实际 {center[2]}"


def test_invalid_element_id():
    """测试无效单元ID"""
    grid = create_test_triangle()
    
    # 测试超出范围的ID
    with pytest.raises(ValueError, match="Invalid element_id"):
        get_surface_center_2d(grid, 1)  # 网格只有1个单元
    
    # 测试负数ID
    with pytest.raises(ValueError, match="Invalid element_id"):
        get_surface_center_2d(grid, -1)


def test_3d_cell_rejection():
    """测试3D单元被拒绝"""
    grid = create_3d_cell_grid()
    
    # 3D单元（四面体）应该被拒绝
    with pytest.raises(ValueError, match="not a 2D cell"):
        get_surface_center_2d(grid, 0)


def test_non_coplanar_points_detection():
    """测试非共面点检测"""
    grid = create_non_coplanar_grid()
    
    # 非共面点应该被检测到并抛出异常
    with pytest.raises(ValueError, match="not coplanar"):
        get_surface_center_2d(grid, 0)


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
        (2, 0, 0),    # 1 - 三角形
        (1, 2, 0),    # 2 - 三角形
        (3, 0, 0),    # 3 - 四边形
        (5, 0, 0),    # 4 - 四边形
        (5, 2, 0),    # 5 - 四边形
        (3, 2, 0),    # 6 - 四边形
        (6, 0, 0),    # 7 - 多边形
        (8, 0, 0),    # 8 - 多边形
        (8, 2, 0),    # 9 - 多边形
        (7, 3, 0),    # 10 - 多边形
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
    
    # 测试每个单元的几何中心
    # 三角形中心 = (1, 2/3, 0)
    triangle_center = get_surface_center_2d(grid, 0)
    expected_triangle = (1.0, 2/3, 0.0)
    assert abs(triangle_center[0] - expected_triangle[0]) < 1e-10, f"三角形中心X错误: {triangle_center[0]}"
    assert abs(triangle_center[1] - expected_triangle[1]) < 1e-10, f"三角形中心Y错误: {triangle_center[1]}"
    assert abs(triangle_center[2] - expected_triangle[2]) < 1e-10, f"三角形中心Z错误: {triangle_center[2]}"
    
    # 四边形中心 = (4, 1, 0)
    quad_center = get_surface_center_2d(grid, 1)
    expected_quad = (4.0, 1.0, 0.0)
    assert abs(quad_center[0] - expected_quad[0]) < 1e-10, f"四边形中心X错误: {quad_center[0]}"
    assert abs(quad_center[1] - expected_quad[1]) < 1e-10, f"四边形中心Y错误: {quad_center[1]}"
    assert abs(quad_center[2] - expected_quad[2]) < 1e-10, f"四边形中心Z错误: {quad_center[2]}"
    
    # 多边形中心 = (7.25, 1.25, 0)
    polygon_center = get_surface_center_2d(grid, 2)
    expected_polygon = (7.25, 1.25, 0.0)
    assert abs(polygon_center[0] - expected_polygon[0]) < 1e-10, f"多边形中心X错误: {polygon_center[0]}"
    assert abs(polygon_center[1] - expected_polygon[1]) < 1e-10, f"多边形中心Y错误: {polygon_center[1]}"
    assert abs(polygon_center[2] - expected_polygon[2]) < 1e-10, f"多边形中心Z错误: {polygon_center[2]}"


def test_edge_cases():
    """测试边界情况"""
    # 测试单点单元（虽然不会构成有效2D单元）
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    points.InsertNextPoint(1, 2, 3)
    grid.SetPoints(points)
    
    # 创建一个只有一个点的"单元"
    from vtkmodules.vtkCommonDataModel import vtkVertex
    single_point_ids = vtkIdList()
    single_point_ids.InsertNextId(0)
    grid.InsertNextCell(vtkVertex().GetCellType(), single_point_ids)
    
    # 这种情况下应该会因为不是2D单元而失败
    with pytest.raises(ValueError, match="not a 2D cell"):
        get_surface_center_2d(grid, 0)
    
    # 测试两点单元（线段，不是2D单元）
    grid2 = vtkUnstructuredGrid()
    points2 = vtkPoints()
    points2.InsertNextPoint(0, 0, 0)
    points2.InsertNextPoint(1, 0, 0)
    grid2.SetPoints(points2)
    
    from vtkmodules.vtkCommonDataModel import vtkLine
    line_ids = vtkIdList()
    line_ids.InsertNextId(0)
    line_ids.InsertNextId(1)
    grid2.InsertNextCell(vtkLine().GetCellType(), line_ids)
    
    with pytest.raises(ValueError, match="not a 2D cell"):
        get_surface_center_2d(grid2, 0)


def test_3d_coordinates():
    """测试3D空间中的2D单元"""
    grid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # 在3D空间中的平面四边形 (z=1平面)
    points.InsertNextPoint(0, 0, 1)
    points.InsertNextPoint(2, 0, 1)
    points.InsertNextPoint(2, 2, 1)
    points.InsertNextPoint(0, 2, 1)
    
    grid.SetPoints(points)
    
    quad_ids = vtkIdList()
    quad_ids.InsertNextId(0)
    quad_ids.InsertNextId(1)
    quad_ids.InsertNextId(2)
    quad_ids.InsertNextId(3)
    grid.InsertNextCell(VTK_QUAD, quad_ids)
    
    # 几何中心应该是 (1, 1, 1)
    center = get_surface_center_2d(grid, 0)
    expected_center = (1.0, 1.0, 1.0)
    
    assert abs(center[0] - expected_center[0]) < 1e-10, f"3D平面中心X错误: {center[0]}"
    assert abs(center[1] - expected_center[1]) < 1e-10, f"3D平面中心Y错误: {center[1]}"
    assert abs(center[2] - expected_center[2]) < 1e-10, f"3D平面中心Z错误: {center[2]}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])