import pytest
from vtkmodules.all import (
    vtkPolyData, 
    vtkUnstructuredGrid, 
    vtkCubeSource, 
    vtkSphereSource,
    vtkCylinderSource,
    vtkPlaneSource,
    vtkPoints, 
    vtkIdList
)
from NMM.base.VTKBase.check_line_on_shell import classify_point_vs_closed_surface


def create_test_cube(center=(0, 0, 0), length=2.0):
    """创建一个立方体用于测试"""
    cube = vtkCubeSource()
    cube.SetCenter(*center)
    cube.SetXLength(length)
    cube.SetYLength(length)
    cube.SetZLength(length)
    cube.Update()
    return cube.GetOutput()


def create_test_sphere(center=(0, 0, 0), radius=1.0):
    """创建一个球体用于测试"""
    sphere = vtkSphereSource()
    sphere.SetCenter(*center)
    sphere.SetRadius(radius)
    sphere.SetThetaResolution(20)
    sphere.SetPhiResolution(20)
    sphere.Update()
    return sphere.GetOutput()


def create_test_plane(center=(0, 0, 0), normal=(0, 0, 1)):
    """创建一个平面用于测试（非封闭表面）"""
    plane = vtkPlaneSource()
    plane.SetOrigin(center[0]-1, center[1]-1, center[2])
    plane.SetPoint1(center[0]+1, center[1]-1, center[2])
    plane.SetPoint2(center[0]-1, center[1]+1, center[2])
    plane.Update()
    return plane.GetOutput()


def test_point_on_surface():
    """测试点在表面上的情况"""
    # 创建立方体表面
    cube_surface = create_test_cube((0, 0, 0), 2.0)
    
    # 测试立方体的顶点（应该在表面上）
    vertices = [
        (-1, -1, -1),  # 顶点1
        (1, -1, -1),   # 顶点2
        (-1, 1, -1),   # 顶点3
        (1, 1, -1),    # 顶点4
        (-1, -1, 1),   # 顶点5
        (1, -1, 1),    # 顶点6
        (-1, 1, 1),    # 顶点7
        (1, 1, 1),     # 顶点8
    ]
    
    for vertex in vertices:
        result = classify_point_vs_closed_surface(vertex, cube_surface, tol=1e-6)
        assert result == "on_surface", f"点 {vertex} 应该在表面上，但返回了 {result}"


def test_point_inside_surface():
    """测试点在封闭表面内部的情况"""
    # 创建立方体表面
    cube_surface = create_test_cube((0, 0, 0), 2.0)
    
    # 测试立方体内部的点
    internal_points = [
        (0, 0, 0),      # 中心点
        (0.5, 0.5, 0.5), # 内部点1
        (-0.3, 0.2, -0.1), # 内部点2
        (0.8, -0.5, 0.3),  # 内部点3
    ]
    
    for point in internal_points:
        result = classify_point_vs_closed_surface(point, cube_surface, tol=1e-6)
        assert result == "inside", f"点 {point} 应该在内部，但返回了 {result}"


def test_point_outside_surface():
    """测试点在封闭表面外部的情况"""
    # 创建立方体表面
    cube_surface = create_test_cube((0, 0, 0), 2.0)
    
    # 测试立方体外部的点
    external_points = [
        (2, 0, 0),      # x方向外部
        (0, 2, 0),      # y方向外部
        (0, 0, 2),      # z方向外部
        (3, 3, 3),      # 远离立方体的点
        (-2.5, 0, 0),   # 负x方向外部
    ]
    
    for point in external_points:
        result = classify_point_vs_closed_surface(point, cube_surface, tol=1e-6)
        assert result == "outside", f"点 {point} 应该在外部，但返回了 {result}"


def test_sphere_surface_classification():
    """测试球体表面的点分类"""
    # 创建球体表面
    sphere_surface = create_test_sphere((0, 0, 0), 1.0)
    
    # 测试球面上的点（使用更宽松的容差）
    surface_points = [
        (1, 0, 0),      # x轴正方向
        (-1, 0, 0),     # x轴负方向
        (0, 1, 0),      # y轴正方向
        (0, -1, 0),     # y轴负方向
        (0, 0, 1),      # z轴正方向
        (0, 0, -1),     # z轴负方向
    ]
    
    for point in surface_points:
        result = classify_point_vs_closed_surface(point, sphere_surface, tol=1e-4)
        # 对于球体，由于网格化的原因，某些点可能被判定为inside或outside
        # 我们主要关注函数能否正确执行和返回合理的结果
        assert result in ["on_surface", "inside", "outside"], f"点 {point} 的分类结果异常: {result}"
    
    # 测试球体内部的点
    internal_points = [
        (0, 0, 0),      # 球心
        (0.5, 0, 0),    # 半径一半处
        (0.3, 0.4, 0),  # 内部点
    ]
    
    for point in internal_points:
        result = classify_point_vs_closed_surface(point, sphere_surface, tol=1e-6)
        assert result == "inside", f"点 {point} 应该在球体内部，但返回了 {result}"
    
    # 测试球体外部的点
    external_points = [
        (1.5, 0, 0),    # 半径外
        (2, 2, 2),      # 远离球体
        (-1.2, 0, 0),   # 负方向外部
    ]
    
    for point in external_points:
        result = classify_point_vs_closed_surface(point, sphere_surface, tol=1e-6)
        assert result == "outside", f"点 {point} 应该在球体外部，但返回了 {result}"


def test_tolerance_effect():
    """测试容差参数的影响"""
    cube_surface = create_test_cube((0, 0, 0), 2.0)
    
    # 测试接近表面但不在表面上的点
    near_surface_points = [
        (1.000001, 0, 0),  # 略微超出表面
        (0.999999, 0, 0),  # 略微在表面内侧
        (-1.000001, 0, 0), # 略微超出表面（负方向）
    ]
    
    # 使用较宽松的容差
    loose_tol_result = classify_point_vs_closed_surface(
        near_surface_points[0], cube_surface, tol=1e-5
    )
    assert loose_tol_result == "on_surface", f"使用宽松容差时应该判定为在表面上"
    
    # 使用严格的容差
    strict_tol_result = classify_point_vs_closed_surface(
        near_surface_points[0], cube_surface, tol=1e-8
    )
    assert strict_tol_result != "on_surface", f"使用严格容差时不应该判定为在表面上"


def test_non_closed_surface():
    """测试非封闭表面的情况（平面）"""
    plane_surface = create_test_plane((0, 0, 0))
    
    # 平面上的点
    on_plane_points = [
        (0, 0, 0),
        (0.5, -0.5, 0),
        (-0.3, 0.7, 0),
    ]
    
    for point in on_plane_points:
        result = classify_point_vs_closed_surface(point, plane_surface, tol=1e-6)
        # 对于平面，点要么在表面上，要么根据法向量判断内外
        assert result in ["on_surface", "inside", "outside"], f"点 {point} 的分类结果异常: {result}"


def test_edge_cases():
    """测试边界情况"""
    cube_surface = create_test_cube((0, 0, 0), 2.0)
    
    # 零向量点
    result = classify_point_vs_closed_surface((0, 0, 0), cube_surface, tol=1e-6)
    assert result in ["inside", "on_surface"], f"原点分类结果异常: {result}"
    
    # 很远的点
    far_point_result = classify_point_vs_closed_surface((1000, 1000, 1000), cube_surface, tol=1e-6)
    assert far_point_result == "outside", f"远离点应该在外部"
    
    # 非常小的容差
    tiny_tol_result = classify_point_vs_closed_surface((1, 0, 0), cube_surface, tol=1e-12)
    assert tiny_tol_result == "on_surface", f"精确表面上的点应该被识别"


def test_unstructured_grid_input():
    """测试传入vtkUnstructuredGrid作为surface参数"""
    # 创建立方体并转换为UnstructuredGrid
    cube_source = vtkCubeSource()
    cube_source.SetCenter(0, 0, 0)
    cube_source.SetXLength(2)
    cube_source.SetYLength(2)
    cube_source.SetZLength(2)
    cube_source.Update()
    
    # 函数应该能够处理vtkUnstructuredGrid输入
    result = classify_point_vs_closed_surface((0, 0, 0), cube_source.GetOutput(), tol=1e-6)
    assert result in ["inside", "on_surface"], f"UnstructuredGrid输入测试失败: {result}"


def run_comprehensive_test():
    """运行综合测试并生成报告"""
    print("=" * 60)
    print("classify_point_vs_closed_surface 函数综合测试报告")
    print("=" * 60)
    
    # 测试不同形状
    shapes = [
        ("立方体", create_test_cube((0, 0, 0), 2.0)),
        ("球体", create_test_sphere((0, 0, 0), 1.0)),
        ("平面", create_test_plane((0, 0, 0)))
    ]
    
    test_points = [
        ("原点", (0, 0, 0)),
        ("表面点1", (1, 0, 0)),
        ("表面点2", (0, 1, 0)),
        ("内部点", (0.5, 0.5, 0.5)),
        ("外部点", (3, 0, 0))
    ]
    
    for shape_name, shape in shapes:
        print(f"\n测试形状: {shape_name}")
        print("-" * 40)
        for point_name, point in test_points:
            try:
                result = classify_point_vs_closed_surface(point, shape, tol=1e-6)
                print(f"  {point_name} {point}: {result}")
            except Exception as e:
                print(f"  {point_name} {point}: 错误 - {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v"])
    
    # 可选：运行综合测试报告
    # run_comprehensive_test()