from tomli import load


def load_toml_file(file_path: str, map_name: str = None):
    with open(file_path, 'rb') as toml_file:
        map_file = load(toml_file)
    if map_name is not None:
        return map_file[map_name]
    else:
        return map_file
