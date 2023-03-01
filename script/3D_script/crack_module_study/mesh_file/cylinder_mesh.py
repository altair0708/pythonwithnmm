import pygmsh

with pygmsh.occ.Geometry() as geom:
    geom.add_cylinder((0, 0, 0), (4, 0, 0), 10, mesh_size=1)
    mesh = geom.generate_mesh()
mesh.write('gmsh_file.vtu')
