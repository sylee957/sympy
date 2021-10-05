from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import match_AYCD
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel


def _ratio_ECS1(C, objective, prove):
    Y, P, Q, l = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Collinear(A, P, Q))
            if assertion:
                subs[G] = (Ratio(A, P, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_ECS2(C, objective, prove):
    Y, P, Q, U, V = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Collinear(A, U, V))
            if assertion:
                subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_ECS3(C, objective, prove):
    Y, R, P, Q, l = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Collinear(A, R, Y))
            if assertion:
                subs[G] = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_ECS4(C, objective, prove):
    Y, U, V, R, P, Q = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Collinear(A, U, V))
            if assertion:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            else:
                subs[G] = Area(A, U, V) / Area(C, U, D, V)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs


def _ratio_ECS5(C, objective, prove):
    Y, R, P, Q, W, U, V = C.args
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and Y in G.args:
            reciprocal, A, Y, C, D = match_AYCD(G, Y)
            assertion = prove(Parallel(A, Y, P, Q))
            if assertion:
                subs[G] = Area(A, U, W, V) / Area(C, U, D, V)
            else:
                subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
            if reciprocal:
                subs[G] = 1 / subs[G]
    return subs
