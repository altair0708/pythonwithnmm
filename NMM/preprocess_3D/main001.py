from NMM.preprocess_3D.Model.ModelBuilder import PreprocessModelBuilder


builder = PreprocessModelBuilder()
model = builder.build('D:/science/NMM/python-NMM/example/example001')

model.initial()
# print(model.get_property('data_structure').get_property('mathematics_point').value.GetNumberOfCells())
# print(model.get_property('database').database_path)

