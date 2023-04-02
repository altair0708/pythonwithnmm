import pygmsh
import os

output_path = '../../../data_3D/mesh/'
output_path = os.path.abspath(output_path)

with pygmsh.occ.Geometry() as geom:
    geom.add_cylinder((0, 0, 0), (2, 0, 0), 10, mesh_size=1)
    mesh = geom.generate_mesh()
mesh.write(output_path + '/gmsh_file.vtu')
