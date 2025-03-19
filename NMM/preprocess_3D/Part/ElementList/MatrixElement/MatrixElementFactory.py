from NMM.preprocess_3D.Part.ElementList.MatrixElement.MatrixElementBase import MatrixElementBase
from NMM.preprocess_3D.Part.ElementList.MatrixElement.ElementFactoryInterface import AbstractElementFactory
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement import PropertyMap, PropertyVector, PropertyMatrix, PropertyString, PropertyId, PropertyInteger, PropertyFloat, PropertyBool
from typing import List


class MatrixElementFactory(AbstractElementFactory):
    def build(self, element_id: int, manifold_element: VtkGrid, attribute_toml: str = None) -> List:

        if attribute_toml is None:
            from NMM.base.CacheBase.EntranceCache import entrance_cache
            attribute_map = entrance_cache.get_item('global_variable_Part')['attribute']
        else:
            attribute_map = PropertyMap.generate_from_toml(attribute_toml, 'attribute')

        new_matrix_element = MatrixElementBase()
        for each_attribute_id in range(manifold_element.get_cell_attribute_number()):

            attribute_name = manifold_element.get_cell_attribute_name(each_attribute_id)
            each_attribute = attribute_map[attribute_name]
            tuple_dimensional = int(each_attribute['tuple_dimensional'])
            array_type = each_attribute['array_type']

            if tuple_dimensional == 1:
                attribute_value = manifold_element.get_cell_attribute(attribute_name, element_id)[0]
                if array_type == 'int':
                    temp_property = PropertyInteger(int(attribute_value))
                elif array_type == 'float':
                    temp_property = PropertyFloat(float(attribute_value))
                else:
                    raise Exception('Array type error!!!')
            elif tuple_dimensional > 1:
                attribute_value = manifold_element.get_cell_attribute(attribute_name, element_id)
                temp_property = PropertyVector(attribute_value)
            else:
                raise Exception('Tuple dimensional error!!!')

            temp_property.set_name(attribute_name)

            new_matrix_element.add_property(temp_property)

        return [new_matrix_element]
