from sympy.core.numbers import Rational
from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometryFrozenSignedRatio as FrozenRatio
)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryMidpoint as Midpoint
)
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel
from sympy.geometry.synthetic.common import (
    _simplify_area,
    _simplify_ratio,
    _uniformize_area,
    _substitution_rule,
    _quadrilateral_area
)
from sympy.geometry.synthetic.affine_area import (
    _area_lratio,
    _area_pratio,
    _area_inter_line_line,
    _area_inter_pline_line,
    _area_inter_pline_pline
)
from sympy.geometry.synthetic.area_coordinates import _area_coordinates
from sympy.geometry.synthetic.options import (
    _auto_option_prove,
    _auto_coordinates_skew
)
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_affine
from sympy.geometry.synthetic.degenerate import _degenerate_construction
from sympy.geometry.synthetic.simplify import _cancel
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.affine_match import (
    _match_inter_line_line,
    _match_pratio,
    _match_lratio,
    _match_inter_pline_line,
    _match_inter_pline_pline
)
from sympy.geometry.synthetic.common import _apply_to_image, match_AYCD


def _ratio_lratio(Y, P, Q, l, constructions, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method_affine(constructions, Collinear(A, P, Q))
            if assertion is S.true:
                subs[G] = (Ratio(A, P, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_pratio(Y, R, P, Q, l, constructions, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method_affine(constructions, Collinear(A, R, Y))
            if assertion is S.true:
                subs[G] = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_line_line(Y, P, Q, U, V, constructions, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method_affine(constructions, Collinear(A, U, V))
            if assertion is S.true:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_pline_line(Y, R, P, Q, U, V, constructions, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method_affine(constructions, Collinear(A, U, V))
            if assertion is S.true:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_pline_pline(Y, R, P, Q, W, U, V, constructions, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method_affine(constructions, Parallel(A, Y, P, Q))
            if assertion is S.true:
                subs[G] = Area(A, U, W, V) / Area(C, U, D, V)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _eliminate_area_lratio(C, constructions, objective):
    match = _match_lratio(C)
    if match is None:
        return objective
    Y, P, Q, r = match
    subs = _area_lratio(Y, P, Q, r, objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_area_pratio(C, constructions, objective):
    match = _match_pratio(C)
    if match is None:
        return objective
    Y, R, P, Q, r = match
    subs = _area_pratio(Y, R, P, Q, r, objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_area_inter_line_line(C, constructions, objective):
    match = _match_inter_line_line(C)
    if match is None:
        return objective
    Y, P, Q, U, V = match
    subs = _area_inter_line_line(Y, P, Q, U, V, objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_area_inter_pline_line(C, constructions, objective):
    match = _match_inter_pline_line(C)
    if match is None:
        return objective
    Y, R, P, Q, U, V = match
    subs = _area_inter_pline_line(Y, R, P, Q, U, V, objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_area_inter_pline_pline(C, constructions, objective):
    match = _match_inter_pline_pline(C)
    if match is None:
        return objective
    Y, R, P, Q, W, U, V = match
    subs = _area_inter_pline_pline(Y, R, P, Q, W, U, V, objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_lratio(C, constructions, area_method, objective):
    match = _match_lratio(C)
    if match is None:
        return objective
    Y, P, Q, r = match
    subs = _ratio_lratio(Y, P, Q, r, constructions + (C,), objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_pratio(C, constructions, area_method, objective):
    match = _match_pratio(C)
    if match is None:
        return objective
    Y, R, P, Q, r = match
    subs = _ratio_pratio(Y, R, P, Q, r, constructions + (C,), objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_inter_line_line(C, constructions, area_method, objective):
    match = _match_inter_line_line(C)
    if match is None:
        return objective
    Y, P, Q, U, V = match
    subs = _ratio_inter_line_line(Y, P, Q, U, V, constructions + (C,), objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_inter_pline_line(C, constructions, area_method, objective):
    match = _match_inter_pline_line(C)
    if match is None:
        return objective
    Y, R, P, Q, U, V = match
    subs = _ratio_inter_pline_line(Y, R, P, Q, U, V, constructions + (C,), objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_inter_pline_pline(C, constructions, area_method, objective):
    match = _match_inter_pline_pline(C)
    if match is None:
        return objective
    Y, R, P, Q, W, U, V = match
    subs = _ratio_inter_pline_pline(Y, R, P, Q, W, U, V, constructions + (C,), objective)
    subs = _apply_to_image(lambda X: _eliminate(C, constructions, X), subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_other_constructions(C, constructions, objective):
    if isinstance(C, On):
        Y, L = C.args
        if isinstance(L, Line):
            P, Q = L.args
            l = FrozenRatio(P, Y, P, Q)
            C = PRatio(Y, P, Line(P, Q), l)
            return _eliminate(C, constructions, objective)
        if isinstance(L, PLine):
            R, P, Q = L.args
            l = FrozenRatio(R, Y, P, Q)
            C = PRatio(Y, R, Line(P, Q), l)
            return _eliminate(C, constructions, objective)
    if isinstance(C, Midpoint):
        Y, L = C.args
        if isinstance(L, Line):
            U, V = L.args
            C = LRatio(Y, Line(U, V), Rational(1, 2))
            return _eliminate(C, constructions, objective)
    return objective


def _eliminate(C, constructions, objective):
    while True:
        old = objective

        objective = _substitution_rule(_quadrilateral_area(objective))(objective)
        objective = _substitution_rule(_simplify_area(objective))(objective)
        objective = _substitution_rule(_simplify_ratio(objective))(objective)
        objective = _substitution_rule(_uniformize_area(objective))(objective)

        objective = _eliminate_area_lratio(C, constructions, objective)
        objective = _eliminate_area_pratio(C, constructions, objective)
        objective = _eliminate_area_inter_line_line(C, constructions, objective)
        objective = _eliminate_area_inter_pline_line(C, constructions, objective)
        objective = _eliminate_area_inter_pline_pline(C, constructions, objective)

        objective = _eliminate_ratio_lratio(C, constructions, area_method_affine, objective)
        objective = _eliminate_ratio_pratio(C, constructions, area_method_affine, objective)
        objective = _eliminate_ratio_inter_line_line(C, constructions, area_method_affine, objective)
        objective = _eliminate_ratio_inter_pline_line(C, constructions, area_method_affine, objective)
        objective = _eliminate_ratio_inter_pline_pline(C, constructions, area_method_affine, objective)

        objective = _eliminate_other_constructions(C, constructions, objective)

        objective = _cancel(objective)

        new = objective
        if old == new:
            break
    return objective


def area_method_affine(constructions, objective, *, O=None, U=None, V=None, prove=None):
    constructions = tuple(constructions)
    prove = _auto_option_prove(objective, prove)
    objective = _normalize_predicate_affine(objective)

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove:
            assertion = _degenerate_construction(C)
            if area_method_affine(constructions[:i], assertion, prove=True) is S.true:
                return S.true

        objective = _eliminate(C, constructions[:i], objective)

        Y = C.args[0]
        for G in _geometric_quantities(objective):
            if G.has(Y):
                raise NotImplementedError(f"The elimination step for {Y} in {C} is not properly implemented")

    O, U, V = _auto_coordinates_skew(objective, O, U, V)
    subs = _area_coordinates(O, U, V, objective)
    subs = _apply_to_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _cancel(objective)

    if prove and objective is not S.true:
        objective = S.false
    return objective


def _simplify(objective):
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _substitution_rule(_simplify_ratio(objective))(objective)
    objective = _substitution_rule(_uniformize_area(objective))(objective)
    objective = _cancel(objective)
    return objective
