from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import match_AYCD


def _ratio_ECS1(C, objective, prove):
    Y, P, Q, U, V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Collinear(A, U, V))
            if assertion is S.true:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
            subs[G] = subs[G].doit()
    return subs


def _ratio_ECS2(C, objective, prove):
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
    Y, P, U, V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, D, Y, E, F = match_AYCD(G, Y)
            assertion = prove(Collinear(D, U, V))
            if assertion is S.true:
                subs[G] = Pythagoras(P, E, D, F) / Pythagoras(E, F, E)
            else:
                subs[G] = Area(D, U, V) / Area(E, U, F, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
            subs[G] = subs[G].doit()
    return subs


def _ratio_ECS3(C, objective, prove):
    Y, R, P, Q, l = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Collinear(A, R, Y))
            if assertion is S.true:
                subs[G] = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
            subs[G] = subs[G].doit()
    return subs


def _ratio_ECS4(C, objective, prove):
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
    Y, P, Q, r = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, D, Y, E, F = match_AYCD(G, Y)
            assertion = prove(Collinear(D, P, Y))
            if assertion is S.true:
                subs[G] = (Area(D, P, Q) - r / 4 * Pythagoras(P, Q, P)) / Pythagoras(E, P, F, Q)
            else:
                subs[G] =  Pythagoras(D, P, Q) / Pythagoras(E, P, F, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
            subs[G] = subs[G].doit()
    return subs
