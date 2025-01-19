import numpy as np
from scipy.spatial import Delaunay
from typing import Tuple, List
from NMM.GlobalVariable import CONST
from NMM.fem_3D.PointBase_3D import EPoint3D
from NMM.base.DeltaFFunction import f_function
from NMM.preprocess_3D.Part.ElementList.MatrixElement.ElementInterface import AbstractElement


class MatrixElementBase(AbstractElement):
    pass
