# 测试运行说明

## 快速开始
```bash
# 运行所有测试
python -m pytest testNew3D/testGetSurfaceArea/test_get_surface_area.py -v

# 运行特定测试函数
python -m pytest testNew3D/testGetSurfaceArea/test_get_surface_area.py::test_triangle_area_calculation -v
```

## 测试环境要求
- Python 3.7+
- VTK库
- pytest
- numpy

## 预期输出示例
```
============================= test session starts ==============================
collected 9 items

test_get_surface_area.py::test_triangle_area_calculation PASSED          [ 11%]
test_get_surface_area.py::test_quad_area_calculation PASSED              [ 22%]
test_get_surface_area.py::test_polygon_area_calculation PASSED           [ 33%]
test_get_surface_area.py::test_invalid_element_id PASSED                 [ 44%]
test_get_surface_area.py::test_3d_cell_rejection PASSED                  [ 55%]
test_get_surface_area.py::test_non_coplanar_points_detection PASSED      [ 66%]
test_get_surface_area.py::test_check_coplanar_function PASSED            [ 77%]
test_get_surface_area.py::test_multiple_valid_cells PASSED               [ 88%]
test_get_surface_area.py::test_edge_case_single_point PASSED             [100%]

============================== 9 passed in 0.12s ===============================
```