from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyData, vtkDataSet
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter, vtkXMLPolyDataWriter
import re


def write_file(vtk_model: vtkDataSet, file_path: str):
    extends = ['.vtu', '.vtp', '.vti']
    if isinstance(vtk_model, vtkUnstructuredGrid):
        writer = vtkXMLUnstructuredGridWriter()
        file_path = replace_extensions_in_text(file_path, target_exts=extends, new_ext='.vtu')
    elif isinstance(vtk_model, vtkPolyData):
        writer = vtkXMLPolyDataWriter()
        file_path = replace_extensions_in_text(file_path, target_exts=extends, new_ext='.vtp')
    else:
        raise Exception('Unexpected grid type!!!')
    writer.SetFileName(file_path)
    writer.SetInputData(vtk_model)
    writer.Write()


def debug_write_file(vtk_model: vtkDataSet, file_name: str):
    file_path = '/Users/suboyi/PycharmProjects/pythonwithnmm/debug/' + file_name
    # file_path = 'D:\\science\\NMM\\python-NMM\\debug\\' + file_name
    write_file(vtk_model, file_path)


def replace_extensions_in_text(text, target_exts, new_ext):
    """
    将字符串中所有目标扩展名的文件，替换为新的扩展名。

    参数:
        text (str): 原始字符串
        target_exts (set[str]): 要查找的扩展名，如 {'.vtu', '.vtk'}
        new_ext (str): 要替换成的新扩展名，如 '.vtp'

    返回:
        替换后的字符串
    """
    # 构造正则，匹配包含这些扩展名的文件名
    # [^\s"']+?\.(vtu|vtk) 匹配非空格/引号结尾的路径
    ext_pattern = '|'.join([ext.lstrip('.').lower() for ext in target_exts])
    pattern = rf'([^\s"\'<>]+?)\.({ext_pattern})\b'

    def replacer(match):
        base = match.group(1)  # 文件名不含扩展名部分
        return base + new_ext

    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)


if __name__ == '__main__':
    text = '读取 mesh.vtu 和 model.vtk，忽略 notes.txt 和图像 image.jpg。输出为 processed.vtu'

    new_text = replace_extensions_in_text(text, target_exts=['.vtu', '.vtk'], new_ext='.vtp')
    print(new_text)
    # 输出: '读取 mesh.vtp 和 model.vtp，忽略 notes.txt 和图像 image.jpg。输出为 processed.vtp'
