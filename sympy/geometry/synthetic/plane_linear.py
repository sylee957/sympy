from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_linear
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras


def _linear_ECS1(C, objective):
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
    Y, U, V, P, Q = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue

        UYUV = Area(U, P, Q) / Area(U, P, V, Q)
        YVUV = -Area(V, P, Q) / Area(U, P, V, Q)

        subs[G] = UYUV * _G(V) + YVUV * _G(U)
        subs[G] = subs[G].doit()
    return subs


def _linear_ECS2(C, objective):
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
    Y, P, U, V = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue

        UYUV = Pythagoras(P, U, V) / Pythagoras(U, V, U)
        YVUV = Pythagoras(P, V, U) / Pythagoras(U, V, U)

        subs[G] = UYUV * _G(V) + YVUV * _G(U)
        subs[G] = subs[G].doit()
    return subs


def _linear_ECS3(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $PRatio(Y, W, U, V, r)$.

    Explanation
    ===========

    Let $G(Y)$ be either

    - $\mathcal{S}_{A, B, Y}$,
    - $\mathcal{S}_{A, B, C, Y}$
    - $\mathcal{P}_{A, B, Y}$,
    - $\mathcal{P}_{A, B, C, Y}$

    .. math::
        G(Y) = G(W) + r (G(V) - G(U))

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
    Y, W, U, V, l = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue
        subs[G] = _G(W) + l * (_G(V) - _G(U))
        subs[G] = subs[G].doit()
    return subs
