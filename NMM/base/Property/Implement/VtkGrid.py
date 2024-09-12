from NMM.base.Property.Property import Property
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.VTKBase import get_grid_by_cell_type, generate_cover_grid, add_attribute, write_file, get_attribute, new_a_grid, load_a_grid
from NMM.base.VTKBase import generate_grid, set_attribute, insert_a_vtk_cell
from NMM.base.CacheBase.AttributeCache import attribute_cache
from NMM.base.CacheBase.GeometryCache import geometry_cache
import warnings


class VtkGrid(Property):
    def __init__(self, grid_name: str, file_name: str = None):
        super(VtkGrid, self).__init__()
        self._name = grid_name
        self._type = 'VtkGrid'

        if file_name is None:
            # self._value = new_a_grid(allow_duplicate=False)
            self._value = new_a_grid()
        else:
            self._value = load_a_grid(file_name)

        # modify cache
        attribute_cache.add_observer(self)
        geometry_cache.add_observer(self)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vtk_grid):
        self._value = vtk_grid

    def add_attribute(self, attribute_name):
        add_attribute(self._value, attribute_name)

    # Interface from attribute_cache and geometry_cache, modify attribute
    def modify(self, modify_dict: dict):
        if self._name == modify_dict['grid_name']:
            if 'attribute_name' in modify_dict:
                set_attribute(self._value,
                              modify_dict['attribute_name'],
                              modify_dict['attribute_id'],
                              modify_dict['value'])
            elif 'cell_grid' in modify_dict:
                insert_a_vtk_cell(modify_dict['cell_grid'],
                                  self._value)
            else:
                raise Exception('Modify dict error!!!')

    def get_cover_element_list(self):
        warnings.warn('Deprecation method: get_cover_element_list', DeprecationWarning)
        relationship_list = []
        for each_id in range(self.get_number()):
            each_relationship_list = get_attribute(self._value, each_id, 'cover_element')
            for each_relationship in each_relationship_list:
                relationship_list.append(Relationship('cover_element', each_relationship['cover'], each_relationship['element']))
        return relationship_list

    def get_number(self):
        return self._value.GetNumberOfCells()

    def extract_by_cell_type(self, geometric_name: str):
        warnings.warn('Deprecation method: extract_by_cell_type', DeprecationWarning)
        return get_grid_by_cell_type(self._value, geometric_name)

    def extract_mathematics_cover(self, cover_name):
        warnings.warn('Deprecation method: extract_mathematics_cover', DeprecationWarning)
        return generate_cover_grid(self._value, cover_name)

    def generate_grid(self, entity_name):
        return generate_grid(self._value, entity_name)

    def write_file(self, file_name):
        write_file(self._value, file_name)
