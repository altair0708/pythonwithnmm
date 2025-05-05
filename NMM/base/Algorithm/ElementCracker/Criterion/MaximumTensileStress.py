from NMM.base.Algorithm.ElementCracker.Criterion.CriterionInterface import AbstractCriterion
import numpy as np


class MaximumTensileStress(AbstractCriterion):
    def update(self, *args, **kwargs):
        self.calculate_elastic_stress()
        stress_tensor = self.stress_tensor

        max_component = stress_tensor.max_component_vector[0]
        if max_component > 10000:
            self._crack_flag = True
        self._normal = stress_tensor.max_component_vector[1]
        self._normal = np.array(self._normal).flatten().tolist()

        assert len(self._normal) == 3
