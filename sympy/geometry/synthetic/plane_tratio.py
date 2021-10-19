from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _match_linear_area_3
from sympy.geometry.synthetic.common import _match_linear_area_4
from sympy.geometry.synthetic.common import _match_linear_pythagoras_3
from sympy.geometry.synthetic.common import _match_linear_pythagoras_4
from sympy.geometry.synthetic.common import _match_quadratic_pythagoras_3
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras


def _area_ECS4(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $TRatio(Y, P, Q, r)$.

    Explanation
    ===========

    .. math::
        \mathcal{S}_{A, B, Y} =
        \mathcal{S}_{A, B, P} -
        \frac{r}{4} \mathcal{P}_{P, A, Q, B}

    .. math::
        \mathcal{S}_{A, B, C, Y} =
        \mathcal{S}_{A, B, C, P} -
        \frac{r}{4} \mathcal{P}_{P, A, Q, C}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, P, Q, r = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if not isinstance(G, Area):
            continue

        if len(G.args) == 3:
            A, B, C = G.args
            match = _match_linear_area_3(A, B, C, Y)
            if match is None:
                continue

            A, B, Y = match
            subs[G] = Area(A, B, P) - r / 4 * Pythagoras(P, A, Q, B)
            subs[G] = subs[G].doit()
        elif len(G.args) == 4:
            A, B, C, D = G.args
            match = _match_linear_area_4(A, B, C, D, Y)
            if match is None:
                continue

            A, B, C, Y = match
            subs[G] = Area(A, B, C, P) - r / 4 * Pythagoras(P, A, Q, C)
            subs[G] = subs[G].doit()
    return subs


def _pythagoras_ECS4(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $TRatio(Y, P, Q, r)$.

    Explanation
    ===========

    .. math::
        \mathcal{P}_{A, B, Y} =
        \mathcal{P}_{A, B, P} -
        4r \mathcal{S}_{P, A, Q, B}

    .. math::
        \mathcal{P}_{A, B, C, Y} =
        \mathcal{P}_{A, B, C, P} -
        4r \mathcal{S}_{P, A, Q, C}

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, P, Q, r = C.args

    subs = {}
    for G in _geometric_quantities(objective):
        if not isinstance(G, Pythagoras):
            continue
        if len(G.args) == 3:
            A, B, C = G.args
            match = _match_linear_pythagoras_3(A, B, C, Y)
            if match is None:
                continue

            A, B, Y = match
            subs[G] = Pythagoras(A, B, P) - 4*r*Area(P, A, Q, B)
            subs[G] = subs[G].doit()
        elif len(G.args) == 4:
            A, B, C, D = G.args
            match = _match_linear_pythagoras_4(A, B, C, D, Y)
            if match is None:
                continue

            A, B, C, Y = match
            subs[G] = Pythagoras(A, B, C, P) - 4*r*Area(P, A, Q, C)
            subs[G] = subs[G].doit()
    return subs


def _quadratic_ECS4(C, objective):
    r"""Eliminate the point $Y$ from the construction
    $TRatio(Y, P, Q, \lambda)$.

    Explanation
    ===========

    .. math::
        \mathcal{P}_{A, Y, B} =
        \mathcal{P}_{A, P, B} +
        r^2 \mathcal{P}_{P, Q, P} -
        4r (\mathcal{S}_{A, P, Q} + \mathcal{S}_{B, P, Q})

    References
    ==========

    .. [1] Chou, Shih-Chun & Gao, Xiao-Shan & Zhang, J.. (1994).
       Machine Proofs in Geometry: Automated Production of Readable Proofs
       for Geometry Theorems. 10.1142/9789812798152.
    """
    Y, P, Q, l = C.args

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
            4*l*(Area(A, P, Q) + Area(B, P, Q))
        )
        subs[G] = subs[G].doit()
    return subs
