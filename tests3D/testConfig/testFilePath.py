from NMM.preprocess_3D.Part.FilePath.FilePathBuilder import FilePathBuilder


def testFilePath():
    builder = FilePathBuilder()
    file_path = builder.build('D:/example')
    print(file_path.get_property('work_path'))
    print(file_path.get_property('mesh_path'))
    print(file_path.get_property('geometry_path'))
    print(file_path.get_property('result_path'))

