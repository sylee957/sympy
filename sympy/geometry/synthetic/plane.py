from sympy.core.singleton import S
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.degenerate import _degenerate_construction
from sympy.geometry.synthetic.options import _auto_coordinates_orthogonal, _auto_option_prove
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_plane
from sympy.geometry.synthetic.simplify import _cancel


def _match_pratio(C):
    if not isinstance(C, PRatio):
        return None

    Y, W, L, l = C.args
    if not isinstance(L, Line):
        return None

    U, V = L.args
    return Y, W, U, V, l


def _match_inter_line_line(C):
    if not isinstance(C, Intersection):
        return None

    Y, L1, L2 = C.args
    if not isinstance(L1, Line):
        return None
    if not isinstance(L2, Line):
        return None

    U, V = L1.args
    P, Q = L2.args
    return Y, U, V, P, Q


def _match_foot(C):
    if not isinstance(C, Foot):
        return None

    Y, P, L = C.args
    if not isinstance(L, Line):
        return None

    U, V = L.args
    return Y, P, U, V


def _match_tratio(C):
    if not isinstance(C, TRatio):
        return None

    Y, L, l = C.args
    if not isinstance(L, Line):
        return None

    P, Q = L.args
    return Y, P, Q, l


def area_method_plane(constructions, objective, *, O=None, U=None, V=None, prove=None):
    prove = _auto_option_prove(objective, prove)
    objective = _normalize_predicate_plane(objective)

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove:
            assertion = _degenerate_construction(C)
            if area_method_plane(constructions[:i], assertion, prove=True) is S.true:
                return S.true

        while True:
            old = objective
            objective = _eliminate(C, constructions[:i + 1], objective)
            new = objective
            if old == new:
                break

    O, U, V = _auto_coordinates_orthogonal(O, U, V)
    subs = _area_coordinates(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _cancel(objective)

    if prove and objective is not S.true:
        objective = S.false
    return objective
