from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometryFrozenSignedRatio as FrozenRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.degenerate import _degenerate_construction
from sympy.geometry.synthetic.options import _auto_coordinates_orthogonal, _auto_option_prove
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_plane
from sympy.geometry.synthetic.simplify import _cancel
from sympy.geometry.synthetic.common import _substitution_rule
from sympy.geometry.synthetic.common import _quadrilateral_area
from sympy.geometry.synthetic.common import _quadrilateral_pythagoras
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _simplify_area
from sympy.geometry.synthetic.common import _simplify_ratio
from sympy.geometry.synthetic.common import _simplify_pythagoras
from sympy.geometry.synthetic.common import _uniformize_area
from sympy.geometry.synthetic.common import _uniformize_pythagoras
from sympy.geometry.synthetic.plane_linear import _linear_pratio
from sympy.geometry.synthetic.plane_linear import _linear_inter_line_line
from sympy.geometry.synthetic.plane_linear import _linear_foot
from sympy.geometry.synthetic.plane_quadratic import _quadratic_pratio
from sympy.geometry.synthetic.plane_quadratic import _quadratic_inter_line_line
from sympy.geometry.synthetic.plane_quadratic import _quadratic_foot
from sympy.geometry.synthetic.plane_tratio import _tratio_area
from sympy.geometry.synthetic.plane_tratio import _tratio_pythagoras
from sympy.geometry.synthetic.plane_tratio import _tratio_quadratic
from sympy.geometry.synthetic.area_coordinates import _area_coordinates
from sympy.geometry.synthetic.area_coordinates_orthogonal import _area_coordinates_pythagoras
from sympy.geometry.synthetic.area_coordinates_orthogonal import _area_coordinates_herron
from sympy.geometry.synthetic.area_coordinates_orthogonal import _align_area_OUV


def _eliminate_image(C, constructions, subs):
    return {k: _eliminate(C, constructions, v) for k, v in subs.items()}


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


def _eliminate_linear_pratio(C, constructions, objective):
    match = _match_pratio(C)
    if match is None:
        return objective
    Y, W, U, V, l = match
    subs = _linear_pratio(Y, W, U, V, l, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_linear_inter_line_line(C, constructions, objective):
    match = _match_inter_line_line(C)
    if match is None:
        return objective
    Y, U, V, P, Q = match
    subs = _linear_inter_line_line(Y, U, V, P, Q, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_linear_foot(C, constructions, objective):
    match = _match_foot(C)
    if match is None:
        return objective
    Y, P, U, V = match
    subs = _linear_foot(Y, P, U, V, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_quadratic_pratio(C, constructions, objective):
    match = _match_pratio(C)
    if match is None:
        return objective
    Y, W, U, V, l = match
    subs = _quadratic_pratio(Y, W, U, V, l, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_quadratic_inter_line_line(C, constructions, objective):
    match = _match_inter_line_line(C)
    if match is None:
        return objective
    Y, U, V, P, Q = match
    subs = _quadratic_inter_line_line(Y, U, V, P, Q, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_quadratic_foot(C, constructions, objective):
    match = _match_foot(C)
    if match is None:
        return objective
    Y, P, U, V = match
    subs = _quadratic_foot(Y, P, U, V, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_tratio_area(C, constructions, objective):
    match = _match_tratio(C)
    if match is None:
        return objective
    Y, P, Q, l = match
    subs = _tratio_area(Y, P, Q, l, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_tratio_pythagoras(C, constructions, objective):
    match = _match_tratio(C)
    if match is None:
        return objective
    Y, P, Q, l = match
    subs = _tratio_pythagoras(Y, P, Q, l, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_tratio_quadratic(C, constructions, objective):
    match = _match_tratio(C)
    if match is None:
        return objective
    Y, P, Q, l = match
    subs = _tratio_quadratic(Y, P, Q, l, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_quadrilateral_expand(C, constructions, objective):
    objective = _substitution_rule(_quadrilateral_area(objective))(objective)
    objective = _substitution_rule(_quadrilateral_pythagoras(objective))(objective)
    objective = _eliminate(C, constructions, objective)
    return objective


def _has_unsolved_quadrilateral(C, objective):
    Y = C.args[0]
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 4 and Y in G.args:
            return True
        if isinstance(G, Pythagoras) and len(G.args) == 4 and Y in G.args:
            return True
    return False


def _eliminate_other_constructions(C, constructions, objective):
    if isinstance(C, On):
        Y, L = C.args
        if isinstance(L, Line):
            U, V = L.args
            C = PRatio(Y, U, Line(U, V), FrozenRatio(U, Y, U, V))
            constructions = tuple(constructions[:-1]) + (C,)
            return _eliminate(C, constructions, objective)
    return objective


def _eliminate(C, constructions, objective):
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _substitution_rule(_simplify_ratio(objective))(objective)
    objective = _substitution_rule(_simplify_pythagoras(objective))(objective)
    objective = _substitution_rule(_uniformize_area(objective))(objective)
    objective = _substitution_rule(_uniformize_pythagoras(objective))(objective)

    objective = _eliminate_linear_pratio(C, constructions, objective)
    objective = _eliminate_linear_inter_line_line(C, constructions, objective)
    objective = _eliminate_linear_foot(C, constructions, objective)

    objective = _eliminate_quadratic_pratio(C, constructions, objective)
    objective = _eliminate_quadratic_inter_line_line(C, constructions, objective)
    objective = _eliminate_quadratic_foot(C, constructions, objective)

    objective = _eliminate_tratio_area(C, constructions, objective)
    objective = _eliminate_tratio_pythagoras(C, constructions, objective)
    objective = _eliminate_tratio_quadratic(C, constructions, objective)

    objective = _eliminate_other_constructions(C, constructions, objective)

    if _has_unsolved_quadrilateral(C, objective):
        objective = _eliminate_quadrilateral_expand(C, constructions, objective)

    objective = _cancel(objective)
    return objective


def _apply_area_coordinates(O, U, V, objective):
    objective = _substitution_rule(_quadrilateral_area(objective))(objective)
    objective = _substitution_rule(_quadrilateral_pythagoras(objective))(objective)

    subs = _area_coordinates(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _area_coordinates_pythagoras(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _align_area_OUV(O, U, V, objective)
    objective = _substitution_rule(subs)(objective)
    subs = _area_coordinates_herron(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)

    objective = _simplify(objective)
    return objective


def _simplify(objective):
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _substitution_rule(_simplify_ratio(objective))(objective)
    objective = _substitution_rule(_simplify_pythagoras(objective))(objective)
    objective = _substitution_rule(_uniformize_area(objective))(objective)
    objective = _substitution_rule(_uniformize_pythagoras(objective))(objective)
    objective = _cancel(objective)
    return objective


def _simplify_image(simplify, subs):
    return {k: simplify(v) for k, v in subs.items()}


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

        Y = C.args[0]
        for G in _geometric_quantities(objective):
            if G.has(Y):
                raise NotImplementedError(f"The elimination step for {Y} in {C} is not properly implemented")

    O, U, V = _auto_coordinates_orthogonal(O, U, V)
    objective = _apply_area_coordinates(O, U, V, objective)

    if prove and objective is not S.true:
        objective = S.false
    return objective
