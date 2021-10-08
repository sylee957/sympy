from sympy.core.symbol import symbols, Symbol
from sympy.core.singleton import S
from sympy.core.numbers import Integer, Rational
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
)
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.affine import area_method_affine


def test_area_lratio():
    P, Q = symbols('P Q')
    A, B, Y = symbols('A B Y')
    l = Symbol('lambda')

    constructions = [LRatio(Y, Line(P, Q), l)]
    objective = Area(A, B, Y)
    desired = l*Area(A, B, Q) + (S.One - l) * Area(A, B, P)
    assert area_method_affine(constructions, objective - desired) == 0


def test_area_pratio():
    P, Q, R = symbols('P Q R')
    A, B, Y = symbols('A B Y')
    l = Symbol('lambda')

    constructions = [PRatio(Y, R, Line(P, Q), l)]
    objective = Area(A, B, Y)
    desired = Area(A, B, R) + l * Area(A, P, B, Q)
    assert area_method_affine(constructions, objective - desired) == 0


def test_area_inter_line_line():
    P, Q = symbols('P Q')
    U, V = symbols('U V')
    A, B, Y = symbols('A B Y')

    constructions = [Intersection(Y, Line(U, V), Line(P, Q))]
    objective = Area(A, B, Y)
    desired = (Area(P, U, V) * Area(A, B, Q) + Area(Q, V, U) * Area(A, B, P)) / Area(P, U, Q, V)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [Intersection(Y, Line(P, Q), Line(U, V))]
    objective = Area(A, B, Y)
    desired = (Area(P, U, V) * Area(A, B, Q) + Area(Q, V, U) * Area(A, B, P)) / Area(P, U, Q, V)
    assert area_method_affine(constructions, objective - desired) == 0


def test_area_inter_pline_line():
    P, Q, R = symbols('P Q R')
    U, V = symbols('U V')
    A, B, Y = symbols('A B Y')

    constructions = [Intersection(Y, PLine(R, P, Q), Line(U, V))]
    objective = Area(A, B, Y)
    desired = (Area(P, U, Q, R) * Area(A, B, V) - Area(P, V, Q, R) * Area(A, B, U)) / Area(P, U, Q, V)
    assert area_method_affine(constructions, objective - desired) == 0


def test_area_inter_pline_pline():
    P, Q, R = symbols('P Q R')
    U, V, W = symbols('U V W')
    A, B, Y = symbols('A B Y')

    constructions = [Intersection(Y, PLine(R, P, Q), PLine(W, U, V))]
    objective = Area(A, B, Y)
    desired = Area(P, W, Q, R) / Area(P, U, Q, V) * Area(A, U, B, V) + Area(A, B, W)
    assert area_method_affine(constructions, objective - desired) == 0


def test_eliminate_area_pratio_consistency():
    P, Q, R = symbols('P Q R')
    A, B, Y = symbols('A B Y')
    S = Symbol('S')
    O = Symbol('O')
    l = Symbol('lambda')

    construction = [
        LRatio(O, Line(Q, R), Rational(1, 2)),
        LRatio(S, Line(P, O), Integer(2)),
        LRatio(Y, Line(R, S), l)
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, R) + l * Area(A, P, B, Q)
    objective = lhs - rhs
    assert area_method_affine(construction, objective) == Integer(0)


def test_eliminate_area_inter_line_pline_consistency():
    P, Q, R = symbols('P Q R')
    U, V = symbols('U V')
    A, B, Y = symbols('A B Y')
    X1, X2 = symbols('X1 X2')

    constructions = [
        LRatio(X1, Line(Q, R), Rational(1, 2)),
        LRatio(X2, Line(P, X1), Integer(2)),
        Intersection(Y, Line(R, X2), Line(U, V))
    ]

    lhs = Area(A, B, Y)
    rhs = (Area(P, U, Q, R) * Area(A, B, V) - Area(P, V, Q, R) * Area(A, B, U)) / Area(P, U, Q, V)
    assert area_method_affine(constructions, lhs - rhs) == Integer(0)


def test_eliminate_area_inter_pline_pline_consistency():
    P, Q, R = symbols('P Q R')
    U, V, W = symbols('U V W')
    A, B, Y = symbols('A B Y')
    X1, X2, X3, X4 = symbols('X1 X2 X3 X4')

    constructions = [
        LRatio(X1, Line(Q, R), Rational(1, 2)),
        LRatio(X2, Line(P, X1), Integer(2)),
        LRatio(X3, Line(V, W), Rational(1, 2)),
        LRatio(X4, Line(U, X3), Integer(2)),
        Intersection(Y, Line(R, X2), Line(W, X4))
    ]

    lhs = Area(A, B, Y)
    rhs = Area(P, W, Q, R) / Area(P, U, Q, V) * Area(A, U, B, V) + Area(A, B, W)
    assert area_method_affine(constructions, lhs - rhs) == Integer(0)


# XXX Add more consistency tests if we find more elementary constructions
# for existing elimination methods.
