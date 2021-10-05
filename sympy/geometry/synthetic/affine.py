from sympy.core.symbol import Dummy
from sympy.polys.polytools import cancel
from sympy.logic.boolalg import Boolean
from sympy.core.basic import Atom
from sympy.core.numbers import Rational
from sympy.core.singleton import S
from sympy.core.relational import Eq, Ne
from sympy.core.compatibility import default_sort_key
from sympy.geometry.synthetic.predicates import (
    SyntheticGeometrySamePoints as SamePoints,
    SyntheticGeometryCollinear as Collinear,
    SyntheticGeometryParallel as Parallel
)
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometrySignedArea as Area,
    SyntheticGeometrySignedRatio as Ratio,
    SyntheticGeometryFrozenSignedRatio as FrozenRatio
)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryMidpoint as Midpoint
)
from sympy.geometry.synthetic.common import (
    _geometric_quantities,
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


def degenerate(C, construction):
    if isinstance(C, LRatio):
        Y, P, Q, l = C.args
        assertion = area_method_affine(construction, SamePoints(P, Q))
        return assertion

    elif isinstance(C, PRatio):
        Y, R, P, Q, l = C.args
        assertion = area_method_affine(construction, SamePoints(P, Q))
        return assertion

    elif isinstance(C, Intersection):
        Y, L1, L2 = C.args
        if isinstance(L1, Line) and isinstance(L2, Line):
            P, Q = L1.args
            U, V = L2.args
            assertion = area_method_affine(construction, Parallel(U, V, P, Q))
            return assertion

        if isinstance(L1, Line) and isinstance(L2, PLine):
            L1, L2 = L2, L1

        if isinstance(L1, PLine) and isinstance(L2, Line):
            R, P, Q = L1.args
            U, V = L2.args
            assertion = area_method_affine(construction, Parallel(U, V, P, Q))
            return assertion

        if isinstance(L1, PLine) and isinstance(L2, PLine):
            R, P, Q = L1.args
            W, U, V = L2.args
            assertion = area_method_affine(construction, Parallel(U, V, P, Q))
            return assertion


def _eliminate_image(C, constructions, subs):
    return {k: _eliminate(C, constructions, v) for k, v in subs.items()}


def _simplify_image(simplify, subs):
    return {k: simplify(v) for k, v in subs.items()}


def _eliminate(C, constructions, objective):
    objective = _substitution_rule(_quadrilateral_area(objective))(objective)
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _substitution_rule(_simplify_ratio(objective))(objective)
    objective = _substitution_rule(_uniformize_area(objective))(objective)

    subs = _area_lratio(C, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)

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


def _normalize_coordinates(O, U, V):
    if O is None:
        O = Dummy('$O')
    if U is None:
        U = Dummy('$U')
    if V is None:
        V = Dummy('$V')
    return O, U, V


def _auto_coordinates(constructions, objective, O, U, V):
    all_points = set()
    for G in _geometric_quantities(objective):
        for point in G.args:
            all_points.add(point)
    constructed_points = set()
    for C in constructions:
        if isinstance(C, LRatio):
            Y, P, Q, _ = C.args
            constructed_points.add(Y)
            all_points.add(Y)
            all_points.add(P)
            all_points.add(Q)
        elif isinstance(C, PRatio):
            Y, R, P, Q, _ = C.args
            constructed_points.add(Y)
            all_points.add(Y)
            all_points.add(P)
            all_points.add(Q)
            all_points.add(R)
        if isinstance(C, Intersection):
            Y, L1, L2 = C.args
            constructed_points.add(Y)
            all_points.add(Y)
            for point in L1.args:
                all_points.add(point)
            for point in L2.args:
                all_points.add(point)
    free_points = all_points.difference(constructed_points)
    free_points = sorted(free_points, key=default_sort_key)

    if not free_points:
        return O, U, V
    if len(free_points) == 1:
        O = free_points
        return O, U, V
    if len(free_points) == 2:
        O, U = free_points
        return O, U, V

    O, U, V, *_ = free_points
    return O, U, V


def _normalize_constructions(constructions):
    new = []
    for C in constructions:
        if isinstance(C, On):
            Y, line = C.args
            if isinstance(line, Line):
                P, Q = line.args
                l = FrozenRatio(P, Y, P, Q)
                new.append(PRatio(Y, P, P, Q, l))
                continue
            elif isinstance(line, PLine):
                R, P, Q = line.args
                l = FrozenRatio(R, Y, P, Q)
                new.append(PRatio(Y, R, P, Q, l))
                continue
        if isinstance(C, Midpoint):
            Y, U, V = C.args
            new.append(LRatio(Y, U, V, Rational(1, 2)))
            continue
        new.append(C)
    return tuple(new)


def _normalize_proof_objective(objective):
    if isinstance(objective, Collinear):
        A, B, C = objective.args
        return Eq(Area(A, B, C), S.Zero)
    if isinstance(objective, Parallel):
        A, B, C, D = objective.args
        return Eq(Area(A, B, C) - Area(A, B, D), S.Zero)
    if isinstance(objective, SamePoints):
        A, B = objective.args
        X, Y = Dummy('X'), Dummy('Y')
        return Eq(Ratio(A, B, X, Y), S.Zero)
    if not isinstance(objective, Atom):
        return objective.func(*(_normalize_proof_objective(arg) for arg in objective.args))
    return objective


def _normalize_argument_prove(objective, prove):
    if prove is None:
        prove = False
        if isinstance(objective, Boolean):
            prove = True
    return prove


def area_method_affine(constructions, objective, *, O=None, U=None, V=None, prove=None):
    prove = _normalize_argument_prove(objective, prove)
    constructions = _normalize_constructions(constructions)
    objective = _normalize_proof_objective(objective)
    O, U, V = _normalize_coordinates(O, U, V)
    O, U, V = _auto_coordinates(constructions, objective, O, U, V)

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove and degenerate(C, constructions[:i]) is S.true:
            return S.true

        while True:
            old = objective
            objective = _eliminate(C, constructions[:i + 1], objective)
            new = objective
            if old == new:
                break

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
