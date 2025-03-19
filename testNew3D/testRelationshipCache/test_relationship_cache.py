from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabaseBuilder import NmmDatabaseBuilder
from NMM.base.CacheBase import relationship_cache

builder = NmmDatabaseBuilder()
nmm_database = builder.build('test.db', False)


def test_get_relationship():
    relationship_list = relationship_cache.get_item('cover', 'element', id_0=None, id_1=0)
    for each_relationship in relationship_list:
        print(each_relationship['cover'])

