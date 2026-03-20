# get_surface_area 函数测试

## 概述
这个测试套件专门用于测试 `get_surface_area` 函数，该函数用于计算VTK网格中2D单元的面积。

## 功能测试
测试包括以下场景：

1. **三角形面积计算** - 测试基本三角形单元的面积计算
2. **四边形面积计算** - 测试四边形单元的面积计算
3. **多边形面积计算** - 测试任意多边形单元的面积计算
4. **无效单元ID处理** - 测试超出范围和负数ID的处理
5. **3D单元拒绝** - 测试对3D单元（如四面体）的拒绝
6. **非共面点检测** - 测试对非共面点的检测和拒绝
7. **共面性检查函数** - 测试底层的共面性检查功能
8. **多单元网格** - 测试包含多种2D单元的复杂网格
9. **边界情况** - 测试特殊边界条件

## 运行测试

### 使用 pytest 运行（推荐）
```bash
cd /Users/suboyi/PycharmProjects/pythonwithnmm
python -m pytest testNew3D/testGetSurfaceArea/test_get_surface_area.py -v
```

### 直接运行脚本
```bash
cd /Users/suboyi/PycharmProjects/pythonwithnmm/testNew3D/testGetSurfaceArea
python test_get_surface_area.py
```

## 测试覆盖率
- ✅ 2D单元类型验证（三角形、四边形、多边形）
- ✅ 单元ID有效性检查
- ✅ 共面性检测
- ✅ 面积计算准确性
- ✅ 3D单元拒绝
- ✅ 非共面点检测
- ✅ 边界情况处理
- ✅ 多单元网格支持

## 注意事项
1. 函数仅支持2D单元类型（VTK_TRIANGLE, VTK_QUAD, VTK_POLYGON）
2. 所有单元点必须共面，否则会抛出异常
3. 单元ID必须在有效范围内
4. 计算出的面积必须为正数