# modify_point_coordinate 函数使用说明

## 功能概述
提供安全、高效的方法来修改 vtkUnstructuredGrid 中指定点的坐标，同时保持所有其他属性不变。

## 主要函数

### 1. `modify_point_coordinate(vtk_grid, point_id, new_coordinate)`
修改单个点的坐标

**参数：**
- `vtk_grid`: vtkUnstructuredGrid 对象
- `point_id`: 要修改的点的ID（非负整数）
- `new_coordinate`: 新坐标 (x, y, z) 元组或列表

**返回值：**
- `bool`: True 表示修改成功

**异常：**
- `TypeError`: 网格类型错误
- `ValueError`: point_id 或坐标格式错误
- `IndexError`: point_id 超出范围

### 2. `batch_modify_point_coordinates(vtk_grid, point_id_coord_pairs)`
批量修改多个点的坐标

**参数：**
- `vtk_grid`: vtkUnstructuredGrid 对象
- `point_id_coord_pairs`: [(point_id, (x, y, z)), ...] 列表

**返回值：**
- `int`: 成功修改的点数量

## 使用示例

```python
from NMM.base.VTKBase.modify_point_coordinate import modify_point_coordinate, batch_modify_point_coordinates
from vtkmodules.all import vtkUnstructuredGrid, vtkPoints

# 创建测试网格
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)

grid = vtkUnstructuredGrid()
grid.SetPoints(points)

# 单点修改
modify_point_coordinate(grid, 1, (2.0, 3.0, 4.0))
print(f"点1的新坐标: {grid.GetPoint(1)}")  # 输出: (2.0, 3.0, 4.0)

# 批量修改
modifications = [
    (0, (10.0, 10.0, 10.0)),
    (2, (20.0, 20.0, 20.0))
]
count = batch_modify_point_coordinates(grid, modifications)
print(f"成功修改了 {count} 个点")
```

## 特性保证

✅ **坐标精确修改** - 只修改指定点的坐标值
✅ **属性保护** - 不改变点的ID、单元连接关系等其他属性
✅ **数据完整性** - 自动设置 Modified 标志，确保VTK管道更新
✅ **错误处理** - 完善的参数验证和异常处理
✅ **批量操作** - 支持高效批量修改多个点
✅ **容错机制** - 批量操作中跳过无效数据，继续处理有效数据

## 测试覆盖

测试套件包含以下场景：
- 单点坐标修改验证
- 无效参数处理
- 批量修改功能
- 边界条件测试
- 数据完整性验证
- 单元结构保护测试

## 运行测试
```bash
cd /Users/suboyi/PycharmProjects/pythonwithnmm
python -m pytest testNew3D/testModifyPointCoordinate/test_modify_point_coordinate.py -v
```

## 注意事项
1. 点ID必须在有效范围内 [0, GetNumberOfPoints()-1]
2. 坐标必须是长度为3的元组或列表
3. 函数会自动调用 `Modified()` 方法标记数据变更
4. 批量修改时，无效的数据项会被跳过，不影响有效项的处理