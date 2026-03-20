# classify_point_vs_closed_surface 函数测试

## 概述
这个测试套件专门用于测试 `classify_point_vs_closed_surface` 函数，该函数用于判断点相对于封闭表面的位置关系。

## 功能测试
测试包括以下场景：

1. **点在表面上** - 测试立方体顶点等确实在表面上的点
2. **点在内部** - 测试封闭几何体内部的点  
3. **点在外部** - 测试远离几何体的点
4. **球体表面分类** - 测试球形几何体的点分类
5. **容差影响** - 测试不同容差值对结果的影响
6. **非封闭表面** - 测试平面等非封闭几何体
7. **边界情况** - 测试零点、远点等特殊情况
8. **不同类型输入** - 测试 vtkUnstructuredGrid 输入

## 运行测试

### 使用 pytest 运行（推荐）
```bash
cd /Users/suboyi/PycharmProjects/pythonwithnmm
python -m pytest testNew3D/testClassifyPointVsClosedSurface/test_classify_point_vs_closed_surface.py -v
```

### 直接运行脚本
```bash
cd /Users/suboyi/PycharmProjects/pythonwithnmm/testNew3D/testClassifyPointVsClosedSurface
python test_classify_point_vs_closed_surface.py
```

## 测试输出示例
```
========================================================= test session starts =========================================================
collected 8 items                                                                                                                     

test_classify_point_vs_closed_surface.py::test_point_on_surface PASSED
test_classify_point_vs_closed_surface.py::test_point_inside_surface PASSED  
test_classify_point_vs_closed_surface.py::test_point_outside_surface PASSED
test_classify_point_vs_closed_surface.py::test_sphere_surface_classification PASSED
test_classify_point_vs_closed_surface.py::test_tolerance_effect PASSED
test_classify_point_vs_closed_surface.py::test_non_closed_surface PASSED
test_classify_point_vs_closed_surface.py::test_edge_cases PASSED
test_classify_point_vs_closed_surface.py::test_unstructured_grid_input PASSED

========================================================== 8 passed in 1.43s ==========================================================
```

## 函数说明
`classify_point_vs_closed_surface(point, surface, tol=1e-6)` 返回以下值之一：
- `"on_surface"` - 点在表面上（在容差范围内）
- `"inside"` - 点在封闭表面内部
- `"outside"` - 点在封闭表面外部

## 依赖
- pytest
- VTK (Visualization Toolkit)
- NMM 项目相关模块

## 注意事项
1. 容差参数 `tol` 影响表面检测的精度
2. 对于复杂的曲面（如球体），网格分辨率会影响准确性
3. 函数假设输入的 surface 是封闭且法向量一致的几何体