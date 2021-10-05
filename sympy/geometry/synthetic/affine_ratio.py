from sympy.core.singleton import S
from sympy.geometry.synthetic.predicates import (
    SyntheticGeometryCollinear as Collinear,
    SyntheticGeometryParallel as Parallel)
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometrySignedArea as Area,
    SyntheticGeometrySignedRatio as Ratio)
from sympy.geometry.synthetic.common import (
    _geometric_quantities,
    match_AYCD
)


def _ratio_lratio(Y, P, Q, l, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions, Collinear(A, P, Q))
            if assertion is S.true:
                subs[G] = (Ratio(A, P, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_pratio(Y, R, P, Q, l, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions, Collinear(A, R, Y))
            if assertion is S.true:
                subs[G] = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_line_line(Y, P, Q, U, V, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions, Collinear(A, U, V))
            if assertion is S.true:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_pline_line(Y, R, P, Q, U, V, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions, Collinear(A, U, V))
            if assertion is S.true:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_pline_pline(Y, R, P, Q, W, U, V, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = area_method(constructions, Parallel(A, Y, P, Q))
            if assertion is S.true:
                subs[G] = Area(A, U, W, V) / Area(C, U, D, V)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs
