from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.matrices import Matrix


def _area_coordinates_pythagoras(O, U, V, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            if A == C:
                subs[G] = (
                    Pythagoras(O, U, O) / 2 *
                    (Area(O, V, A) - Area(O, V, B))**2 / Area(O, U, V)**2 +
                    Pythagoras(O, V, O) / 2 *
                    (Area(O, U, A) - Area(O, U, B))**2 / Area(O, U, V)**2
                )
            else:
                subs[G] = (
                    Pythagoras(A, B, A) / 2 +
                    Pythagoras(B, C, B) / 2 -
                    Pythagoras(A, C, A) / 2)

    return subs


def _area_coordinates_base(O, U, V, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3:
            A, B, C = G.args
            if A == C:
                subs[G] = (
                    Pythagoras(O, U, O) / 2 *
                    (Area(O, V, A) - Area(O, V, B))**2 / Area(O, U, V)**2 +
                    Pythagoras(O, V, O) / 2 *
                    (Area(O, U, A) - Area(O, U, B))**2 / Area(O, U, V)**2
                )
            else:
                subs[G] = (
                    Pythagoras(A, B, A) / 2 +
                    Pythagoras(B, C, B) / 2 -
                    Pythagoras(A, C, A) / 2)

    return subs
