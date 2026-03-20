from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_QUAD, VTK_POLYGON
import numpy as np
from NMM.base.CalculateArea import calculate_area


def check_coplanar(points: vtkPoints, tolerance=1e-6):
    """
    检查点集是否共面
    
    Args:
        points: vtkPoints对象
        tolerance: 共面性检测容差
    
    Returns:
        bool: 如果点集共面返回True，否则返回False
    """
    point_number = points.GetNumberOfPoints()
    if point_number < 3:
        return True
    
    # 提取所有点坐标
    point_array = []
    for i in range(point_number):
        point_array.append(points.GetPoint(i))
    
    # 使用SVD方法检查共面性
    points_np = np.array(point_array)
    centroid = np.mean(points_np, axis=0)
    centered = points_np - centroid
    
    # 进行奇异值分解
    try:
        _, singular_values, _ = np.linalg.svd(centered)
        # 如果最小奇异值接近0，则点集共面
        return singular_values[-1] < tolerance
    except np.linalg.LinAlgError:
        return False


def get_surface_area(element_grid: vtkUnstructuredGrid, element_id):
    """
    计算2D单元的面积
    
    Args:
        element_grid: vtkUnstructuredGrid对象
        element_id: 单元ID
    
    Returns:
        float: 单元面积
    
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
    
    # 计算面积
    area = calculate_area(cell_points)
    
    # 验证面积为正数
    if area <= 0:
        raise ValueError(f"Calculated area is not positive: {area}")
    
    return area
