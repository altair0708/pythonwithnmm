from NMM.base.VTKBase import generate_point_grid


a_grid = generate_point_grid()

b_grid = generate_point_grid()
b_grid.EditableOn()

a_grid.BuildLocator()
b_grid.BuildLocator()

print(a_grid.GetPointLocator())
print(b_grid.GetPointLocator())
