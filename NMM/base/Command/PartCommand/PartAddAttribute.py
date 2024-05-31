from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Command.PropertyCommand.PropertyAddAttribute import PropertyAddAttribute
from NMM.base.Command.Invoker import Invoker
from NMM.base.Part.Part import Part


class PartAddAttribute(AbstractCommand):

    def __init__(self, data_structure: Part, grid_name: str, attribute_name: str):
        self.__part = data_structure
        self.__grid_name = grid_name
        self.__attribute_name = attribute_name

    def execute(self):
        vtk_grid = self.__part.get_property(self.__grid_name)
        new_command = PropertyAddAttribute(vtk_grid, self.__attribute_name)
        invoker = Invoker(new_command)
        invoker.press_button()
