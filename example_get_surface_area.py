#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
get_surface_area函数使用示例

这个示例展示了如何使用get_surface_area函数计算2D VTK单元的面积，
包括单元类型验证和共面性检查。
"""

from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid, 
    vtkTriangle, 
    vtkQuad, 
    vtkPolygon,
    VTK_TRIANGLE, 
    VTK_QUAD, 
    VTK_POLYGON
)
from NMM.base.VTKBase.get_surface_area import get_surface_area


def create_sample_grid():
    """创建示例网格数据"""
    grid = vtkUnstructuredGrid()
    
    # 创建点集
    points = vtkPoints()
    
    # 三角形点
    points.InsertNextPoint(0, 0, 0)    # 点0
    points.InsertNextPoint(2, 0, 0)    # 点1
    points.InsertNextPoint(1, 2, 0)    # 点2
    
    # 四边形点
    points.InsertNextPoint(3, 0, 0)    # 点3
    points.InsertNextPoint(5, 0, 0)    # 点4
    points.InsertNextPoint(5, 2, 0)    # 点5
    points.InsertNextPoint(3, 2, 0)    # 点6
    
    # 多边形点
    points.InsertNextPoint(6, 0, 0)    # 点7
    points.InsertNextPoint(8, 0, 0)    # 点8
    points.InsertNextPoint(9, 1, 0)    # 点9
    points.InsertNextPoint(8, 2, 0)    # 点10
    points.InsertNextPoint(6, 2, 0)    # 点11
    
    grid.SetPoints(points)
    
    # 创建三角形单元 (使用点 0,1,2)
    triangle_ids = vtkIdList()
    triangle_ids.InsertNextId(0)
    triangle_ids.InsertNextId(1)
    triangle_ids.InsertNextId(2)
    grid.InsertNextCell(VTK_TRIANGLE, triangle_ids)
    
    # 创建四边形单元 (使用点 3,4,5,6)
    quad_ids = vtkIdList()
    quad_ids.InsertNextId(3)
    quad_ids.InsertNextId(4)
    quad_ids.InsertNextId(5)
    quad_ids.InsertNextId(6)
    grid.InsertNextCell(VTK_QUAD, quad_ids)
    
    # 创建多边形单元 (使用点 7,8,9,10,11)
    polygon_ids = vtkIdList()
    polygon_ids.InsertNextId(7)
    polygon_ids.InsertNextId(8)
    polygon_ids.InsertNextId(9)
    polygon_ids.InsertNextId(10)
    polygon_ids.InsertNextId(11)
    grid.InsertNextCell(VTK_POLYGON, polygon_ids)
    
    return grid


def demonstrate_basic_usage():
    """演示基本用法"""
    print("=== 基本用法演示 ===")
    
    # 创建示例网格
    grid = create_sample_grid()
    
    print(f"网格包含 {grid.GetNumberOfCells()} 个单元")
    print(f"网格包含 {grid.GetNumberOfPoints()} 个点")
    print()
    
    # 计算各个单元的面积
    for i in range(grid.GetNumberOfCells()):
        cell_type = grid.GetCellType(i)
        cell_types = {VTK_TRIANGLE: "三角形", VTK_QUAD: "四边形", VTK_POLYGON: "多边形"}
        cell_name = cell_types.get(cell_type, f"未知类型({cell_type})")
        
        try:
            area = get_surface_area(grid, i)
            print(f"单元 {i} ({cell_name}): 面积 = {area:.6f}")
        except ValueError as e:
            print(f"单元 {i} ({cell_name}): 错误 - {e}")


def demonstrate_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理演示 ===")
    
    # 1. 测试无效单元ID
    print("1. 测试无效单元ID:")
    grid = create_sample_grid()
    try:
        area = get_surface_area(grid, 10)  # 不存在的单元ID
    except ValueError as e:
        print(f"   捕获到预期错误: {e}")
    
    # 2. 测试3D单元 (应该被拒绝)
    print("\n2. 测试3D单元拒绝:")
    from vtkmodules.vtkCommonDataModel import vtkTetra
    
    tetra_grid = vtkUnstructuredGrid()
    tetra_points = vtkPoints()
    # 创建一个四面体(3D单元)
    tetra_points.InsertNextPoint(0, 0, 0)
    tetra_points.InsertNextPoint(1, 0, 0)
    tetra_points.InsertNextPoint(0, 1, 0)
    tetra_points.InsertNextPoint(0, 0, 1)
    tetra_grid.SetPoints(tetra_points)
    
    tetra = vtkTetra()
    for i in range(4):
        tetra.GetPointIds().SetId(i, i)
    tetra_grid.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
    
    try:
        area = get_surface_area(tetra_grid, 0)
    except ValueError as e:
        print(f"   捕获到预期错误: {e}")
    
    # 3. 测试非共面点
    print("\n3. 测试非共面点检测:")
    non_coplanar_grid = vtkUnstructuredGrid()
    points = vtkPoints()
    # 创建一个轻微扭曲的四边形
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(0, 0, 0.01)  # 稍微偏离XY平面
    non_coplanar_grid.SetPoints(points)
    
    quad = vtkQuad()
    for i in range(4):
        quad.GetPointIds().SetId(i, i)
    non_coplanar_grid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())
    
    try:
        area = get_surface_area(non_coplanar_grid, 0)
    except ValueError as e:
        print(f"   捕获到预期错误: {e}")


def main():
    """主函数"""
    print("VTK 2D单元面积计算函数演示")
    print("=" * 50)
    
    demonstrate_basic_usage()
    demonstrate_error_handling()
    
    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    main()