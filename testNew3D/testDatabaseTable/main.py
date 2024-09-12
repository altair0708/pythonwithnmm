from NMM.base.Property.Implement.DatabaseTable import DatabaseTable
from NMM.base.CacheBase.RelationshipCache import relationship_cache


def test_database_table():
    table = DatabaseTable('b_c', 'test.db')
    relationship_cache.add_observer(table)
    relationship_cache.add_item('b', 0, 'c', 1)
