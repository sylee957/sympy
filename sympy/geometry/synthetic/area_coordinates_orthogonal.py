from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.polys.rings import sring
from sympy.core.expr import Expr
from sympy.polys.polytools import cancel


def _area_coordinates_pythagoras(O, U, V, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            if A == C:
                subs[G] = (
                    Pythagoras(O, U, O) *
                    (Area(O, V, A) - Area(O, V, B))**2 / Area(O, U, V)**2 +
                    Pythagoras(O, V, O) *
                    (Area(O, U, A) - Area(O, U, B))**2 / Area(O, U, V)**2
                )
            else:
                subs[G] = (
                    Pythagoras(A, B, A) / 2 +
                    Pythagoras(B, C, B) / 2 -
                    Pythagoras(A, C, A) / 2)

    return subs


def _geometric_subexpressions(expr):
    if isinstance(expr, Expr):
        return {expr}
    if not expr.args:
        return set()
    return set.union(*(_geometric_subexpressions(arg) for arg in expr.args))


def _align_area_OUV(O, U, V, objective):
    canonical = Area(O, U, V)
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area):
            if G.args == (U, V, O) or G.args == (V, O, U):
                subs[G] = canonical
            elif G.args == (O, V, U) or G.args == (U, O, V) or G.args == (V, U, O):
                subs[G] = -canonical
    return subs


def _area_coordinates_herron(O, U, V, objective):
    ouo = Pythagoras(O, U, O)
    ovo = Pythagoras(O, V, O)
    ouv = Area(O, U, V)
    elim = ouv**2 - ouo * ovo / 16

    subs = {}
    for X in _geometric_subexpressions(objective):
        if not X.has(ouv):
            continue
        f, g = X.as_numer_denom()
        R, (F, G, E) = sring((f, g, elim), ouv, ouo, ovo)
        R = R.to_domain()
        F = R.to_sympy(F.rem(E))
        G = R.to_sympy(G.rem(E))
        target = cancel(F / G)
        if X != target:
            subs[X] = target

    return subs
