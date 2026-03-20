from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_QUAD, VTK_POLYGON
import numpy as np
from NMM.base.CalculateArea import calculate_area
from NMM.base.VTKBase.get_surface_area import check_coplanar


def get_surface_center_2d(element_grid: vtkUnstructuredGrid, element_id):
    """
    校验该单元为平面单元，并计算出单元的几何中心
    
    Args:
        element_grid: vtkUnstructuredGrid对象
        element_id: 单元ID
    
    Returns:
        tuple: 几何中心坐标 (x, y, z)
    
    Raises:
        ValueError: 当单元不是2D单元或点不共面时抛出异常
    """
    # 检查单元ID有效性
    if element_id >= element_grid.GetNumberOfCells() or element_id < 0:
        raise ValueError(f"Invalid element_id: {element_id}")
    
    # 获取单元类型
    cell_type = element_grid.GetCellType(element_id)
    
    # 定义有效的2D单元类型
    valid_2d_types = {VTK_TRIANGLE, VTK_QUAD, VTK_POLYGON}
    
    # 验证单元类型
    if cell_type not in valid_2d_types:
        raise ValueError(f"Element {element_id} is not a 2D cell. Cell type: {cell_type}")
    
    # 获取单元
    cell = element_grid.GetCell(element_id)
    cell_points = cell.GetPoints()
    
    # 检查点是否共面
    if not check_coplanar(cell_points):
        raise ValueError(f"Points of element {element_id} are not coplanar")
    
    # 计算几何中心（质心）
    point_number = cell_points.GetNumberOfPoints()
    center_x = 0.0
    center_y = 0.0
    center_z = 0.0
    
    for i in range(point_number):
        x, y, z = cell_points.GetPoint(i)
        center_x += x
        center_y += y
        center_z += z
    
    center_x /= point_number
    center_y /= point_number
    center_z /= point_number
    
    return (center_x, center_y, center_z)
