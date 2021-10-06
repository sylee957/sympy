from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_linear_area_3
from sympy.geometry.synthetic.common import _match_linear_pythagoras_3
from sympy.geometry.synthetic.common import _match_quadratic_pythagoras_3
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras


def _tratio_area(Y, P, Q, l, objective):
    r"""Eliminate the point $Y$ from the construction
    $TRatio(Y, Line(P, Q), \lambda)$.

    Explanation
    ===========

    .. math::
        \mathcal{S}_{A, B, Y} =
        \mathcal{S}_{A, B, P} -
        \frac{\lambda}{4} \mathcal{P}_{P, A, Q, B}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if not isinstance(G, Area):
            continue
        if not len(G.args) == 3:
            continue

        A, B, C = G.args
        match = _match_linear_area_3(A, B, C, Y)
        if match is None:
            continue

        A, B, Y = match
        subs[G] = Area(A, B, P) - l / 4 * Pythagoras(P, A, Q, B)
    return subs


def _tratio_pythagoras(Y, P, Q, l, objective):
    r"""Eliminate the point $Y$ from the construction
    $TRatio(Y, Line(P, Q), \lambda)$.

    Explanation
    ===========

    .. math::
        \mathcal{P}_{A, B, Y} =
        \mathcal{P}_{A, B, P} -
        4 \lambda \mathcal{S}_{P, A, Q, B}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if not isinstance(G, Pythagoras):
            continue
        if not len(G.args) == 3:
            continue

        A, B, C = G.args
        match = _match_linear_pythagoras_3(A, B, C, Y)
        if match is None:
            continue

        A, B, Y = match
        subs[G] = Pythagoras(A, B, P) - 4 * l * Area(P, A, Q, B)
    return subs


def _tratio_quadratic(Y, P, Q, l, objective):
    r"""Eliminate the point $Y$ from the construction
    $TRatio(Y, Line(P, Q), \lambda)$.

    Explanation
    ===========

    .. math::
        \mathcal{P}_{A, Y, B} =
        \mathcal{P}_{A, P, B} +
        r^2 \mathcal{P}_{P, Q, P} -
        4 \lambda (\mathcal{S}_{A, P, Q} + \mathcal{S}_{B, P, Q})

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if not isinstance(G, Pythagoras):
            continue
        if not len(G.args) == 3:
            continue

        A, B, C = G.args
        match = _match_quadratic_pythagoras_3(A, B, C, Y)
        if match is None:
            continue

        A, B, Y = match
        subs[G] = (
            Pythagoras(A, P, B) + l**2 * Pythagoras(P, Q, P) -
            4*l*(Pythagoras(A, P, Q) + Pythagoras(B, P, Q))
        )
    return subs
