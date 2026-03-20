from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyFloat
from NMM.base.CacheBase.RelationshipCache import relationship_cache


class ContactElementBuilder(AbstractElementBuilder):
    def set_simple_properties(self, element_id: int):
        element_grid = self._element_grid

        temp_property = PropertyInteger(int(element_grid.get_cell_attribute('cell_id', element_id)[0]))
        temp_property.set_name('cell_id')
        self._element.add_property(temp_property)

    def set_vertexes(self, element_id: int):
        element_grid = self._element_grid

        point_id = element_grid.get_cell_point_id(element_id)
        temp_property = PropertyList(point_id)
        temp_property.set_name('point_id')
        self._element.add_property(temp_property)

        point_coordinate = [element_grid.get_point_coordinate(i) for i in point_id]
        temp_property = PropertyList(point_coordinate)
        temp_property.set_name('point_coordinate')
        self._element.add_property(temp_property)

        surface_area = element_grid.get_surface_area(element_id)
        temp_property = PropertyFloat(surface_area)
        temp_property.set_name('surface_area')
        self._element.add_property(temp_property)

        center = element_grid.get_cell_attribute('center_coordinate_0', element_id)
        temp_property = PropertyList(center)
        temp_property.set_name('center_coordinate_0')
        self._element.add_property(temp_property)

        center = element_grid.get_cell_attribute('center_coordinate_1', element_id)
        temp_property = PropertyList(center)
        temp_property.set_name('center_coordinate_1')
        self._element.add_property(temp_property)

    def set_patches(self, surface_id: int):
        element_id = relationship_cache.get_item('element', 'cracksurface', None, surface_id)[0]['element']
        new_element_id = relationship_cache.get_item('element', 'newelement', element_id, None)
        assert len(new_element_id) == 2

        for each_id, each in enumerate(new_element_id):
            new_cover_id = relationship_cache.get_item('newcover', 'newelement', None, each['newelement'])
            patch_id = [int(each_relationship['newcover']) for each_relationship in new_cover_id]

            temp_property = PropertyInteger(each['newelement'])
            temp_property.set_name(f'new_element_id_{each_id}')
            self._element.add_property(temp_property)

            patch_total_id = [int(self._cover_grid.get_cell_attribute('total_id', i)[0]) for i in patch_id]
            temp_property = PropertyList(patch_total_id)
            temp_property.set_name(f'math_cover_id_{each_id}')
            self._element.add_property(temp_property)

            patch_displacement_total = [self._cover_grid.get_cell_attribute('math_cover_displacement_total', i) for i in
                                        patch_id]
            temp_property = PropertyList(patch_displacement_total)
            temp_property.set_name(f'math_cover_displacement_total_{each_id}')
            self._element.add_property(temp_property)

            patch_displacement_increment = [self._cover_grid.get_cell_attribute('math_cover_displacement_increment', i) for i in patch_id]
            temp_property = PropertyList(patch_displacement_increment)
            temp_property.set_name(f'math_cover_displacement_increment_{each_id}')
            self._element.add_property(temp_property)

            patch_coordinate = [self._cover_grid.get_cell_attribute('math_cover_coordinate', i) for i in patch_id]
            temp_property = PropertyList(patch_coordinate)
            temp_property.set_name(f'math_cover_coordinate_{each_id}')
            self._element.add_property(temp_property)

    def set_special_points(self, *args, **kwargs):
        pass
