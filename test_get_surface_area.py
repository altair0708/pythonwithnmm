import unittest
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTriangle, vtkQuad, vtkPolygon, VTK_TRIANGLE, VTK_QUAD, VTK_POLYGON
from NMM.base.VTKBase.get_surface_area import get_surface_area, check_coplanar


class TestGetSurfaceArea(unittest.TestCase):
    
    def setUp(self):
        """设置测试数据"""
        # 创建测试用的vtkUnstructuredGrid
        self.grid = vtkUnstructuredGrid()
        
        # 添加三角形单元 (面积 = 0.5)
        triangle_points = vtkPoints()
        triangle_points.InsertNextPoint(0, 0, 0)
        triangle_points.InsertNextPoint(1, 0, 0)
        triangle_points.InsertNextPoint(0, 1, 0)
        
        triangle = vtkTriangle()
        triangle.GetPointIds().SetId(0, 0)
        triangle.GetPointIds().SetId(1, 1)
        triangle.GetPointIds().SetId(2, 2)
        
        # 添加四边形单元 (面积 = 1.0)
        quad_points = vtkPoints()
        quad_points.InsertNextPoint(2, 0, 0)
        quad_points.InsertNextPoint(3, 0, 0)
        quad_points.InsertNextPoint(3, 1, 0)
        quad_points.InsertNextPoint(2, 1, 0)
        
        quad = vtkQuad()
        quad.GetPointIds().SetId(0, 0)
        quad.GetPointIds().SetId(1, 1)
        quad.GetPointIds().SetId(2, 2)
        quad.GetPointIds().SetId(3, 3)
        
        # 添加多边形单元 (面积 = 2.0)
        polygon_points = vtkPoints()
        polygon_points.InsertNextPoint(4, 0, 0)
        polygon_points.InsertNextPoint(6, 0, 0)
        polygon_points.InsertNextPoint(6, 2, 0)
        polygon_points.InsertNextPoint(4, 2, 0)
        
        polygon = vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(4)
        polygon.GetPointIds().SetId(0, 0)
        polygon.GetPointIds().SetId(1, 1)
        polygon.GetPointIds().SetId(2, 2)
        polygon.GetPointIds().SetId(3, 3)
        
        # 组装网格
        all_points = vtkPoints()
        # 添加三角形点
        for i in range(3):
            all_points.InsertNextPoint(triangle_points.GetPoint(i))
        # 添加四边形点
        for i in range(4):
            all_points.InsertNextPoint(quad_points.GetPoint(i))
        # 添加多边形点
        for i in range(4):
            all_points.InsertNextPoint(polygon_points.GetPoint(i))
            
        self.grid.SetPoints(all_points)
        self.grid.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())
        self.grid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())
        self.grid.InsertNextCell(polygon.GetCellType(), polygon.GetPointIds())
    
    def test_triangle_area(self):
        """测试三角形单元面积计算"""
        area = get_surface_area(self.grid, 0)
        self.assertAlmostEqual(area, 0.5, places=6)
    
    def test_quad_area(self):
        """测试四边形单元面积计算"""
        area = get_surface_area(self.grid, 1)
        self.assertAlmostEqual(area, 1.0, places=6)
    
    def test_polygon_area(self):
        """测试多边形单元面积计算"""
        area = get_surface_area(self.grid, 2)
        self.assertAlmostEqual(area, 2.0, places=6)
    
    def test_invalid_element_id(self):
        """测试无效单元ID"""
        with self.assertRaises(ValueError):
            get_surface_area(self.grid, 10)  # 超出范围的ID
            
        with self.assertRaises(ValueError):
            get_surface_area(self.grid, -1)  # 负数ID
    
    def test_3d_cell_rejection(self):
        """测试拒绝3D单元"""
        # 创建包含3D单元的网格
        tetra_grid = vtkUnstructuredGrid()
        tetra_points = vtkPoints()
        tetra_points.InsertNextPoint(0, 0, 0)
        tetra_points.InsertNextPoint(1, 0, 0)
        tetra_points.InsertNextPoint(0, 1, 0)
        tetra_points.InsertNextPoint(0, 0, 1)
        tetra_grid.SetPoints(tetra_points)
        
        from vtkmodules.vtkCommonDataModel import vtkTetra
        tetra = vtkTetra()
        for i in range(4):
            tetra.GetPointIds().SetId(i, i)
        tetra_grid.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
        
        with self.assertRaises(ValueError) as context:
            get_surface_area(tetra_grid, 0)
        self.assertIn("not a 2D cell", str(context.exception))
    
    def test_non_coplanar_points(self):
        """测试非共面点检测"""
        # 创建非共面的四边形
        non_coplanar_grid = vtkUnstructuredGrid()
        points = vtkPoints()
        points.InsertNextPoint(0, 0, 0)      # 点1
        points.InsertNextPoint(1, 0, 0)      # 点2  
        points.InsertNextPoint(1, 1, 0)      # 点3
        points.InsertNextPoint(0, 0, 0.1)    # 点4 (不在XY平面)
        
        quad = vtkQuad()
        for i in range(4):
            quad.GetPointIds().SetId(i, i)
            
        non_coplanar_grid.SetPoints(points)
        non_coplanar_grid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())
        
        with self.assertRaises(ValueError) as context:
            get_surface_area(non_coplanar_grid, 0)
        self.assertIn("not coplanar", str(context.exception))
    
    def test_check_coplanar_function(self):
        """测试共面性检查函数"""
        # 测试共面点
        coplanar_points = vtkPoints()
        coplanar_points.InsertNextPoint(0, 0, 0)
        coplanar_points.InsertNextPoint(1, 0, 0)
        coplanar_points.InsertNextPoint(0, 1, 0)
        coplanar_points.InsertNextPoint(1, 1, 0)
        self.assertTrue(check_coplanar(coplanar_points))
        
        # 测试非共面点
        non_coplanar_points = vtkPoints()
        non_coplanar_points.InsertNextPoint(0, 0, 0)
        non_coplanar_points.InsertNextPoint(1, 0, 0)
        non_coplanar_points.InsertNextPoint(0, 1, 0)
        non_coplanar_points.InsertNextPoint(0, 0, 0.1)
        self.assertFalse(check_coplanar(non_coplanar_points, tolerance=1e-3))
        
        # 测试三点总是共面
        three_points = vtkPoints()
        three_points.InsertNextPoint(0, 0, 0)
        three_points.InsertNextPoint(1, 0, 0)
        three_points.InsertNextPoint(0, 1, 0)
        self.assertTrue(check_coplanar(three_points))


if __name__ == '__main__':
    unittest.main()