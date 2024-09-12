from NMM.base.CacheBase.CacheInterface import AbstractCache
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


class GeometryCache(AbstractCache):
    def __init__(self):
        super(GeometryCache, self).__init__()

    def add_item(self, grid_name: str, cell_grid: vtkUnstructuredGrid):
        self._cache_list.append({'grid_name': grid_name, 'cell_grid': cell_grid})
        self.update()


geometry_cache = GeometryCache()

