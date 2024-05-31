from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Property.Property.VtkGrid import VtkGrid


class VtkGridAddAttribute(AbstractCommand):

    def __init__(self, vtk_grid: VtkGrid, attribute_name: str):
        self.__vtk_grid = vtk_grid
        self.__attribute_name = attribute_name

    def execute(self):
        self.__vtk_grid.add_attribute(self.__attribute_name)
