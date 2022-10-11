from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader, vtkXMLUnstructuredGridWriter
from NMM.GlobalVariable import CONST, PATH
from NMM.base.ObjectBase import NmmObjectBase
import sqlite3
import os


class ElementIOer3D(object):
    @staticmethod
    def load_vtk_model(file_name):
        reader = vtkXMLUnstructuredGridReader()
        reader.SetFileName(file_name)
        reader.Update()
        output = reader.GetOutput()
        return output

    @staticmethod
    def load_database(file_name):
        connect = sqlite3.connect(file_name)
        cursor = connect.cursor()
        return cursor

    @staticmethod
    def write_vtk_model(vtk_model: NmmObjectBase):

        if not os.path.exists(PATH.output_path):
            os.mkdir(PATH.output_path)

        model_output = PATH.output_path + vtk_model.name
        if not os.path.exists(model_output):
            os.mkdir(model_output)

        file_name = '{path}/{model_name}_{step:0>3d}.vtu'.format(path=model_output, model_name=vtk_model.name, step=CONST.STEP)
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(file_name)
        writer.SetInputData(vtk_model.content)
        writer.Write()
        del writer


