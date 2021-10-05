from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_linear
from sympy.geometry.synthetic.common import _match_quadratic
from sympy.geometry.synthetic.common import match_AYCD
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.core.singleton import S


def _linear_ARatio(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $ARatio(Y, O, U, V, r_O, r_U, r_V)$.

    Explanation
    ===========

    Let $G(Y)$ be either

    - $\mathcal{S}_{A, B, Y}$,
    - $\mathcal{S}_{A, B, C, Y}$
    - $\mathcal{P}_{A, B, Y}$,
    - $\mathcal{P}_{A, B, C, Y}$

    then

    .. math::
        G(Y) = r_O G(O) + r_U G(U) + r_V G(V)

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, O, U, V, r_O, r_U, r_V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue

        subs[G] = r_O*_G(O) + r_U*_G(U) + r_V*_G(V)
        subs[G] = subs[G].doit()
    return subs


def _quadratic_ARatio(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $ARatio(Y, O, U, V, r_O, r_U, r_V)$.

    Explanation
    ===========

    Let $Q(Y)$ be $\mathcal{P}_{A, Y, B}$ then

    .. math::
        Q(Y) = r_O Q(O) + r_U Q(U) + r_V Q(V)
        - r_O r_V \mathcal{P}_{OVO}
        - r_O r_U \mathcal{P}_{OUO}
        - r_U r_V \mathcal{P}_{UVU}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, O, U, V, r_O, r_U, r_V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _Q = _match_quadratic(G, Y)
        if _Q is None:
            continue

        subs[G] = (
            r_O*_Q(O) + r_U*_Q(U) + r_V*_Q(V)
            - r_O*r_V*Pythagoras(O, V, O)
            - r_O*r_U*Pythagoras(O, U, O)
            - r_U*r_V*Pythagoras(U, V, U)
        )
        subs[G] = subs[G].doit()
    return subs


def _ratio_ARatio(C, objective, prove):
    r"""Eliminate the point $Y$ from the construction
    $ARatio(Y, O, U, V, r_O, r_U, r_V)$.

    Explanation
    ===========

    .. math::
        \frac{\overline{DY}}{\overline{EF}} =
        \begin{cases}
        \frac{r_U \mathcal{S}_{ODU} + r_V \mathcal{S}_{ODV}}
        {\mathcal{S}_{OEDF}}
        \text{ if } O, D, Y \text{ not collinear} \\
        \frac{r_O \mathcal{S}_{UDO} + r_V \mathcal{S}_{UDV}}
        {\mathcal{S}_{UEDF}}
        \text{ if } U, D, Y \text{ not collinear} \\
        \frac{r_O \mathcal{S}_{VDO} + r_U \mathcal{S}_{VDU}}
        {\mathcal{S}_{VEDF}}
        \text{ if } V, D, Y \text{ not collinear} \\
        \end{cases}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, O, U, V, r_O, r_U, r_V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, D, Y, E, F = match_AYCD(G, Y)
            if prove(Collinear(O, D, Y)) is S.true:
                if prove(Collinear(U, D, Y)) is S.true:
                    subs[G] = (r_O*Area(V, D, O) + r_U*Area(V, D, U)) / Area(V, E, D, F)
                else:
                    subs[G] = (r_O*Area(U, D, O) + r_V*Area(U, D, V)) / Area(U, E, D, F)
            else:
                subs[G] = (r_U*Area(O, D, U) + r_V*Area(O, D, V)) / Area(O, E, D, F)

            if reciprocal:
                subs[G] = 1 / subs[G]
            subs[G] = subs[G].doit()
    return subs
