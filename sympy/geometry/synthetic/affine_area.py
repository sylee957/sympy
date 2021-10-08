from sympy.geometry.synthetic.common import (
    _compress, match_ABY)
from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.affine_match import _match_lratio
from sympy.geometry.synthetic.affine_match import _match_pratio
from sympy.geometry.synthetic.affine_match import _match_inter_line_line
from sympy.geometry.synthetic.affine_match import _match_inter_pline_line
from sympy.geometry.synthetic.affine_match import _match_inter_pline_pline
from sympy.geometry.synthetic.common import _inject_new_variables_and_eliminate


def _eliminate_area_lratio(C, constructions, domain, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $LRatio(Y, Line(P, Q), \lambda)$

    Explanation
    ===========

    If $Y$ is a point introduced by $LRatio(Y, Line(P, Q), \lambda)$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \lambda \mathcal{S}_{A, B, Q} +
        (1 - \lambda) \mathcal{S}_{A, B, P}
    """
    match = _match_lratio(C)
    if match is None:
        return domain, objective
    Y, P, Q, r = match
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)

            eliminant = r * Area(A, B, Q) + (S.One - r) * Area(A, B, P)
            eliminant = eliminant.doit()

            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _eliminate_area_pratio(C, constructions, domain, objective):
    r"""Eliminate $\mathcal{S}_{A, B, Y}$ where $Y$ is constructed from
    $PRatio(Y, R, Line(P, Q), \lambda)$

    Explanation
    ===========

    If $Y$ is a point introduced by $PRatio(Y, R, Line(P, Q), \lambda)$,

    .. math::
        \mathcal{S}_{A, B, Y} =
        \mathcal{S}_{A, B, R} + \lambda \mathcal{S}_{A, P, B, Q}
    """
    match = _match_pratio(C)
    if match is None:
        return domain, objective
    Y, R, P, Q, r = match
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)

            eliminant = Area(A, B, R) + r * Area(A, P, B, Q)
            eliminant = eliminant.doit()

            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _eliminate_area_inter_line_line(C, constructions, domain, objective):
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
    match = _match_inter_line_line(C)
    if match is None:
        return domain, objective
    Y, P, Q, U, V = match
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)

            eliminant = (Area(P, U, V) * Area(A, B, Q) + Area(Q, V, U) * Area(A, B, P)) / Area(P, U, Q, V)
            eliminant = eliminant.doit()

            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _eliminate_area_inter_pline_line(C, constructions, domain, objective):
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
    match = _match_inter_pline_line(C)
    if match is None:
        return domain, objective
    Y, R, P, Q, U, V = match
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)

            eliminant = (Area(P, U, Q, R) * Area(A, B, V) - Area(P, V, Q, R) * Area(A, B, U)) / Area(P, U, Q, V)
            eliminant = eliminant.doit()

            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _eliminate_area_inter_pline_pline(C, constructions, domain, objective):
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
    match = _match_inter_pline_pline(C)
    if match is None:
        return domain, objective
    Y, R, P, Q, W, U, V = match
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3 and Y in G.args:
            A, B, Y = match_ABY(G, Y)

            eliminant = Area(P, W, Q, R) / Area(P, U, Q, V) * Area(A, U, B, V) + Area(A, B, W)
            eliminant = eliminant.doit()

            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective
