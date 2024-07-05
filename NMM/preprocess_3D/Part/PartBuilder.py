from NMM.preprocess_3D.Part import PreprocessElementListBuilder, NmmDatabaseBuilder, DataStructureBuilder, FilePathBuilder


class PartBuilder:
    def __init__(self, root_path: str):
        self.__root_path = root_path

    def get_part(self, builder_name):
        if 'file_path' == builder_name:
            builder = FilePathBuilder(self.__root_path)
        elif 'data_structure' == builder_name:
            builder = DataStructureBuilder()
        elif 'database' == builder_name:
            builder = NmmDatabaseBuilder()
        elif 'preprocess_element_list' == builder_name:
            builder = PreprocessElementListBuilder()
        else:
            raise Exception('Builder name error!!!')

        return builder.build()


