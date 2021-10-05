from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_linear
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot


def _linear_pratio(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $PRatio(Y, W, U, V, \lambda)$.

    Explanation
    ===========

    Let $G(Y)$ be either

    - $\mathcal{S}_{A, B, Y}$,
    - $\mathcal{S}_{A, B, C, Y}$
    - $\mathcal{P}_{A, B, Y}$,
    - $\mathcal{P}_{A, B, C, Y}$

    .. math::
        G(Y) = G(W) + \lambda (G(V) - G(U))

    Notes
    =====

    Although the original **Lemma 3.22** in [1]_ adds an additional
    side condition if $W, U, V$ are collinear, we are not using that
    because it is redundant.

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    if not isinstance(C, PRatio):
        return subs

    Y, W, L, l = C.args
    if not isinstance(L, Line):
        return subs

    U, V = L.args
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue
        subs[G] = _G(W) + l * (_G(V) - _G(U))
    return subs


def _linear_inter_line_line(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $Inter(Y, Line(U, V), Line(P, Q))$.

    Explanation
    ===========

    Let $G(Y)$ be either

    - $\mathcal{S}_{A, B, Y}$,
    - $\mathcal{S}_{A, B, C, Y}$
    - $\mathcal{P}_{A, B, Y}$,
    - $\mathcal{P}_{A, B, C, Y}$

    .. math::
        G(Y) =
        \frac{\mathcal{S}_{U, P, Q} G(V) - \mathcal{S}_{V, P, Q} G(U)}
        {\mathcal{S}_{U, P, V, Q}}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    if not isinstance(C, Intersection):
        return subs

    Y, L1, L2 = C.args
    if not isinstance(L1, Line):
        return subs
    if not isinstance(L2, Line):
        return subs

    U, V = L1.args
    P, Q = L2.args
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue
        subs[G] = (Area(U, P, Q) * _G(V) - Area(V, P, Q) * _G(U)) / Area(U, P, V, Q)
    return subs


def _linear_foot(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $Foot(Y, P, U, V)$.

    Explanation
    ===========

    Let $G(Y)$ be either

    - $\mathcal{S}_{A, B, Y}$,
    - $\mathcal{S}_{A, B, C, Y}$
    - $\mathcal{P}_{A, B, Y}$,
    - $\mathcal{P}_{A, B, C, Y}$

    .. math::
        G(Y) =
        \frac{\mathcal{P}_{P, U, V} G(V) + \mathcal{P}_{P, V, U} G(U)}
        {\mathcal{P}_{U, V, U}}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    if not isinstance(C, Foot):
        return subs

    Y, P, L = C.args
    if not isinstance(L, Line):
        return subs

    U, V = L.args
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue
        subs[G] = (Pythagoras(P, U, V) * _G(V) + Pythagoras(P, V, U) * _G(U)) / Pythagoras(U, V, U)
    return subs
