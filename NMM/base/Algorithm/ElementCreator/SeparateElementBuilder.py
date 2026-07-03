from NMM.base.Algorithm.ElementCreator.ElementBuilderInterface import AbstractElementBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyMap, PropertyVector, PropertyVtkCell
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase


class SeparateElementBuilder(AbstractElementBuilder):
    def reset(self):
        self._element = ElementBase('separate_element')

    def set_vertexes(self, element_id: int):
        super(SeparateElementBuilder, self).set_vertexes(element_id)

        vtk_cell = self._element_grid[element_id]
        temp_property = PropertyVtkCell(vtk_cell)
        temp_property.set_name('vtk_cell')
        self._element.add_property(temp_property)

    def set_patches(self, element_id: int):
        relationship_list = relationship_cache.get_item(name_0='newcover', name_1='newelement', id_0=None, id_1=element_id)
        patch_id = [int(each_relationship['newcover']) for each_relationship in relationship_list]

        temp_property = PropertyList(patch_id)
        temp_property.set_name('new_cover_id')
        self._element.add_property(temp_property)

        patch_total_id = [int(self._cover_grid.get_cell_attribute('total_id', i)[0]) for i in patch_id]
        temp_property = PropertyList(patch_total_id)
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

        patch_displacement_velocity = [self._cover_grid.get_cell_attribute('math_cover_velocity', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_velocity)
        temp_property.set_name('math_cover_velocity')
        self._element.add_property(temp_property)

    def set_special_points(self, element_id: int):
        # relationship_list = relationship_cache.get_item(name_0='element', name_1='specialpoint', id_0=element_id, id_1=None)
        #
        # loading_point_id = []  # point_type = 0
        # fixed_point_id = []  # point_type = 1
        # measured_point_id = []  # point_type = 2
        #
        # for each_relationship in relationship_list:
        #     special_point_id = int(each_relationship['specialpoint'])
        #     point_type = special_point.get_cell_attribute('point_type', special_point_id)[0]
        #     if point_type == 0:
        #         loading_point_id.append(special_point_id)
        #     elif point_type == 1:
        #         fixed_point_id.append(special_point_id)
        #     elif point_type == 2:
        #         measured_point_id.append(special_point_id)
        #
        temp_property = PropertyList([])
        temp_property.set_name('loading_point_id')
        self._element.add_property(temp_property)

        temp_property = PropertyList([])
        temp_property.set_name('fixed_point_id')
        self._element.add_property(temp_property)

        temp_property = PropertyList([])
        temp_property.set_name('measured_point_id')
        self._element.add_property(temp_property)

        loading_point_coordinate = []
        temp_property = PropertyList(loading_point_coordinate)
        temp_property.set_name('loading_point_coordinate')
        self._element.add_property(temp_property)

        fixed_point_coordinate = []
        temp_property = PropertyList(fixed_point_coordinate)
        temp_property.set_name('fixed_point_coordinate')
        self._element.add_property(temp_property)

        measured_point_coordinate = []
        temp_property = PropertyList(measured_point_coordinate)
        temp_property.set_name('measured_point_coordinate')
        self._element.add_property(temp_property)

        loading_point_force = []
        temp_property = PropertyList(loading_point_force)
        temp_property.set_name('loading_point_force')
        self._element.add_property(temp_property)

        fixed_point_velocity = []
        temp_property = PropertyList(fixed_point_velocity)
        temp_property.set_name('fixed_point_velocity')
        self._element.add_property(temp_property)

        fixed_point_displacement_total = []
        temp_property = PropertyList(fixed_point_displacement_total)
        temp_property.set_name('fixed_point_displacement_total')
        self._element.add_property(temp_property)

        fixed_point_displacement_increment = []
        temp_property = PropertyList(fixed_point_displacement_increment)
        temp_property.set_name('fixed_point_displacement_increment')
        self._element.add_property(temp_property)
