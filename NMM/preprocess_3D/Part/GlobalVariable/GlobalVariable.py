from NMM.base.Part.Part import Part


class GlobalVariable(Part):
    def __init__(self):
        super(GlobalVariable, self).__init__()
        self.name = 'global_variable'  # global_variable_Part

    def get_variable(self, variable_name: str):
        global_variable = self.get_property('global_variable')  # global_variable_PropertyMap
        return global_variable[variable_name]

