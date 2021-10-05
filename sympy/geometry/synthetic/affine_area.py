from sympy.geometry.synthetic.common import (
    _geometric_quantities, match_ABY)
from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area


def _area_ECS1(C, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $LRatio(Y, P, Q, \lambda)$

    Explanation
    ===========

    If $Y$ is a point introduced by $LRatio(Y, P, Q, \lambda)$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \lambda \mathcal{S}_{A, B, Q} +
        (1 - \lambda) \mathcal{S}_{A, B, P}
    """
    Y, P, Q, l = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)
            subs[G] = l * Area(A, B, Q) + (S.One - l) * Area(A, B, P)
    return subs


def _area_ECS2(C, objective):
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
    Y, P, Q, U, V = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)
            subs[G] = (Area(P, U, V) * Area(A, B, Q) + Area(Q, V, U) * Area(A, B, P)) / Area(P, U, Q, V)
    return subs


def _area_ECS3(C, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $PRatio(Y, R, P, Q, r)$

    Explanation
    ===========

    If $Y$ is a point introduced by $PRatio(Y, R, P, Q, r)$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \mathcal{S}_{A, B, R} + r \mathcal{S}_{A, P, B, Q}
    """
    Y, R, P, Q, l = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)
            subs[G] = Area(A, B, R) + l * Area(A, P, B, Q)
    return subs


def _area_ECS4(C, objective):
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
    Y, U, V, R, P, Q = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)
            subs[G] = (Area(P, U, Q, R) * Area(A, B, V) - Area(P, V, Q, R) * Area(A, B, U)) / Area(P, U, Q, V)
    return subs


def _area_ECS5(C, objective):
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
    Y, R, P, Q, W, U, V = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)
            subs[G] = Area(P, W, Q, R) / Area(P, U, Q, V) * Area(A, U, B, V) + Area(A, B, W)
    return subs
