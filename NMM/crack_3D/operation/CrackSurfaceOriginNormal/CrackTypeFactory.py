from NMM.crack_3D.operation.CrackSurfaceOriginNormal.Implement.FreeCrackSurface import FreeCrackSurface
from NMM.crack_3D.operation.CrackSurfaceOriginNormal.Implement.CoplaneCrackSurface import CoplaneCrackSurface
from NMM.crack_3D.operation.CrackSurfaceOriginNormal.Implement.LSQCrackSurface import LSQCrackSurface


class CrackTypeFactory:
    @staticmethod
    def get_crack_type_factory(crack_type: int):
        if 12 == crack_type:
            return FreeCrackSurface()

        elif 23 == crack_type:
            return CoplaneCrackSurface()
        elif 24 == crack_type:
            return LSQCrackSurface()

        elif 33 == crack_type:
            return CoplaneCrackSurface()
        elif 34 == crack_type:
            return LSQCrackSurface()
        elif 35 == crack_type:
            return LSQCrackSurface()
        elif 36 == crack_type:
            return LSQCrackSurface()

        else:
            raise Exception('Unknown crack type!')

