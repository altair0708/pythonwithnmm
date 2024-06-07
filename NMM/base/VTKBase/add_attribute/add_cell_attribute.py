from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkIntArray, vtkDoubleArray
from NMM.base.VTKBase.add_attribute.add_attribute_interface import FunctionAddAttribute


class AddCellAttribute(FunctionAddAttribute):
    @staticmethod
    def add_int_array(vtk_model: vtkUnstructuredGrid, attribute_name: str, tuple_dimensional: int, is_id=False):
        array = vtkIntArray()
        array.SetName(attribute_name)
        array.SetNumberOfComponents(tuple_dimensional)

        # closure of array tuple
        def initial_tuple(dimensional, id_yes):
            def initial_value(id_value):
                if id_yes:
                    return [id_value for i in range(dimensional)]
                else:
                    return [-1 for i in range(dimensional)]
            return initial_value

        initial_data = initial_tuple(tuple_dimensional, is_id)
        [array.InsertTuple(i, initial_data(i)) for i in range(vtk_model.GetNumberOfCells())]
        vtk_model.GetCellData().AddArray(array)

    @staticmethod
    def add_float_array(vtk_model: vtkUnstructuredGrid, attribute_name: str, tuple_dimensional: int, is_id=False):
        array = vtkDoubleArray()
        array.SetName(attribute_name)
        array.SetNumberOfComponents(tuple_dimensional)
        initial_data = [-1 for i in range(tuple_dimensional)]
        [array.InsertTuple(i, initial_data) for i in range(vtk_model.GetNumberOfCells())]
        vtk_model.GetCellData().AddArray(array)
