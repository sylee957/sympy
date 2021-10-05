from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.matrices import Matrix


def _area_coordinates(O, U, V, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3:
            A, B, Y = G.args
            if A == O and B == U:
                continue
            if A == O and B == V:
                continue
            subs[G] = Matrix(
                [[Area(O, U, A), Area(O, V, A), 1],
                 [Area(O, U, B), Area(O, V, B), 1],
                 [Area(O, U, Y), Area(O, V, Y), 1]]
            ).det() / Area(O, U, V)

    return subs
