from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_linear
from sympy.geometry.synthetic.common import _match_quadratic
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.core.singleton import S
from sympy.geometry.synthetic.common import match_AYCD
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear


def _linear_ECS8(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $Inter(Y, Line(U, V), Circle(O, U))$.

    Explanation
    ===========

    Let $G(Y)$ be either

    - $\mathcal{S}_{A, B, Y}$,
    - $\mathcal{S}_{A, B, C, Y}$
    - $\mathcal{P}_{A, B, Y}$,
    - $\mathcal{P}_{A, B, C, Y}$

    then

    .. math::
        \frac{\overline{U, Y}}{\overline{U, V}} =
        \frac{\mathcal{P}_{U, P, Q} - \frac{\mathcal{P}_{P, Q, P}}{2}}
        {\mathcal{P}_{U, P, V, Q}}

    .. math::
        \frac{\overline{Y, V}}{\overline{U, V}} =
        -\frac{\mathcal{P}_{V, P, Q} - \frac{\mathcal{P}_{P, Q, P}}{2}}
        {\mathcal{P}_{U, P, V, Q}}

    .. math::
        G(Y) =
        \frac{\overline{U, Y}}{\overline{U, V}} G(V) +
        \frac{\overline{Y, V}}{\overline{U, V}} G(U)

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
    Machine Proofs in Geometry: Automated Production of Readable Proofs
    for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, U, V, O = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _G = _match_linear(G, Y)
        if _G is None:
            continue

        UYUV = 2 * Pythagoras(O, U, V) / Pythagoras(U, V, U)
        YVUV = (Pythagoras(O, V, O) - Pythagoras(O, U, O)) / Pythagoras(U, V, U)

        subs[G] = UYUV * _G(V) + YVUV * _G(U)
        subs[G] = subs[G].doit()
    return subs


def _quadratic_ECS8(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $Inter(Y, Line(U, V), Circle(O, U))$.

    Explanation
    ===========

    Let $Q(Y)$ be $\mathcal{P}_{A, Y, B}$ then

    .. math::
        \frac{\overline{U, Y}}{\overline{U, V}} =
        2 \frac{\mathcal{P}_{O, U, V}}{\mathcal{P}_{U, V, U}}

    .. math::
        \frac{\overline{Y, V}}{\overline{U, V}} =
        \frac{\mathcal{P}_{O, V, O} - \mathcal{P}_{O, U, O}}
        {\mathcal{P}_{U, V, U}}

    .. math::
        Q(Y) =
        \frac{\overline{U, Y}}{\overline{U, V}} Q(V) +
        \frac{\overline{U, Y}}{\overline{U, V}} Q(U) -
        \frac{\overline{U, Y}}{\overline{U, V}}
        \frac{\overline{U, Y}}{\overline{U, V}}
        \mathcal{P}_{U, V, U}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, U, V, O = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        _Q = _match_quadratic(G, Y)
        if _Q is None:
            continue

        UYUV = 2 * Pythagoras(O, U, V) / Pythagoras(U, V, U)
        YVUV = (Pythagoras(O, V, O) - Pythagoras(O, U, O)) / Pythagoras(U, V, U)

        subs[G] = UYUV*_Q(V) + YVUV*_Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
        subs[G] = subs[G].doit()
    return subs


def _ratio_ECS8(C, objective, prove):
    r"""Eliminate the point $Y$ from the constructions

    - Inter(Y, Line(U, V), Cir(O, U))

    Explanation
    ===========

    Let $Q(Y)$ be $\mathcal{P}_{A, Y, B}$ then

    .. math::
        \frac{\overline{D, Y}}{\overline{E, F}} =
        \begin{cases}
        \frac{\frac{\overline{D, U}}{\overline{U, V}} +
        \frac{\overline{U, Y}}{\overline{U, V}}}
        {\frac{\overline{E, F}}{\overline{U, V}}}
        \text{ if } D, U, V \text{collinear} \\
        \frac{\mathcal{S}_{D, U, V}}{\mathcal{S}_{E, U, F, V}}
        \text{ otherwise }
        \end{cases}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, U, V, O = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, D, Y, E, F = match_AYCD(G, Y)
            assertion = prove(Collinear(D, U, V))

            UYUV = 2 * Pythagoras(O, U, V) / Pythagoras(U, V, U)
            if assertion is S.true:
                subs[G] = (Ratio(D, U, U, V) + UYUV) / Ratio(E, F, U, V)
            else:
                subs[G] = Area(D, U, V) / Area(E, U, F, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
            subs[G] = subs[G].doit()
    return subs
