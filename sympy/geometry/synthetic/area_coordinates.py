from sympy.geometry.synthetic.common import _inject_new_variables_and_eliminate, _compress
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.matrices import Matrix


def _area_coordinates(O, U, V, domain, objective):
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3:
            A, B, Y = G.args
            if A == O and B == U:
                continue
            if A == O and B == V:
                continue

            eliminant = Matrix(
                [[Area(O, U, A), Area(O, V, A), 1],
                 [Area(O, U, B), Area(O, V, B), 1],
                 [Area(O, U, Y), Area(O, V, Y), 1]]
            ).det() / Area(O, U, V)
            eliminant = eliminant.doit()

            if eliminant == G:
                continue

            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective
