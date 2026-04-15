import numpy as np
from scipy.sparse.linalg import cg, spsolve, eigsh, spilu, LinearOperator
from scipy.sparse import diags
from NMM.base.Algorithm.Solver.AbstractSolver import AbstractSolver
from NMM.base.Algorithm.Solver.GeometricPrecondition import GeometricPrecondition
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ConstraintSolver(AbstractSolver):
    def update(self, *args, **kwargs):
        k = self._total_matrix
        f = self._total_force
        k = k.tolil()

        global_variable = entrance_cache.get_item('global_variable_Part')
        material_parameter = global_variable.get_property('material_parameter')
        penalty_parameter = material_parameter['0']['penalty_parameter']

        def get_dofs(node_id):
            return [
                3 * node_id + 0,  # ux
                3 * node_id + 1,  # uy
                3 * node_id + 2  # uz
            ]

        manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')

        cell_id = list(range(manifold_element.get_cell_number()))
        crack_cell_id = filter(lambda x: manifold_element.get_cell_attribute('cracked', x)[0] == 7, cell_id)

        cover_id = set()
        for each_id in crack_cell_id:
            temp = relationship_cache.get_item('cover', 'element', id_0=None, id_1=each_id)
            for each_relationship in temp:
                temp_cover_id = int(each_relationship['cover'])
                if mathematics_point.get_cell_attribute('cracked', temp_cover_id)[0] == 9:
                    cover_id.add(temp_cover_id)

        for each_id in cover_id:
            temp = relationship_cache.get_item('cover', 'newcover', id_0=each_id, id_1=None)
            assert len(temp) == 2
            new_cover_list = [int(x['newcover']) for x in temp]

            real_id = list(filter(lambda x: new_cover.get_cell_attribute('real', x)[0] == 1, new_cover_list))
            virtual_id = list(filter(lambda x: new_cover.get_cell_attribute('real', x)[0] == 0, new_cover_list))
            assert len(real_id) == 1 and len(virtual_id) == 1

            real_id = real_id[0]
            real_id = int(new_cover.get_cell_attribute('total_id', real_id)[0])
            real_id = get_dofs(real_id)

            virtual_id = virtual_id[0]
            virtual_id = int(new_cover.get_cell_attribute('total_id', virtual_id)[0])
            virtual_id = get_dofs(virtual_id)

            constraint_dof = zip(real_id, virtual_id)
            for a, b in constraint_dof:
                # print(a, b)
                k[a, a] += penalty_parameter * 10
                k[b, b] += penalty_parameter * 10
                k[a, b] -= penalty_parameter * 10
                k[b, a] -= penalty_parameter * 10

        k = k.tocsc()

        algorithm = GeometricPrecondition()
        algorithm.update()
        T = algorithm.precondition
        T = diags(T)

        k_precondition = (T @ k @ T).tocsc()
        f_precondition = T @ f

        u_precondition = spsolve(k_precondition, f_precondition)
        u = T @ u_precondition
        # u = spsolve(k, f)

        self._result = u
