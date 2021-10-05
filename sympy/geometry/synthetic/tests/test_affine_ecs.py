from sympy.geometry.synthetic.ecs import AffineECS2 as C4
from sympy.geometry.synthetic.ecs import AffineECS4 as C7
from sympy.geometry.synthetic.ecs import AffineECS5 as C8
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryRatio as AuxiliaryRatio
from sympy.core.numbers import Rational
from sympy.geometry.synthetic.affine_ecs import _construction_to_ecs
from sympy.core.symbol import symbols, Symbol


def test_to_ecs():
    Y = Symbol('Y')
    U, V, W = symbols('U V W')
    P, Q, R = symbols('P Q R')
    r = Symbol('r')

    assert _construction_to_ecs(On(Y, Line(P, Q))) == LRatio(Y, P, Q, AuxiliaryRatio(P, Y, P, Q))
    assert _construction_to_ecs(On(Y, PLine(R, P, Q))) == PRatio(Y, R, P, Q, AuxiliaryRatio(R, Y, P, Q))
    assert _construction_to_ecs(LRatio(Y, P, Q, r)) == LRatio(Y, P, Q, r)
    assert _construction_to_ecs(PRatio(Y, R, P, Q, r)) == PRatio(Y, R, P, Q, r)
    assert _construction_to_ecs(Midpoint(Y, P, Q)) == LRatio(Y, P, Q, Rational(1, 2))
    assert _construction_to_ecs(Intersection(Y, Line(P, Q), Line(U, V))) == C4(Y, P, Q, U, V)
    assert _construction_to_ecs(Intersection(Y, Line(U, V), PLine(R, P, Q))) == C7(Y, U, V, R, P, Q)
    assert _construction_to_ecs(Intersection(Y, PLine(R, P, Q), Line(U, V))) == C7(Y, U, V, R, P, Q)
    assert _construction_to_ecs(Intersection(Y, PLine(R, P, Q), PLine(W, U, V))) == C8(Y, R, P, Q, W, U, V)
