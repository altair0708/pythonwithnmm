import pygmsh
import os

output_path = './mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    # geom.add_cylinder((0, 0, 0), (6, 0, 0), 10, mesh_size=1.5)
    geom.add_box(x0=(0, 0, 0), extents=(4, 20, 20), mesh_size=1.5)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
