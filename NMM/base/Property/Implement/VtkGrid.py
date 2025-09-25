from NMM.base.Property.Property import Property
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.VTKBase import get_grid_by_cell_type, generate_cover_grid, add_attribute
from NMM.base.VTKBase import generate_grid, insert_a_vtk_cell, get_a_vtk_cell_grid, delete_vtk_cell
from NMM.base.VTKBase import get_cell_point_id, get_point_coordinate
from NMM.base.VTKBase import get_cell_attribute_number, get_point_attribute_number
from NMM.base.VTKBase import new_a_grid, load_a_grid, write_file
from NMM.base.VTKBase import get_cell_attribute_name, get_point_attribute_name
from NMM.base.VTKBase import get_attribute, get_cell_attribute, get_point_attribute
from NMM.base.VTKBase import set_attribute, set_cell_attribute, set_point_attribute
from NMM.base.VTKBase.is_empty_cell import is_empty_cell_id
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_point import insert_a_point
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_line_with_point_id import insert_a_line_with_point_id
from NMM.base.VTKBase.get_point_cell_id import get_point_cell_id
from NMM.base.CacheBase import attribute_cache, geometry_cache
from NMM.base.Command.ModelCommand.ModelGetObject import ModelGetObject
from NMM.base.Command.Invoker import Invoker
from collections.abc import Iterator, Iterable
import warnings


class AlphabeticalOrderIterator(Iterator):
    """
    Concrete Iterators implement various traversal algorithms. These classes
    store the current traversal position at all times.
    """

    """
    `_position` attribute stores the current traversal position. An iterator may
    have a lot of other fields for storing iteration state, especially when it
    is supposed to work with a particular kind of collection.
    """
    _position: int = None

    """
    This attribute indicates the traversal direction.
    """
    _reverse: bool = False

    def __init__(self, collection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = get_a_vtk_cell_grid(self._collection.value, self._position)
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class VtkGrid(Property):
    def __init__(self, grid_name: str, file_name: str = None):
        super(VtkGrid, self).__init__()
        self._type = 'VtkGrid'
        self.name = grid_name

        if file_name is None:
            # self._value = new_a_grid(allow_duplicate=False)
            self._value = new_a_grid()
        else:
            self._value = load_a_grid(file_name)

        # modify cache
        attribute_cache.add_observer(self)
        geometry_cache.add_observer(self)

    def __getitem__(self, index: int):
        return get_a_vtk_cell_grid(self._value, index)

    def __iter__(self) -> AlphabeticalOrderIterator:
        """
        The __iter__() method returns the iterator object itself, by default we
        return the iterator in ascending order.
        """
        return AlphabeticalOrderIterator(self)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vtk_grid):
        self._value = vtk_grid

    def add_attribute(self, attribute_name, attribute_toml: str = None):
        add_attribute(self._value, attribute_name, attribute_toml)

    def set_attribute(self, attribute_name: str, cell_id: int, value):
        set_attribute(self._value, attribute_name, cell_id, value)

    def get_attribute(self, attribute_name: str, cell_id: int):
        # get attribute you don't know if cell_attribute or point_attribute
        return get_attribute(self._value, attribute_name, cell_id)

    def get_point_attribute(self, attribute_name: str, point_id: int):
        return get_point_attribute(self._value, attribute_name, point_id)

    def set_point_attribute(self, attribute_name: str, point_id: int, value):
        set_point_attribute(self._value, attribute_name, point_id, value)

    def get_cell_attribute(self, attribute_name: str, cell_id: int):
        return get_cell_attribute(self._value, attribute_name, cell_id)

    def set_cell_attribute(self, attribute_name: str, cell_id: int, value):
        set_cell_attribute(self._value, attribute_name, cell_id, value)

    def get_cell_attribute_number(self):
        return get_cell_attribute_number(self._value)

    def get_point_attribute_number(self):
        return get_point_attribute_number(self._value)

    def get_cell_attribute_name(self, attribute_id):
        return get_cell_attribute_name(self._value, attribute_id)

    def get_point_attribute_name(self, attribute_id):
        return get_point_attribute_name(self._value, attribute_id)

    def get_point_coordinate(self, point_id):
        return get_point_coordinate(self._value, point_id)

    def get_cell_point_id(self, cell_id):
        return get_cell_point_id(self._value, cell_id)

    # Interface from attribute_cache and geometry_cache, modify attribute
    def insert(self, modify_dict: dict):
        if self._name == modify_dict['grid_name']:
            if 'attribute_name' in modify_dict:
                set_attribute(self._value, modify_dict['attribute_name'], modify_dict['attribute_id'], modify_dict['value'])
            elif 'cell_grid' in modify_dict:
                insert_a_vtk_cell(modify_dict['cell_grid'], self._value)
            else:
                raise Exception('Modify dict error!!!')

    def get_cover_element_list(self):
        warnings.warn('Deprecation method: get_cover_element_list', DeprecationWarning)
        relationship_list = []
        for each_id in range(self.get_number()):
            each_relationship_list = get_attribute(self._value, 'cover_element', each_id)
            for each_relationship in each_relationship_list:
                relationship_list.append(Relationship('cover_element', each_relationship['cover'], each_relationship['element']))
        return relationship_list

    def extract_by_cell_type(self, geometric_name: str):
        warnings.warn('Deprecation method: extract_by_cell_type', DeprecationWarning)
        return get_grid_by_cell_type(self._value, geometric_name)

    def extract_mathematics_cover(self, cover_name):
        warnings.warn('Deprecation method: extract_mathematics_cover', DeprecationWarning)
        return generate_cover_grid(self._value, cover_name)

    def get_number(self):
        return self._value.GetNumberOfCells()

    def generate_grid(self, entity_name):
        return generate_grid(self._value, entity_name)

    def write_file(self, file_path: str = None):
        if file_path is None:
            invoker = Invoker()
            invoker.set_command(ModelGetObject(f'{self.name}_Path'))
            file_name = invoker.press_button()
            file_path = file_name.value
        write_file(self._value, file_path)

    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self, True)

    def get_cell_number(self):
        return self._value.GetNumberOfCells()

    def get_point_number(self):
        return self._value.GetNumberOfPoints()

    def add_item(self, item) -> None:
        return insert_a_vtk_cell(item, self._value)

    def delete_cell(self, id_value: int):
        delete_vtk_cell(self._value, id_value)

    def get_file_name(self):
        file_name = f'{self.name}.vtu'
        return file_name
    
    def is_empty_cell(self, cell_id: int):
        return is_empty_cell_id(self._value, cell_id)

    def insert_a_point(self, coordinate):
        return insert_a_point(self._value, coordinate)

    def insert_a_line_with_point_id(self, id_0: int, id_1: int):
        insert_a_line_with_point_id(self._value, id_0, id_1)

    def get_point_cell_id(self, point_id: int):
        return get_point_cell_id(self._value, point_id)
