from sympy.core.symbol import symbols, Symbol
from sympy.core.numbers import Rational
from sympy.geometry.synthetic.predicates import SyntheticGeometryEqpoints as Eqpoints
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryBLine as BLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryALine as ALine
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.plane import area_method_plane


def test_centroid():
    # Centroid Theorem
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')
    Y1, Y2 = symbols('Y1 Y2')
    Y = Symbol('Y')

    constructions = [
        Midpoint(D, B, C),
        Midpoint(E, C, A),
        Midpoint(F, A, B),
        Intersection(Y1, Line(A, D), Line(B, E)),
        Intersection(Y2, Line(B, E), Line(C, F))
    ]
    objective = Eqpoints(Y1, Y2)
    assert area_method_plane(constructions, objective) == True

    # Centroid Coordinates
    constructions = [
        Midpoint(D, B, C),
        Midpoint(E, C, A),
        Midpoint(F, A, B),
        Intersection(Y, Line(A, D), Line(B, E)),
    ]
    objective = Area(Y, A, B) / Area(A, B, C)
    assert area_method_plane(constructions, objective) == Rational(1, 3)
    objective = Area(Y, B, C) / Area(A, B, C)
    assert area_method_plane(constructions, objective) == Rational(1, 3)
    objective = Area(Y, C, A) / Area(A, B, C)
    assert area_method_plane(constructions, objective) == Rational(1, 3)


def test_orthocenter():
    # Orthocenter Theorem
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')
    Y1, Y2 = symbols('Y1 Y2')
    Y = Symbol('Y')

    # Orthocenter Coordinates
    constructions = [
        Foot(D, A, B, C),
        Foot(E, B, C, A),
        Foot(F, C, A, B),
        Intersection(Y1, Line(A, D), Line(B, E)),
        Intersection(Y2, Line(B, E), Line(C, F)),
    ]
    objective = Eqpoints(Y1, Y2)
    assert area_method_plane(constructions, objective) == True

    constructions = [
        Foot(D, A, B, C),
        Foot(E, B, C, A),
        Foot(F, C, A, B),
        Intersection(Y, Line(A, D), Line(B, E))
    ]

    lhs = Area(Y, B, C) / Area(A, B, C)
    rhs = Pythagoras(A, B, C)*Pythagoras(A, C, B) / (16*Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(Y, C, A) / Area(A, B, C)
    rhs = Pythagoras(B, A, C)*Pythagoras(B, C, A) / (16*Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(Y, A, B) / Area(A, B, C)
    rhs = Pythagoras(C, A, B)*Pythagoras(C, B, A) / (16*Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_circumcenter():
    # Circumcenter Theorem
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')
    Y1, Y2 = symbols('Y1 Y2')
    Y = Symbol('Y')

    constructions = [
        Intersection(Y1, BLine(A, B), BLine(B, C)),
        Intersection(Y2, BLine(B, C), BLine(C, A)),
    ]
    objective = Eqpoints(Y1, Y2)
    assert area_method_plane(constructions, objective) == True

    constructions = [
        Intersection(Y, BLine(A, B), BLine(B, C))
    ]

    lhs = Area(Y, B, C) / Area(A, B, C)
    rhs = Pythagoras(B, C, B)*Pythagoras(B, A, C) / (32*Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(Y, C, A) / Area(A, B, C)
    rhs = Pythagoras(A, C, A)*Pythagoras(A, B, C) / (32*Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(Y, A, B) / Area(A, B, C)
    rhs = Pythagoras(A, B, A)*Pythagoras(A, C, B) / (32*Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_incenter_outcenter():
    # Coordinate of C with respect to incenter/outcenter I and B, C
    A, B, C = symbols('A B C')
    I = Symbol('I')

    constructions = [
        Intersection(C, ALine(A, I, A, B, I), ALine(B, I, B, A, I))
    ]

    lhs = Area(C, A, B) / Area(I, A, B)
    rhs = -2*Pythagoras(I, A, B)*Pythagoras(I, B, A) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(C, B, I) / Area(I, A, B)
    rhs = Pythagoras(I, A, B)*Pythagoras(I, B, I) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(C, I, A) / Area(I, A, B)
    rhs = Pythagoras(I, B, A)*Pythagoras(I, A, I) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0
