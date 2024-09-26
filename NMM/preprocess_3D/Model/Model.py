from NMM.base.Model.Model import Model


class PreprocessModel(Model):
    def __init__(self):
        super(PreprocessModel, self).__init__()
        self.name = 'model'


# singleton
preprocess_model = PreprocessModel()
