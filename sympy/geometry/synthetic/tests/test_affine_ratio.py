from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine
)
from sympy.geometry.synthetic.affine import area_method_affine
from sympy.core.symbol import symbols, Symbol
from sympy.core.numbers import Integer, Rational


def test_ratio_lratio():
    P, Q = symbols('P Q')
    A, Y, C, D = symbols('A Y C D')
    l = Symbol('lambda')

    objective = Ratio(A, Y, C, D)

    constructions = [LRatio(Y, P, Q, l)]
    desired = Area(A, P, Q) / Area(C, P, D, Q)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [On(A, Line(P, Q)), LRatio(Y, P, Q, l)]
    desired = (Ratio(A, P, P, Q) + l) / Ratio(C, D, P, Q)
    assert area_method_affine(constructions, objective - desired) == 0


def test_ratio_inter_line_line():
    P, Q = symbols('P Q')
    U, V = symbols('U V')
    A, Y, C, D = symbols('A Y C D')

    objective = Ratio(A, Y, C, D)

    constructions = [
        Intersection(Y, Line(P, Q), Line(U, V))
    ]
    desired = Area(A, U, V) / Area(C, U, D, V)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [
        Intersection(Y, Line(U, V), Line(P, Q)),
        On(A, PLine(Y, C, D))
    ]
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [
        On(A, Line(U, V)),
        Intersection(Y, Line(P, Q), Line(U, V))
    ]
    desired = Area(A, P, Q) / Area(C, P, D, Q)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [
        On(A, Line(U, V)),
        Intersection(Y, Line(U, V), Line(P, Q))
    ]
    assert area_method_affine(constructions, objective - desired) == 0


def test_ratio_pratio():
    P, Q, R = symbols('P Q R')
    A, Y, C, D = symbols('A Y C D')
    l = Symbol('lambda')

    objective = Ratio(A, Y, C, D)

    constructions = [PRatio(Y, R, P, Q, l)]
    desired = Area(A, P, R, Q) / Area(C, P, D, Q)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [PRatio(Y, R, P, Q, l), On(A, Line(R, Y))]
    desired = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
    assert area_method_affine(constructions, objective - desired) == 0


def test_ratio_inter_pline_line():
    P, Q, R = symbols('P Q R')
    U, V = symbols('U V')
    A, Y, C, D = symbols('A Y C D')

    objective = Ratio(A, Y, C, D)

    constructions = [Intersection(Y, PLine(R, P, Q), Line(U, V))]
    desired = Area(A, U, V) / Area(C, U, D, V)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [On(A, Line(U, V)), Intersection(Y, PLine(R, P, Q), Line(U, V))]
    desired = Area(A, P, R, Q) / Area(C, P, D, Q)
    assert area_method_affine(constructions, objective - desired) == 0


def test_ratio_inter_pline_pline():
    P, Q, R = symbols('P Q R')
    U, V, W = symbols('U V W')
    A, Y, C, D = symbols('A Y C D')

    objective = Ratio(A, Y, C, D)

    constructions = [Intersection(Y, PLine(R, P, Q), PLine(W, U, V))]
    desired = Area(A, P, R, Q) / Area(C, P, D, Q)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [
        Intersection(Y, PLine(W, U, V), PLine(R, P, Q)),
        On(A, PLine(Y, C, D))
    ]
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
        On(A, Line(R, Y))
    ]
    desired = Area(A, U, W, V) / Area(C, U, D, V)
    assert area_method_affine(constructions, objective - desired) == 0

    constructions = [
        Intersection(Y, PLine(W, U, V), PLine(R, P, Q)),
        On(A, Line(R, Y))
    ]
    assert area_method_affine(constructions, objective - desired) == 0


def test_eliminate_ratio_pratio_consistency_1():
    P, Q, R = symbols('P Q R')
    A, B, Y = symbols('A B Y')
    C, D = symbols('C D')
    S = Symbol('S')
    O = Symbol('O')
    l = Symbol('lambda')

    construction = [
        LRatio(O, Q, R, Rational(1, 2)),
        LRatio(S, P, O, Integer(2)),
        LRatio(Y, R, S, l)
    ]
    lhs = Ratio(A, Y, C, D)
    rhs = Area(A, P, R, Q) / Area(C, P, D, Q)
    objective = lhs - rhs
    assert area_method_affine(construction, objective) == Integer(0)


def test_eliminate_ratio_pratio_consistency_2():
    P, Q, R = symbols('P Q R')
    A, B, Y = symbols('A B Y')
    C, D = symbols('C D')
    X1, X2, X3, X4 = symbols('X1 X2 X3 X4')
    l = Symbol('lambda')
    m1, m2 = symbols('mu_1 mu_2')

    construction = [
        LRatio(X1, Q, R, Rational(1, 2)),
        LRatio(X2, P, X1, Integer(2)),

        LRatio(X3, Q, C, Rational(1, 2)),
        LRatio(X4, P, X3, Integer(2)),
        LRatio(D, C, X4, m2),

        LRatio(Y, R, X2, l),
        LRatio(A, R, Y, m1),
    ]

    lhs = Ratio(A, Y, C, D)
    rhs = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
    objective = lhs - rhs
    assert area_method_affine(construction, objective) == Integer(0)


# XXX Add more consistency tests if we find more elementary constructions
# for existing elimination methods.
