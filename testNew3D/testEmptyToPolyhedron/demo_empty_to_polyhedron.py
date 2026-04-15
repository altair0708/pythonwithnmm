"""
Demonstration script for empty_to_polyhedron function.
This script shows how to convert an empty cell to a polyhedron.
"""

from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_EMPTY_CELL, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.base.VTKBase.empty_to_polyhedron import empty_to_polyhedron


def demo_tetrahedron_conversion():
    """Demonstrate conversion of tetrahedron-shaped empty cell to polyhedron"""
    print("=" * 60)
    print("Demo 1: Converting Tetrahedron Empty Cell to Polyhedron")
    print("=" * 60)
    
    # Create an empty cell with tetrahedron point structure
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(0, 0, 1)
    
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)
    
    # Insert an empty cell
    empty_cell_ids = vtkIdList()
    empty_cell_ids.InsertNextId(0)
    empty_cell_ids.InsertNextId(1)
    empty_cell_ids.InsertNextId(2)
    empty_cell_ids.InsertNextId(3)
    grid.InsertNextCell(VTK_EMPTY_CELL, empty_cell_ids)
    
    print(f"Original grid:")
    print(f"  - Number of cells: {grid.GetNumberOfCells()}")
    print(f"  - Number of points: {grid.GetNumberOfPoints()}")
    print(f"  - Cell type: Empty Cell (VTK_EMPTY_CELL)")
    
    # Convert to polyhedron
    result = empty_to_polyhedron(grid)
    
    print(f"\nConverted grid:")
    print(f"  - Number of cells: {result.GetNumberOfCells()}")
    print(f"  - Number of points: {result.GetNumberOfPoints()}")
    print(f"  - Cell type: Polyhedron (VTK_POLYHEDRON)")
    
    # Get face stream
    face_stream = vtkIdList()
    result.GetFaceStream(0, face_stream)
    print(f"  - Number of faces: {face_stream.GetId(0)}")
    print(f"  - Face stream length: {face_stream.GetNumberOfIds()}")
    
    # Save to file
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName('demo_tetrahedron_polyhedron.vtu')
    writer.SetInputData(result)
    writer.Write()
    print(f"\nResult saved to: demo_tetrahedron_polyhedron.vtu")
    

def demo_cube_conversion():
    """Demonstrate conversion of cube-shaped empty cell to polyhedron"""
    print("\n" + "=" * 60)
    print("Demo 2: Converting Cube Empty Cell to Polyhedron")
    print("=" * 60)
    
    # Create an empty cell with cube point structure
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
    
    print(f"Original grid:")
    print(f"  - Number of cells: {grid.GetNumberOfCells()}")
    print(f"  - Number of points: {grid.GetNumberOfPoints()}")
    print(f"  - Cell type: Empty Cell (VTK_EMPTY_CELL)")
    
    # Convert to polyhedron
    result = empty_to_polyhedron(grid)
    
    print(f"\nConverted grid:")
    print(f"  - Number of cells: {result.GetNumberOfCells()}")
    print(f"  - Number of points: {result.GetNumberOfPoints()}")
    print(f"  - Cell type: Polyhedron (VTK_POLYHEDRON)")
    
    # Get face stream
    face_stream = vtkIdList()
    result.GetFaceStream(0, face_stream)
    print(f"  - Number of faces: {face_stream.GetId(0)}")
    print(f"  - Face stream length: {face_stream.GetNumberOfIds()}")
    
    # Save to file
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName('demo_cube_polyhedron.vtu')
    writer.SetInputData(result)
    writer.Write()
    print(f"\nResult saved to: demo_cube_polyhedron.vtu")


def demo_2d_rejection():
    """Demonstrate that 2D (planar) empty cells are rejected"""
    print("\n" + "=" * 60)
    print("Demo 3: 2D Empty Cell Rejection")
    print("=" * 60)
    
    # Create a 2D (planar) empty cell
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
    
    print(f"Attempting to convert 2D (planar) empty cell...")
    
    try:
        result = empty_to_polyhedron(grid)
        print("ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"✓ Correctly rejected with error: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Empty Cell to Polyhedron Conversion Demo")
    print("=" * 60)
    
    demo_tetrahedron_conversion()
    demo_cube_conversion()
    demo_2d_rejection()
    
    print("\n" + "=" * 60)
    print("All demos completed successfully!")
    print("=" * 60)
