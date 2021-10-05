from sympy.polys.polytools import cancel
from sympy.core.numbers import Rational
from sympy.core.singleton import S
from sympy.core.relational import Eq, Ne
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometryFrozenSignedRatio as FrozenRatio,
    SyntheticGeometrySignedArea as Area
)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryMidpoint as Midpoint
)
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
from sympy.geometry.synthetic.affine_ratio import (
    _ratio_lratio,
    _ratio_pratio,
    _ratio_inter_line_line,
    _ratio_inter_pline_line,
    _ratio_inter_pline_pline
)
from sympy.geometry.synthetic.area_coordinates import _area_coordinates
from sympy.geometry.synthetic.options import (
    _auto_option_prove,
    _auto_coordinates_skew
)
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_affine
from sympy.geometry.synthetic.degenerate import _degenerate_construction


def _eliminate_image(C, constructions, subs):
    return {k: _eliminate(C, constructions, v) for k, v in subs.items()}


def _simplify_image(simplify, subs):
    return {k: simplify(v) for k, v in subs.items()}


def _eliminate_area_lratio(C, constructions, objective):
    if not isinstance(C, LRatio):
        return objective
    Y, L, r = C.args
    if not isinstance(L, Line):
        return objective
    P, Q = L.args

    subs = _area_lratio(Y, P, Q, r, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate(C, constructions, objective):
    objective = _substitution_rule(_quadrilateral_area(objective))(objective)
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _substitution_rule(_simplify_ratio(objective))(objective)
    objective = _substitution_rule(_uniformize_area(objective))(objective)

    objective = _eliminate_area_lratio(C, constructions, objective)

    subs = _area_pratio(C, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _area_inter_line_line(C, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _area_inter_pline_line(C, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _area_inter_pline_pline(C, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _ratio_lratio(C, constructions, area_method_affine, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _ratio_pratio(C, constructions, area_method_affine, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _ratio_inter_line_line(C, constructions, area_method_affine, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _ratio_inter_pline_line(C, constructions, area_method_affine, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    subs = _ratio_inter_pline_pline(C, constructions, area_method_affine, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

    objective = _simplify(objective)
    return objective


def _normalize_constructions(constructions):
    new = []
    for C in constructions:
        if isinstance(C, On):
            Y, line = C.args
            if isinstance(line, Line):
                P, Q = line.args
                l = FrozenRatio(P, Y, P, Q)
                new.append(PRatio(Y, P, Line(P, Q), l))
                continue
            elif isinstance(line, PLine):
                R, P, Q = line.args
                l = FrozenRatio(R, Y, P, Q)
                new.append(PRatio(Y, R, Line(P, Q), l))
                continue
        if isinstance(C, Midpoint):
            Y, L = C.args
            if isinstance(L, Line):
                U, V = L.args
                new.append(LRatio(Y, Line(U, V), Rational(1, 2)))
            continue
        new.append(C)
    return tuple(new)


def area_method_affine(constructions, objective, *, O=None, U=None, V=None, prove=None):
    prove = _auto_option_prove(objective, prove)
    constructions = _normalize_constructions(constructions)
    objective = _normalize_predicate_affine(objective)

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove:
            assertion = _degenerate_construction(C)
            if area_method_affine(constructions[:i], assertion, prove=True) is S.true:
                return S.true

        while True:
            old = objective
            objective = _eliminate(C, constructions[:i + 1], objective)
            new = objective
            if old == new:
                break

    O, U, V = _auto_coordinates_skew(objective, O, U, V)
    subs = _area_coordinates(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _cancel(objective)

    if prove and objective is not S.true:
        objective = S.false
    return objective


def _cancel(objective):
    if isinstance(objective, (Eq, Ne)):
        return objective.func(cancel(objective.lhs), cancel(objective.rhs))
    return cancel(objective)


def _simplify(objective):
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _substitution_rule(_simplify_ratio(objective))(objective)
    objective = _substitution_rule(_uniformize_area(objective))(objective)
    objective = _cancel(objective)
    return objective
