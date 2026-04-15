# Empty to Polyhedron Test Suite

This directory contains tests and demonstrations for the `empty_to_polyhedron` function.

## Overview

The `empty_to_polyhedron` function converts VTK empty cells (VTK_EMPTY_CELL) to polyhedrons (VTK_POLYHEDRON). This is useful in the NMM (Numerical Manifold Method) framework where empty cells serve as placeholders that need to be converted to proper 3D geometric entities.

## Files

- `test_empty_to_polyhedron.py`: Comprehensive test suite with 10 test cases
- `demo_empty_to_polyhedron.py`: Demonstration script showing usage examples
- `__init__.py`: Package initialization file

## Function Features

The `empty_to_polyhedron` function:

1. **Validates Input**: Ensures the input is a valid vtkUnstructuredGrid with exactly one empty cell
2. **Excludes 2D Cells**: Detects and rejects coplanar (2D) point configurations
3. **Reconstructs Topology**: Automatically determines cell topology based on point count and arrangement
4. **Builds Polyhedron**: Creates proper face streams for tetrahedra and general polyhedra
5. **Cleans Output**: Removes unused points from the resulting grid

## Running Tests

```bash
# Run all tests
cd /Users/suboyi/PycharmProjects/pythonwithnmm
python -m pytest testNew3D/testEmptyToPolyhedron/test_empty_to_polyhedron.py -v

# Run specific test
python -m pytest testNew3D/testEmptyToPolyhedron/test_empty_to_polyhedron.py::test_valid_tetrahedron_empty_cell -xvs
```

## Running Demo

```bash
cd /Users/suboyi/PycharmProjects/pythonwithnmm
PYTHONPATH=/Users/suboyi/PycharmProjects/pythonwithnmm:$PYTHONPATH \
python testNew3D/testEmptyToPolyhedron/demo_empty_to_polyhedron.py
```

The demo will:
1. Convert a tetrahedron-shaped empty cell to polyhedron
2. Convert a cube-shaped empty cell to polyhedron  
3. Demonstrate rejection of 2D (planar) empty cells

Output files:
- `demo_tetrahedron_polyhedron.vtu`: Tetrahedron polyhedron result
- `demo_cube_polyhedron.vtu`: Cube polyhedron result

## Test Cases

The test suite includes:

1. **test_valid_tetrahedron_empty_cell**: Tests conversion of 4-point tetrahedron
2. **test_valid_cube_empty_cell**: Tests conversion of 8-point cube
3. **test_2d_empty_cell_rejected**: Verifies 2D cells are rejected
4. **test_invalid_input_not_unstructured_grid**: Tests type validation
5. **test_invalid_input_multiple_cells**: Tests single-cell requirement
6. **test_invalid_input_not_empty_cell**: Tests empty cell validation
7. **test_empty_cell_no_points**: Tests empty point handling
8. **test_result_preserves_point_coordinates**: Verifies coordinate preservation
9. **test_polyhedron_has_valid_face_stream**: Validates face stream structure
10. **test_polyhedron_cell_initialization**: Checks cell initialization

## Usage Example

```python
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_EMPTY_CELL
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from NMM.base.VTKBase.empty_to_polyhedron import empty_to_polyhedron

# Create empty cell grid
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)

grid = vtkUnstructuredGrid()
grid.SetPoints(points)

empty_cell_ids = vtkIdList()
for i in range(4):
    empty_cell_ids.InsertNextId(i)
grid.InsertNextCell(VTK_EMPTY_CELL, empty_cell_ids)

# Convert to polyhedron
result = empty_to_polyhedron(grid)

# Result is a vtkUnstructuredGrid with VTK_POLYHEDRON cell
print(f"Cell type: {result.GetCellType(0)}")  # Should be 42 (VTK_POLYHEDRON)
```

## Implementation Details

### Topology Reconstruction

- **4 points**: Creates tetrahedron with 4 triangular faces
- **5+ points**: Uses convex hull approach to determine faces
  - Tests all point triplets as potential faces
  - Validates that all other points lie on one side of the face plane
  - Constructs proper face stream format

### 2D Detection

The function detects coplanar points by:
1. Finding three non-collinear points to define a plane
2. Calculating the plane normal vector
3. Checking if all other points lie within tolerance of the plane
4. Rejecting the conversion if points are coplanar

### Face Stream Format

VTK polyhedron face stream format:
```
[num_faces, face0_npts, face0_pt0, face0_pt1, ..., faceN_npts, faceN_pt0, ...]
```

For a tetrahedron:
```
[4, 3, 0, 1, 2, 3, 0, 1, 3, 3, 0, 2, 3, 3, 1, 2, 3]
```

## Error Handling

The function raises:
- `AssertionError`: For invalid input types or structure
- `ValueError`: For 2D cells, insufficient points, or topological issues

## Notes

- The function assumes convex polyhedra for the general case
- For production use with complex geometries, consider integrating a proper convex hull library
- Point coordinates are preserved exactly in the output
- Unused points are automatically removed by vtkCleanUnstructuredGrid
