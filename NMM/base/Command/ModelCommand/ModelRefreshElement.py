from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.ElementRefresher.ElementRefresherNew import ElementRefresher
from NMM.base.Algorithm.ElementRefresher.ContactElementRefresher import ContactElementRefresher
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache


class ModelRefreshElement(AbstractCommand):
    def __init__(self):
        self.__mathematics_point = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__manifold_element = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__new_cover = entrance_cache.get_item('new_cover_VtkGrid')
        self.__new_element = entrance_cache.get_item('new_element_VtkGrid')
        self.__crack_surface = entrance_cache.get_item('crack_surface_VtkGrid')

    def execute(self):
        mathematics_point = self.__mathematics_point
        manifold_element = self.__manifold_element
        new_cover = self.__new_cover
        new_element = self.__new_element
        crack_surface: VtkGrid = self.__crack_surface

        element_refresher = ElementRefresher(mathematics_point, manifold_element, new_cover, new_element)
        element_refresher.update()

        try:
            if global_variable_cache.get_item('contact_calculate') == 1:
                for each_id in range(crack_surface.get_cell_number()):
                    refresher = ContactElementRefresher(each_id, new_cover, crack_surface)
                    refresher.update()
        except AssertionError:
            pass

