from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyMap, PropertyVector
from NMM.base.CacheBase.RelationshipCache import relationship_cache


class CompleteElementBuilder(AbstractElementBuilder):
    def set_simple_properties(self, element_id: int):
        super(CompleteElementBuilder, self).set_simple_properties(element_id)
        temp_property = PropertyInteger(int(self._element_grid.get_cell_attribute('cracked', element_id)[0]))
        temp_property.set_name('cracked')
        self._element.add_property(temp_property)

    def set_patches(self, element_id: int):
        relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None, id_1=element_id)
        patch_id = [int(each_relationship['cover']) for each_relationship in relationship_list]
        temp_property = PropertyList(patch_id)
        temp_property.set_name('math_cover_id')
        self._element.add_property(temp_property)

        patch_coordinate = [self._cover_grid.get_cell_attribute('math_cover_coordinate', i) for i in patch_id]
        temp_property = PropertyList(patch_coordinate)
        temp_property.set_name('math_cover_coordinate')
        self._element.add_property(temp_property)

        patch_displacement_total = [self._cover_grid.get_cell_attribute('math_cover_displacement_total', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_total)
        temp_property.set_name('math_cover_displacement_total')
        self._element.add_property(temp_property)

        patch_displacement_increment = [self._cover_grid.get_cell_attribute('math_cover_displacement_increment', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_increment)
        temp_property.set_name('math_cover_displacement_increment')
        self._element.add_property(temp_property)

    def set_special_points(self, element_id: int):
        relationship_list = relationship_cache.get_item(name_0='element', name_1='specialpoint', id_0=element_id, id_1=None)

        loading_point_id = []  # point_type = 0
        fixed_point_id = []  # point_type = 1
        measured_point_id = []  # point_type = 2

        for each_relationship in relationship_list:
            special_point_id = int(each_relationship['specialpoint'])
            point_type = self._boundary_condition.get_cell_attribute('point_type', special_point_id)[0]
            if point_type == 0:
                loading_point_id.append(special_point_id)
            elif point_type == 1:
                fixed_point_id.append(special_point_id)
            elif point_type == 2:
                measured_point_id.append(special_point_id)

        temp_property = PropertyList(loading_point_id)
        temp_property.set_name('loading_point_id')
        self._element.add_property(temp_property)

        temp_property = PropertyList(fixed_point_id)
        temp_property.set_name('fixed_point_id')
        self._element.add_property(temp_property)

        temp_property = PropertyList(measured_point_id)
        temp_property.set_name('measured_point_id')
        self._element.add_property(temp_property)

        loading_point_coordinate = [self._boundary_condition.get_cell_attribute('special_point_coordinate', i) for i in loading_point_id]
        temp_property = PropertyList(loading_point_coordinate)
        temp_property.set_name('loading_point_coordinate')
        self._element.add_property(temp_property)

        fixed_point_coordinate = [self._boundary_condition.get_cell_attribute('special_point_coordinate', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_coordinate)
        temp_property.set_name('fixed_point_coordinate')
        self._element.add_property(temp_property)

        measured_point_coordinate = [self._boundary_condition.get_cell_attribute('special_point_coordinate', i) for i in measured_point_id]
        temp_property = PropertyList(measured_point_coordinate)
        temp_property.set_name('measured_point_coordinate')
        self._element.add_property(temp_property)

        loading_point_force = [self._boundary_condition.get_cell_attribute('force', i) for i in loading_point_id]
        temp_property = PropertyList(loading_point_force)
        temp_property.set_name('loading_point_force')
        self._element.add_property(temp_property)

        fixed_point_velocity = [self._boundary_condition.get_cell_attribute('velocity', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_velocity)
        temp_property.set_name('fixed_point_velocity')
        self._element.add_property(temp_property)

        fixed_type = [self._boundary_condition.get_cell_attribute('fixed_type', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_type)
        temp_property.set_name('fixed_type')
        self._element.add_property(temp_property)

        fixed_point_displacement_total = [self._boundary_condition.get_cell_attribute('special_point_displacement_total', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_displacement_total)
        temp_property.set_name('fixed_point_displacement_total')
        self._element.add_property(temp_property)

        fixed_point_displacement_increment = [self._boundary_condition.get_cell_attribute('special_point_displacement_increment', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_displacement_increment)
        temp_property.set_name('fixed_point_displacement_increment')
        self._element.add_property(temp_property)
