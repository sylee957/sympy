from sympy.core.singleton import S
from sympy.core.symbol import Dummy
from sympy.core.numbers import Integer
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometryFrozenSignedRatio as FrozenRatio
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryBLine as BLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryTLine as TLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircle as Circle
from sympy.geometry.synthetic.degenerate import _degenerate_construction
from sympy.geometry.synthetic.options import _auto_coordinates_orthogonal, _auto_option_prove
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_plane
from sympy.geometry.synthetic.simplify import _cancel
from sympy.geometry.synthetic.common import _substitution_rule
from sympy.geometry.synthetic.common import _quadrilateral_area
from sympy.geometry.synthetic.common import _quadrilateral_pythagoras
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _simplify_pythagoras
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
from sympy.geometry.synthetic.common import match_AYCD


def _ratio_pratio(Y, R, P, Q, l, constructions, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method_plane(constructions, Collinear(A, R, Y))
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
            assertion = area_method_plane(constructions, Collinear(A, U, V))
            if assertion is S.true:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_foot(Y, P, U, V, constructions, objective):
    r"""
    .. math::
        \frac{\overline{D, Y}}{\overline{E, F}} =
        \begin{cases}
        \frac{\mathcal{P}_{P, E, D, F}}{\mathcal{P}_{E, F, E}}
        \text{ if } D, U, V \text{ collinear} \\
        \frac{\mathcal{S}_{D, U, V}}{\mathcal{S}_{E, U, F, V}}
        \text{ otherwise }
        \end{cases}

    Notes
    =====

    Although the original implementation in [1]_ takes account of an
    additional assumption $D \ne U$, we ignore this
    side condition because it is redundant.

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, D, Y, E, F = match_AYCD(G, Y)
            assertion = area_method_plane(constructions, Collinear(D, U, V))
            if assertion is S.true:
                subs[G] = Pythagoras(P, E, D, F) / Pythagoras(E, F, E)
            else:
                subs[G] = Area(D, U, V) / Area(E, U, F, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_tratio(Y, P, Q, r, constructions, objective):
    r"""

    .. math::
        \frac{\overline{D, Y}}{\overline{E, F}} =
        \begin{cases}
        \frac{\mathcal{S}_{D, P, Q} - \frac{r}{4} \mathcal{P}_{P, Q, P}}{\mathcal{P}_{E, P, F, Q}}
        \text{ if } D, P, Y \text{ collinear} \\
        \frac{\mathcal{P}_{D, P, Q}}{\mathcal{P}_{E, P, F, Q}}
        \text{ otherwise }
        \end{cases}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, D, Y, E, F = match_AYCD(G, Y)
            assertion = area_method_plane(constructions, Collinear(D, P, Y))
            if assertion is S.true:
                subs[G] = (Area(D, P, Q) - r / 4 * Pythagoras(P, Q, P)) / Pythagoras(E, P, F, Q)
            else:
                subs[G] =  Pythagoras(D, P, Q) / Pythagoras(E, P, F, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


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


def _eliminate_ratio_pratio(C, constructions, objective):
    match = _match_pratio(C)
    if match is None:
        return objective
    Y, W, U, V, l = match
    subs = _ratio_pratio(Y, W, U, V, l, constructions, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_inter_line_line(C, constructions, objective):
    match = _match_inter_line_line(C)
    if match is None:
        return objective
    Y, U, V, P, Q = match
    subs = _ratio_inter_line_line(Y, U, V, P, Q, constructions, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_foot(C, constructions, objective):
    match = _match_foot(C)
    if match is None:
        return objective
    Y, P, U, V = match
    subs = _ratio_foot(Y, P, U, V, constructions, objective)
    subs = _eliminate_image(C, constructions, subs)
    objective = _substitution_rule(subs)(objective)
    return objective


def _eliminate_ratio_tratio(C, constructions, objective):
    match = _match_tratio(C)
    if match is None:
        return objective
    Y, P, Q, l = match
    subs = _ratio_tratio(Y, P, Q, l, constructions, objective)
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


def _rewrite_and_eliminate_on(C, constructions, objective):
    r"""Eliminate ``On(Y, L)`` using more elementary constructions.

    The supported form are

    - ``On(Y, Line(U, V))``
    - ``On(Y, PLine(W, U, V))``
    - ``On(Y, TLine(W, U, V))``
    - ``On(Y, BLine(U, V))``
    - ``On(Y, (U, V))``
    """
    if isinstance(C, On):
        Y, L = C.args
        if isinstance(L, Line):
            U, V = L.args
            C = PRatio(Y, U, Line(U, V), FrozenRatio(U, Y, U, V))
            return _eliminate(C, constructions, objective)

        C = lambda L: On(Y, L)
        if isinstance(L, PLine):
            W, U, V = L.args
            return _auxiliary_points_pline(C, constructions, objective, W, U, V)
        if isinstance(L, TLine):
            W, U, V = L.args
            return _auxiliary_points_tline(C, constructions, objective, W, U, V)
        if isinstance(L, BLine):
            U, V = L.args
            return _auxiliary_points_bline(constructions, objective, U, V)
        if isinstance(L, Circle):
            O, P = L.args
            Q = Dummy('\$Q')
            C = Intersection(Y, Line(P, Q), Circle(O, P))
            return _eliminate(C, constructions, objective)

    return objective


def _rewrite_and_eliminate_inter(C, constructions, objective):
    r"""Eliminate ``Inter(Y, L1, L1)`` using more elementary constructions.

    L1, L2 must be ``PLine, TLine, BLine, Circle``
    """
    if isinstance(C, Intersection):
        Y, L1, L2 = C.args

        if isinstance(L1, PLine):
            C = lambda L: Intersection(Y, L, L2)
            W, U, V = L1.args
            return _auxiliary_points_pline(C, constructions, objective, W, U, V)
        elif isinstance(L1, TLine):
            C = lambda L: Intersection(Y, L, L2)
            W, U, V = L1.args
            return _auxiliary_points_tline(C, constructions, objective, W, U, V)
        elif isinstance(L1, BLine):
            U, V = L1.args
            return _auxiliary_points_bline(constructions, objective, U, V)

        if isinstance(L2, PLine):
            C = lambda L: Intersection(Y, L1, L)
            W, U, V = L2.args
            return _auxiliary_points_pline(C, constructions, objective, W, U, V)
        elif isinstance(L2, TLine):
            C = lambda L: Intersection(Y, L1, L)
            W, U, V = L2.args
            return _auxiliary_points_tline(C, constructions, objective, W, U, V)
        elif isinstance(L2, BLine):
            U, V = L2.args
            return _auxiliary_points_bline(constructions, objective, U, V)

        if isinstance(L2, Line) and isinstance(L1, Circle):
            return _eliminate(Intersection(Y, L2, L1))

        if isinstance(L1, Line) and isinstance(L2, Circle):
            U, V = L1.args
            O, U = L2.args
            N = Dummy(r'\breve{N}')
            C1 = Foot(N, O, U, V)
            C2 = PRatio(Y, N, N, U, Integer(-1))

            objective = _eliminate(C2, constructions + (C1, C2), objective)
            objective = _eliminate(C1, constructions + (C1), objective)
            return objective

        if isinstance(L1, Circle) and isinstance(C2, Circle):
            O1, P1 = L1.args
            O2, P2 = L2.args
            if P1 == P2:
                P = P1
                C1 = Foot(N, P, Line(O1, O2))
                C2 = PRatio(Y, N, Line(N, P), Integer(-1))

                objective = _eliminate(C2, constructions + (C1, C2), objective)
                objective = _eliminate(C1, constructions + (C1), objective)
                return objective

    return objective


def _rewrite_and_eliminate_midpoint(C, constructions, objective):
    if isinstance(C, Midpoint):
        Y, L = C.args
        if isinstance(L, Line):
            U, V = L.args
            C = PRatio(Y, U, Line(U, V), S.Half)
            return _eliminate(C, constructions, objective)
    return objective


def _auxiliary_points_pline(C, constructions, objective, W, U, V):
    N = Dummy(r'\breve{N}')
    C1 = PRatio(N, W, Line(U, V), Integer(1))
    C2 = C(Line(W, N))

    objective = _eliminate(C2, constructions + (C1, C2), objective)
    objective = _eliminate(C1, constructions + (C1,), objective)
    return objective


def _auxiliary_points_tline(C, constructions, objective, W, U, V):
    assertion = area_method_plane(constructions, Collinear(W, U, V))
    if assertion is S.true:
        N = Dummy(r'\breve{N}')
        C1 = TRatio(N, Line(W, U), Integer(1))
        C2 = C(Line(N, W))

        objective = _eliminate(C2, constructions + (C1, C2), objective)
        objective = _eliminate(C1, constructions + (C1,), objective)
        return objective
    else:
        N = Dummy(r'\breve{N}')
        C1 = Foot(N, W, Line(U, V))
        C2 = C(Line(N, W))

        objective = _eliminate(C2, constructions + (C1, C2), objective)
        objective = _eliminate(C1, constructions + (C1,), objective)
        return objective


def _auxiliary_points_bline(constructions, objective, U, V):
    M = Dummy(r'\breve{M}')
    N = Dummy(r'\breve{N}')
    C1 = Midpoint(M, Line(U, V))
    C2 = TRatio(N, Line(M, U), S.One)

    objective = _eliminate(C2, constructions + (C1, C2), objective)
    objective = _eliminate(C1, constructions + (C1,), objective)
    return objective


def _eliminate(C, constructions, objective):
    while True:
        old = objective

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

        objective = _eliminate_ratio_pratio(C, constructions, objective)
        objective = _eliminate_ratio_inter_line_line(C, constructions, objective)
        objective = _eliminate_ratio_foot(C, constructions, objective)
        objective = _eliminate_ratio_tratio(C, constructions, objective)

        objective = _rewrite_and_eliminate_on(C, constructions, objective)
        objective = _rewrite_and_eliminate_inter(C, constructions, objective)
        objective = _rewrite_and_eliminate_midpoint(C, constructions, objective)

        if _has_unsolved_quadrilateral(C, objective):
            objective = _eliminate_quadrilateral_expand(C, constructions, objective)

        objective = _cancel(objective)

        new = objective
        if old == new:
            break
    return objective


def _apply_area_coordinates(O, U, V, objective):
    objective = _substitution_rule(_quadrilateral_area(objective))(objective)
    objective = _substitution_rule(_quadrilateral_pythagoras(objective))(objective)

    subs = _area_coordinates(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)

    while True:
        old = objective
        subs = _area_coordinates_pythagoras(O, U, V, objective)
        subs = _simplify_image(_simplify, subs)
        objective = _substitution_rule(subs)(objective)
        new = objective
        if old == new:
            break

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
    constructions = tuple(constructions)
    prove = _auto_option_prove(objective, prove)
    objective = _normalize_predicate_plane(objective)

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove:
            assertion = _degenerate_construction(C)
            if area_method_plane(constructions[:i], assertion, prove=True) is S.true:
                return S.true

        objective = _eliminate(C, constructions[:i], objective)

        Y = C.args[0]
        for G in _geometric_quantities(objective):
            if G.has(Y):
                raise NotImplementedError(f"The elimination step for {Y} in {C} is not properly implemented")

    O, U, V = _auto_coordinates_orthogonal(O, U, V)
    objective = _apply_area_coordinates(O, U, V, objective)

    if prove and objective is not S.true:
        objective = S.false
    return objective
