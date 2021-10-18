from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import match_AYCD
from sympy.geometry.synthetic.common import _match_ratio
from sympy.geometry.synthetic.common import _match_ratio_both


def _ratio_ECS1(C, objective, prove):
    r"""Eliminate $Y$ from Inter(Y, Line(P, Q), Line(U, V))

    .. math::
        \frac{\overline{D, Y}}{\overline{E, Y}} =
        \begin{cases}
        \frac{\mathcal{S}_{D, P, Q}}{\mathcal{S}_{E, P, Q}}
        \text{ if } D, U, V \text{ collinear} \\
        \frac{\mathcal{S}_{D, U, V}}{\mathcal{S}_{E, U, V}}
        \text{ otherwise }
        \end{cases}

    .. math::
        \frac{\overline{D, Y}}{\overline{E, F}} =
        \begin{cases}
        \frac{\mathcal{S}_{D, P, Q}}{\mathcal{S}_{E, P, F, Q}}
        \text{ if } D, U, V \text{ collinear} \\
        \frac{\mathcal{S}_{D, U, V}}{\mathcal{S}_{E, U, F, V}}
        \text{ otherwise }
        \end{cases}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable
       Proofs for Geometry Theorems. 10.1142/9789812798152.

    .. [2] Predrag Janicic, Julien Narboux, Pedro Quaresma.
       The Area Method : a Recapitulation. Journal of Automated
       Reasoning, Springer Verlag, 2012, 48 (4), pp.489-532.
       ⟨10.1007/s10817-010-9209-7⟩. ⟨hal-00426563v2⟩
    """
    Y, P, Q, U, V = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio):
            match = _match_ratio_both(G, Y)
            if match:
                sign, D, E, Y = match
                assertion = prove(Collinear(D, U, V))
                if assertion is S.true:
                    subs[G] = sign * Area(D, P, Q) / Area(E, P, Q)
                else:
                    subs[G] = sign * Area(D, U, V) / Area(E, U, V)
                subs[G] = subs[G].doit()
                continue

            match = _match_ratio(G, Y)
            if match:
                reciprocal, D, Y, E, F = match_AYCD(G, Y)
                assertion = prove(Collinear(D, U, V))
                if assertion is S.true:
                    subs[G] = Area(D, P, Q) / Area(E, P, F, Q)
                else:
                    subs[G] = Area(D, U, V) / Area(E, U, F, V)
                if reciprocal:
                    subs[G] = 1 / subs[G]
                subs[G] = subs[G].doit()
                continue

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
