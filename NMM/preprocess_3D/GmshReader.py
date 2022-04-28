from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridWriter,
    vtkXMLUnstructuredGridReader
)


class GmshReader:
    # simple extraction
    @staticmethod
    def generate_vertex(gmsh_file_name: str):
        pass

    @staticmethod
    def generate_wireframe(gmsh_file_name: str):
        pass

    @staticmethod
    def generate_surface(gmsh_file_name: str):
        pass

    @staticmethod
    def generate_tetrahedron(gmsh_file_name: str):
        pass

    # generate relate math cover
    @staticmethod
    def generate_math_cover(gmsh_file_name: str):
        pass

    @staticmethod
    def generate_math_point(gmsh_file_name: str):
        pass

    # generate relate manifold_element
    @staticmethod
    def generate_manifold_element(gmsh_file_name: str):
        pass
