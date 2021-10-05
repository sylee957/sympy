from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_quadratic
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras


def _quadratic_ECS1(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $Inter(Y, Line(U, V), Line(P, Q))$.

    Explanation
    ===========

    Let $Q(Y)$ be $\mathcal{P}_{A, Y, B}$ then

    .. math::
        Q(Y) =
        \frac{\mathcal{S}_{U, P, Q}}{\mathcal{S}_{U, P, V, Q}} Q(V) -
        \frac{\mathcal{S}_{V, P, Q}}{\mathcal{S}_{U, P, V, Q}} Q(U) +
        \frac{\mathcal{S}_{U, P, Q}}{\mathcal{S}_{U, P, V, Q}}
        \frac{\mathcal{S}_{V, P, Q}}{\mathcal{S}_{U, P, V, Q}}
        \mathcal{P}_{U, V, U}

    Notes
    =====

    The formula in [2]_ has some errors.

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.

    .. [2] Quaresma, Pedro. (2021). The Area Method,
       Rigorous Proofs of Lemmas in Hilbert's Style Axiom System.
    """
    Y, U, V, P, Q = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _Q = _match_quadratic(G, Y)
        if _Q is None:
            continue

        UYUV = Area(U, P, Q) / Area(U, P, V, Q)
        YVUV = -Area(V, P, Q) / Area(U, P, V, Q)

        subs[G] = UYUV*_Q(V) + YVUV*_Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
        subs[G] = subs[G].doit()
    return subs


def _quadratic_ECS2(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $Foot(Y, P, U, V)$.

    Explanation
    ===========

    Let $Q(Y)$ be $\mathcal{P}_{A, Y, B}$ then

    .. math::
        Q(Y) =
        \frac{\mathcal{P}_{P, U, V}}{\mathcal{P}_{U, V, U}} Q(V) +
        \frac{\mathcal{P}_{P, V, U}}{\mathcal{P}_{U, V, U}} Q(U) -
        \frac{\mathcal{P}_{P, U, V} \mathcal{P}_{P, V, U}}
        {\mathcal{P}_{U, V, U}}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.

    .. [2] Quaresma, Pedro. (2021). The Area Method,
       Rigorous Proofs of Lemmas in Hilbert's Style Axiom System.
    """
    Y, P, U, V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _Q = _match_quadratic(G, Y)
        if _Q is None:
            continue

        UYUV = Pythagoras(P, U, V) / Pythagoras(U, V, U)
        YVUV = Pythagoras(P, V, U) / Pythagoras(U, V, U)

        subs[G] = UYUV*_Q(V) + YVUV*_Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
        subs[G] = subs[G].doit()
    return subs


def _quadratic_ECS3(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $PRatio(Y, W, U, V, r)$.

    Explanation
    ===========

    Let $Q(Y)$ be $\mathcal{P}_{A, Y, B}$ then

    .. math::
        Q(Y) = Q(W) + r (Q(V) - Q(U) + 2 \mathcal{P}_{W, U, V})
        - r (1 - r) \mathcal{P}_{U, V, U}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.

    .. [2] Quaresma, Pedro. (2021). The Area Method,
       Rigorous Proofs of Lemmas in Hilbert's Style Axiom System.
    """
    Y, W, U, V, l = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _G = _match_quadratic(G, Y)
        if _G is None:
            continue
        subs[G] = _G(W) + l*(_G(V) - _G(U) + 2*Pythagoras(W, U, V)) - l*(1 - l)*Pythagoras(U, V, U)
        subs[G] = subs[G].doit()
    return subs
