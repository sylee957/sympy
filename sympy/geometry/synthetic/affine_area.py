from sympy.geometry.synthetic.common import (
    _geometric_quantities, match_ABY)
from sympy.core.singleton import S
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryLine as Line,
    SyntheticGeometryIntersection as Intersection
)
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area


def _area_lratio(Y, P, Q, l, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $LRatio(Y, Line(P, Q), \lambda)$

    Explanation
    ===========

    If $Y$ is a point introduced by $LRatio(Y, Line(P, Q), \lambda)$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \lambda \mathcal{S}_{A, B, Q} +
        (1 - \lambda) \mathcal{S}_{A, B, P}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)
            subs[G] = l * Area(A, B, Q) + (S.One - l) * Area(A, B, P)
    return subs


def _area_pratio(C, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $PRatio(Y, R, P, Q, \lambda)$

    Explanation
    ===========

    If $Y$ is a point introduced by $PRatio(Y, R, P, Q, \lambda)$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \mathcal{S}_{A, B, R} + \lambda \mathcal{S}_{A, P, B, Q}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and isinstance(C, PRatio):
            Y, R, L, l = C.args
            if isinstance(L, Line):
                P, Q = L.args
                if Y in G.args and len(G.args) == 3:
                    A, B, Y = match_ABY(G, Y)
                    subs[G] = Area(A, B, R) + l * Area(A, P, B, Q)
    return subs


def _area_inter_line_line(C, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $Intersection(Y, Line(P, Q), Line(U, V))$

    Explanation
    ===========

    If $Y$ is a point introduced by
    $Intersection(Y, Line(P, Q), Line(U, V))$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \frac{\mathcal{S}_{P, U, V} \mathcal{S}_{A, B, Q} +
        \mathcal{S}_{Q, V, U} \mathcal{S}_{A, B, P}}
        {\mathcal{S}_{P, U, Q, V}}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and isinstance(C, Intersection):
            Y, L1, L2 = C.args
            if isinstance(L1, Line) and isinstance(L2, Line):
                P, Q = L1.args
                U, V = L2.args
                if Y in G.args and len(G.args) == 3:
                    A, B, Y = match_ABY(G, Y)
                    subs[G] = (Area(P, U, V) * Area(A, B, Q) + Area(Q, V, U) * Area(A, B, P)) / Area(P, U, Q, V)
    return subs


def _area_inter_pline_line(C, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $Intersection(Y, PLine(R, P, Q), Line(U, V))$

    Explanation
    ===========

    If $Y$ is a point introduced by
    $Intersection(Y, PLine(R, P, Q), Line(U, V))$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \frac{\mathcal{S}_{P, U, Q, R} \mathcal{S}_{A, B, V} -
        \mathcal{S}_{P, V, Q, R} \mathcal{S}_{A, B, U}}
        {\mathcal{S}_{P, U, Q, V}}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and isinstance(C, Intersection):
            Y, L1, L2 = C.args

            if isinstance(L1, Line) and isinstance(L2, PLine):
                L1, L2 = L2, L1

            if isinstance(L1, PLine) and isinstance(L2, Line):
                R, P, Q = L1.args
                U, V = L2.args
                if Y in G.args and len(G.args) == 3:
                    A, B, Y = match_ABY(G, Y)
                    subs[G] = (Area(P, U, Q, R) * Area(A, B, V) - Area(P, V, Q, R) * Area(A, B, U)) / Area(P, U, Q, V)
    return subs


def _area_inter_pline_pline(C, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $Intersection(Y, PLine(R, P, Q), PLine(W, U, V))$

    Explanation
    ===========

    If $Y$ is a point introduced by
    $Intersection(Y, PLine(R, P, Q), PLine(W, U, V))$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \frac{\mathcal{S}_{P, W, Q, R}}{\mathcal{S}_{P, U, Q, V}}
        \mathcal{S}_{A, U, B, V} + \mathcal{S}_{A, B, W}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and isinstance(C, Intersection):
            Y, L1, L2 = C.args
            if isinstance(L1, PLine) and isinstance(L2, PLine):
                R, P, Q = L1.args
                W, U, V = L2.args
                if Y in G.args and len(G.args) == 3:
                    A, B, Y = match_ABY(G, Y)
                    subs[G] = Area(P, W, Q, R) / Area(P, U, Q, V) * Area(A, U, B, V) + Area(A, B, W)
    return subs
