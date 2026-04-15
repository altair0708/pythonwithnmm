"""Test suite for empty_to_polyhedron function"""

import pytest
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_EMPTY_CELL, VTK_POLYHEDRON, VTK_TETRA, VTK_TRIANGLE
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from NMM.base.VTKBase.empty_to_polyhedron import empty_to_polyhedron


def create_empty_cell_grid_with_tetrahedron_points():
    """Create an empty cell grid with tetrahedron point structure"""
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(0, 0, 1)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # Insert an empty cell (type 41 is VTK_EMPTY_CELL)
    empty_cell_ids = vtkIdList()
    empty_cell_ids.InsertNextId(0)
    empty_cell_ids.InsertNextId(1)
    empty_cell_ids.InsertNextId(2)
    empty_cell_ids.InsertNextId(3)
    grid.InsertNextCell(VTK_EMPTY_CELL, empty_cell_ids)
    
    return grid


def create_empty_cell_grid_with_cube_points():
    """Create an empty cell grid with cube point structure"""
    points = vtkPoints()
    # Cube vertices
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(0, 0, 1)
    points.InsertNextPoint(1, 0, 1)
    points.InsertNextPoint(1, 1, 1)
    points.InsertNextPoint(0, 1, 1)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # Insert an empty cell with all 8 cube points
    empty_cell_ids = vtkIdList()
    for i in range(8):
        empty_cell_ids.InsertNextId(i)
    grid.InsertNextCell(VTK_EMPTY_CELL, empty_cell_ids)
    
    return grid


def create_2d_empty_cell_grid():
    """Create a 2D (planar) empty cell grid - should be rejected"""
    points = vtkPoints()
    # All points on z=0 plane
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(0, 1, 0)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    empty_cell_ids = vtkIdList()
    for i in range(4):
        empty_cell_ids.InsertNextId(i)
    grid.InsertNextCell(VTK_EMPTY_CELL, empty_cell_ids)
    
    return grid


def create_non_manifold_empty_cell_grid():
    """Create a non-manifold empty cell grid - should be rejected"""
    # This is tricky to create directly, so we'll skip actual implementation
    # and just document that such cases should raise ValueError
    pass


def test_valid_tetrahedron_empty_cell():
    """Test conversion of valid tetrahedron-shaped empty cell"""
    grid = create_empty_cell_grid_with_tetrahedron_points()
    
    result = empty_to_polyhedron(grid)
    
    # Verify result
    assert isinstance(result, vtkUnstructuredGrid)
    assert result.GetNumberOfCells() == 1
    assert result.GetCellType(0) == VTK_POLYHEDRON
    # A tetrahedron has 4 points
    assert result.GetNumberOfPoints() == 4


def test_valid_cube_empty_cell():
    """Test conversion of valid cube-shaped empty cell"""
    grid = create_empty_cell_grid_with_cube_points()
    
    result = empty_to_polyhedron(grid)
    
    # Verify result
    assert isinstance(result, vtkUnstructuredGrid)
    assert result.GetNumberOfCells() == 1
    assert result.GetCellType(0) == VTK_POLYHEDRON
    # A cube has 8 points
    assert result.GetNumberOfPoints() == 8


def test_2d_empty_cell_rejected():
    """Test that 2D (planar) empty cells are rejected"""
    grid = create_2d_empty_cell_grid()
    
    with pytest.raises(ValueError, match="2D|planar"):
        empty_to_polyhedron(grid)


def test_invalid_input_not_unstructured_grid():
    """Test that non-UnstructuredGrid inputs are rejected"""
    with pytest.raises(AssertionError, match="vtkUnstructuredGrid"):
        empty_to_polyhedron("not a grid")


def test_invalid_input_multiple_cells():
    """Test that grids with multiple cells are rejected"""
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # Add two empty cells
    for _ in range(2):
        cell_ids = vtkIdList()
        cell_ids.InsertNextId(0)
        cell_ids.InsertNextId(1)
        cell_ids.InsertNextId(2)
        grid.InsertNextCell(VTK_EMPTY_CELL, cell_ids)
    
    with pytest.raises(AssertionError, match="exactly one cell"):
        empty_to_polyhedron(grid)


def test_invalid_input_not_empty_cell():
    """Test that non-empty cells are rejected"""
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(0, 0, 1)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # Add a tetrahedron cell instead of empty cell
    tetra_ids = vtkIdList()
    tetra_ids.InsertNextId(0)
    tetra_ids.InsertNextId(1)
    tetra_ids.InsertNextId(2)
    tetra_ids.InsertNextId(3)
    grid.InsertNextCell(VTK_TETRA, tetra_ids)
    
    with pytest.raises(AssertionError, match="empty cell"):
        empty_to_polyhedron(grid)


def test_empty_cell_no_points():
    """Test that empty cells with no points are rejected"""
    points = vtkPoints()
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # Add empty cell with no point IDs
    empty_cell_ids = vtkIdList()
    grid.InsertNextCell(VTK_EMPTY_CELL, empty_cell_ids)
    
    with pytest.raises(ValueError, match="no points"):
        empty_to_polyhedron(grid)


def test_result_preserves_point_coordinates():
    """Test that the result preserves original point coordinates"""
    grid = create_empty_cell_grid_with_tetrahedron_points()
    original_points = grid.GetPoints()
    
    result = empty_to_polyhedron(grid)
    result_points = result.GetPoints()
    
    # Check that all original points are preserved
    assert result_points.GetNumberOfPoints() == original_points.GetNumberOfPoints()
    
    for i in range(original_points.GetNumberOfPoints()):
        orig_coord = original_points.GetPoint(i)
        result_coord = result_points.GetPoint(i)
        for j in range(3):
            assert abs(orig_coord[j] - result_coord[j]) < 1e-10


def test_polyhedron_has_valid_face_stream():
    """Test that the resulting polyhedron has a valid face stream"""
    grid = create_empty_cell_grid_with_tetrahedron_points()
    
    result = empty_to_polyhedron(grid)
    
    # Get face stream
    face_stream = vtkIdList()
    result.GetFaceStream(0, face_stream)
    
    # Face stream should not be empty
    assert face_stream.GetNumberOfIds() > 0
    
    # First value should be number of faces
    num_faces = face_stream.GetId(0)
    assert num_faces > 0


def test_polyhedron_cell_initialization():
    """Test that the resulting polyhedron cell is properly initialized"""
    grid = create_empty_cell_grid_with_cube_points()
    
    result = empty_to_polyhedron(grid)
    
    cell = result.GetCell(0)
    
    # Cell should be initialized
    assert cell is not None
    
    # Should have correct number of points
    assert cell.GetNumberOfPoints() == 8
    
    # Should have faces
    assert cell.GetNumberOfFaces() > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
