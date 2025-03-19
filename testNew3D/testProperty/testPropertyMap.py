from NMM.base.Property.Implement.PropertyMap import PropertyMap


def test_property_map():
    property_map = PropertyMap.generate_from_toml('global_variable.toml', 'attribute')
    print(property_map['cell_id']['tuple_dimensional'])

