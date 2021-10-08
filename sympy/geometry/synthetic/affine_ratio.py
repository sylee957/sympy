from sympy.geometry.synthetic.affine_match import (
    _match_inter_line_line,
    _match_pratio,
    _match_lratio,
    _match_inter_pline_line,
    _match_inter_pline_pline,
)
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel
from sympy.geometry.synthetic.common import match_AYCD
from sympy.geometry.synthetic.common import _inject_new_variables_and_eliminate
from sympy.geometry.synthetic.common import _compress
from sympy.core.singleton import S


def _eliminate_ratio_lratio(construction, constructions, domain, objective, area_method):
    match = _match_lratio(construction)
    if match is None:
        return domain, objective
    Y, P, Q, r = match

    for G in domain.symbols:
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions + (construction,), Collinear(A, P, Q))

            if assertion is S.true:
                eliminant = (Ratio(A, P, P, Q) + r) / Ratio(C, D, P, Q)
            else:
                eliminant = Area(A, P, Q) / Area(C, P, D, Q)
            if reciprocal:
                eliminant = 1 / eliminant

            eliminant = eliminant.doit()
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)

    return domain, objective


def _eliminate_ratio_pratio(construction, constructions, domain, objective, area_method):
    match = _match_pratio(construction)
    if match is None:
        return domain, objective
    Y, R, P, Q, r = match

    for G in domain.symbols:
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions + (construction,), Collinear(A, R, Y))

            if assertion is S.true:
                eliminant = (Ratio(A, R, P, Q) + r) / Ratio(C, D, P, Q)
            else:
                eliminant = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                eliminant = 1 / eliminant

            eliminant = eliminant.doit()
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)

    return domain, objective


def _eliminate_ratio_inter_line_line(construction, constructions, domain, objective, area_method):
    match = _match_inter_line_line(construction)
    if match is None:
        return domain, objective
    Y, P, Q, U, V = match

    for G in domain.symbols:
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions + (construction,), Collinear(A, U, V))

            if assertion is S.true:
                eliminant = Area(A, P, Q) / Area(C, P, D, Q)
            else:
                eliminant = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                eliminant = 1 / eliminant

            eliminant = eliminant.doit()
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)

    return domain, objective


def _eliminate_ratio_inter_pline_line(construction, constructions, domain, objective, area_method):
    match = _match_inter_pline_line(construction)
    if match is None:
        return domain, objective
    Y, R, P, Q, U, V = match

    for G in domain.symbols:
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions + (construction,), Collinear(A, U, V))

            if assertion is S.true:
                eliminant = Area(A, P, R, Q) / Area(C, P, D, Q)
            else:
                eliminant = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                eliminant = 1 / eliminant

            eliminant = eliminant.doit()
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)

    return domain, objective


def _eliminate_ratio_inter_pline_pline(construction, constructions, domain, objective, area_method):
    match = _match_inter_pline_pline(construction)
    if match is None:
        return domain, objective
    Y, R, P, Q, W, U, V = match

    for G in domain.symbols:
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions + (construction,), Parallel(A, Y, P, Q))

            if assertion is S.true:
                eliminant = Area(A, U, W, V) / Area(C, U, D, V)
            else:
                eliminant = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                eliminant = 1 / eliminant

            eliminant = eliminant.doit()
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)

    return domain, objective
