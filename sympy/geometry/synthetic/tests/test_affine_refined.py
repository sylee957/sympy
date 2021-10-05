from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine
)
from sympy.geometry.synthetic.affine import area_method_affine as area_method
from sympy.core.symbol import symbols
from sympy.core.numbers import Integer


# XXX These functions should be implemented as elimination strategies
# after the Geometric Information Base is implemented
# Only the automated proof for them are given at the moment.
def test_refined_inter_line_line_consistency():
    P, Q = symbols('P Q')
    U, V = symbols('U V')
    A, B, Y = symbols('A B Y')

    # AB || UV
    construction = [
        On(A, PLine(B, U, V)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, U)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # AB || PQ
    construction = [
        On(A, PLine(B, P, Q)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, P)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # A on UV
    construction = [
        On(A, Line(U, V)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(U, B, V) * Area(A, P, Q) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # B on UV
    construction = [
        On(B, Line(U, V)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, U, V) * Area(B, P, Q) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # A on PQ
    construction = [
        On(A, Line(P, Q)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(P, B, Q) * Area(A, U, V) / Area(P, U, Q, V)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # B on PQ
    construction = [
        On(B, Line(P, Q)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, P, Q) * Area(B, U, V) / Area(P, U, Q, V)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # U on AB
    construction = [
        On(U, Line(A, B)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = (Area(U, P, Q) * Area(A, B, V) - Area(V, P, Q) * Area(A, B, U)) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # V on AB
    construction = [
        On(V, Line(A, B)),
        Intersection(Y, Line(P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = (Area(U, P, Q) * Area(A, B, V) - Area(V, P, Q) * Area(A, B, U)) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)


def test_refined_inter_pline_line_consistency():
    P, Q, R = symbols('P Q R')
    U, V = symbols('U V')
    A, B, Y = symbols('A B Y')

    # AB || UV
    construction = [
        On(A, PLine(B, U, V)),
        Intersection(Y, PLine(R, P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, U)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # AB || PQ
    construction = [
        On(A, PLine(B, P, Q)),
        Intersection(Y, PLine(R, P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, R)
    area_method(construction, lhs - rhs)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # A on UV
    construction = [
        On(A, Line(U, V)),
        Intersection(Y, PLine(R, P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(U, B, V) * Area(A, P, R, Q) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # B on UV
    construction = [
        On(B, Line(U, V)),
        Intersection(Y, PLine(R, P, Q), Line(U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, U, V) * Area(B, P, R, Q) / Area(U, P, V, Q)
    area_method(construction, lhs - rhs)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # AY || PQ
    construction = [
        Intersection(Y, PLine(R, P, Q), Line(U, V)),
        On(A, PLine(Y, P, Q)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, U, V) * Area(B, Q, R, P) / Area(P, U, Q, V)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # BY || PQ
    construction = [
        Intersection(Y, PLine(R, P, Q), Line(U, V)),
        On(B, PLine(Y, P, Q)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(B, U, V) * Area(A, P, R, Q) / Area(P, U, Q, V)
    assert area_method(construction, lhs - rhs) == Integer(0)


def test_refined_inter_pline_pline_consistency():
    P, Q, R = symbols('P Q R')
    U, V, W = symbols('U V W')
    A, B, Y = symbols('A B Y')

    # AB || UV
    construction = [
        On(A, PLine(B, U, V)),
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, W)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # AB || PQ
    construction = [
        On(A, PLine(B, P, Q)),
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, B, R)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # AY || PQ
    construction = [
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
        On(A, PLine(Y, P, Q)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, U, W, V) * Area(B, Q, R, P) / Area(P, U, Q, V)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # BY || PQ
    construction = [
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
        On(B, PLine(Y, P, Q)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(B, U, W, V) * Area(A, P, R, Q) / Area(P, U, Q, V)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # AY || UV
    construction = [
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
        On(A, PLine(Y, U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(B, V, W, U) * Area(A, P, R, Q) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # BY || UV
    construction = [
        Intersection(Y, PLine(R, P, Q), PLine(W, U, V)),
        On(B, PLine(Y, U, V)),
    ]
    lhs = Area(A, B, Y)
    rhs = Area(A, U, W, V) * Area(B, P, R, Q) / Area(U, P, V, Q)
    assert area_method(construction, lhs - rhs) == Integer(0)


def test_refined_area_simplify_consistency():
    P1, P2, P3, P4 = symbols('P1 P2 P3 P4')

    # P1P2 || P3P4
    construction = [
        On(P1, PLine(P3, P2, P4)),
    ]
    assert area_method(construction, Area(P1, P2, P3, P4)) == Integer(0)

    # P1P2P3 Collinear
    construction = [
        On(P1, Line(P2, P3)),
    ]
    lhs = Area(P1, P2, P3, P4)
    rhs = Area(P1, P3, P4)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # P2P3P4 Collinear
    construction = [
        On(P2, Line(P3, P4)),
    ]
    lhs = Area(P1, P2, P3, P4)
    rhs = Area(P1, P2, P4)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # P1P3P4 Collinear
    construction = [
        On(P1, Line(P3, P4)),
    ]
    lhs = Area(P1, P2, P3, P4)
    rhs = Area(P1, P2, P3)
    assert area_method(construction, lhs - rhs) == Integer(0)

    # P1P2P4 Collinear
    construction = [
        On(P1, Line(P2, P4)),
    ]
    lhs = Area(P1, P2, P3, P4)
    rhs = Area(P2, P3, P4)
    assert area_method(construction, lhs - rhs) == Integer(0)
