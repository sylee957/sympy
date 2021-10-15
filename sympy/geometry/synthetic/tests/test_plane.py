from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryTLine as TLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryBLine as BLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircle as Circle
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryMRatio as MRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryInversion as Inversion
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircumcenter as Circumcenter
from sympy.geometry.synthetic.predicates import SyntheticGeometryPerpendicular as Perpendicular
from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel
from sympy.geometry.synthetic.predicates import SyntheticGeometryHarmonic as Harmonic
from sympy.geometry.synthetic.predicates import SyntheticGeometryEqangle as Eqangle
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import tan
from sympy.core.symbol import symbols, Symbol
from sympy.polys.polytools import cancel
from sympy.core.numbers import Integer
from sympy.core.singleton import S
from sympy.geometry.synthetic.plane import area_method_plane


def test_orthocenter():
    # Exercise 3.36, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    D, E, F = symbols('D E F')
    A, B, C = symbols('A B C')
    E, F, H = symbols('E F H')
    K, L = symbols('K L')

    constructions = [
        Foot(E, B, A, C),
        Foot(F, A, B, C),
        Intersection(H, Line(A, F), Line(B, E))
    ]
    objective = Perpendicular(A, B, C, H)
    assert area_method_plane(constructions, objective) is S.true


def test_example_3_40():
    # 3.40, Machine Proofs in Geometry
    A, B, C = symbols('A B C')
    E, G = symbols('E G')

    constructions = [
        TRatio(E, A, B, Integer(1)),
        TRatio(G, A, C, -Integer(1)),
    ]

    objective = Perpendicular(E, C, G, B)
    assert area_method_plane(constructions, objective) == True


def test_example_3_41():
    # 3.41, Machine Proofs in Geometry
    A, B, C, D, F, M = symbols('A B C D F M')

    constructions = [
        TRatio(D, C, A, Integer(1)),
        TRatio(F, C, B, -Integer(1)),
        Midpoint(M, A, B)
    ]

    objective = Perpendicular(D, F, C, M)
    assert area_method_plane(constructions, objective) == True


def test_example_3_42():
    A, B, C, E, M, N, T, V = symbols('A B C E M N T V')
    M = Symbol('M')

    constructions = [
        On(M, Line(A, B)),
        TRatio(C, M, A, Integer(1)),
        TRatio(E, M, B, -Integer(1)),
        Midpoint(V, E, B),
        Intersection(N, Line(B, C), Circle(V, B)),
        Intersection(T, Line(B, C), Line(A, E))
    ]

    objective = Ratio(B, N, C, N) - Ratio(B, T, C, T)
    assert area_method_plane(constructions, objective) == 0


def test_example_3_43():
    A, B, C, D = symbols('A B C D')
    O, P, Q, R, S = symbols('O P Q R S')
    X, Y = symbols('X Y')
    r = Symbol('r')

    constructions = [
        MRatio(C, A, B, r),
        MRatio(D, A, B, -r),
        Intersection(P, Line(O, A), Line(X, Y)),
        Intersection(Q, Line(O, B), Line(X, Y)),
        Intersection(R, Line(O, C), Line(X, Y)),
        Intersection(S, Line(O, D), Line(X, Y)),
    ]

    objective = Harmonic(P, Q, S, R)
    assert area_method_plane(constructions, objective) == True


def test_example_3_44():
    A, G, X, O, P, Q, R, U = symbols('A G X O P Q R U')
    r1 = Symbol('r1')

    constructions = [
        LRatio(P, O, A, r1),
        Inversion(Q, P, O, A),
        Midpoint(U, P, O),
        Intersection(R, Line(O, X), Circle(U, O)),
        Inversion(G, R, O, A),
    ]

    objective = Perpendicular(G, Q, O, A)
    assert area_method_plane(constructions, objective) == True


def test_example_3_45():
    A, B, C = symbols('A B C')
    E, F, G = symbols('E F G')
    A1, B1, C1 = symbols('A1 B1 C1')
    r = Symbol('r')

    constructions = [
        Midpoint(E, A, C),
        TRatio(B1, E, A, r),
        Midpoint(F, B, C),
        TRatio(A1, F, C, r),
        Midpoint(G, A, B),
        TRatio(C1, G, B, -r),
    ]

    objective = Parallel(A1, C1, C, B1)
    assert area_method_plane(constructions, objective, algebraic=(r**2 - 3,)) == True


def test_example_3_51():
    A, B, C = symbols('A B C')
    D, M, N, J = symbols('D M N J')

    constructions = [
        Foot(D, A, B, C),
        On(J, Line(A, D)),
        Intersection(M, Line(A, B), Line(C, J)),
        Intersection(N, Line(A, C), Line(B, J)),
    ]

    objective = Eqangle(M, D, A, A, D, N)
    assert area_method_plane(constructions, objective) == True


def test_example_3_52():
    A, B = symbols('A B')
    C, O, P = symbols('C O P')
    r = Symbol('r')

    constructions = [
        On(O, BLine(A, B)),
        TRatio(P, B, A, r),
        Intersection(C, Line(A, P), Circle(O, A))
    ]

    objective = tan(A, C, B)
    ACB = area_method_plane(constructions, objective)
    objective = tan(A, O, B)
    AOB = area_method_plane(constructions, objective)

    assert cancel(AOB - 2 * ACB / (1 - ACB**2)) == 0


def test_example_3_65():
    Y, P = symbols('Y P')
    O1, O2 = symbols('O1 O2')

    constructions = [
        Intersection(Y, Circle(O1, P), Circle(O2, P))
    ]

    lhs = Area(Y, O1, O2) / Area(P, O1, O2)
    rhs = -1
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(Y, O2, P) / Area(P, O1, O2)
    rhs = 2 * Pythagoras(P, O2, O1) / Pythagoras(O1, O2, O1)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Area(Y, P, O1) / Area(P, O1, O2)
    rhs = 2 * Pythagoras(P, O1, O2) / Pythagoras(O1, O2, O1)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_example_3_67():
    O, A, B, C = symbols('O A B C')
    P, Q = symbols('P Q')

    constructions = [
        Circumcenter(O, A, B, C)
    ]

    lhs = Pythagoras(O, A, O)
    rhs = Pythagoras(A, B, A) * Pythagoras(A, C, A) * Pythagoras(B, C, B) / (64 * Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Pythagoras(A, B, O)
    rhs = Pythagoras(A, B, A) / 2
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    lhs = Pythagoras(A, O, B)
    rhs = Pythagoras(A, B, A) * (Pythagoras(A, C, A) * Pythagoras(B, C, B) - 32 * Area(A, B, C)**2) / (64 * Area(A, B, C)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    constructions = [
        On(Q, TLine(P, A, B)),
        Circumcenter(O, A, B, C)
    ]

    lhs = Area(P, Q, O)
    rhs = Area(P, Q, A) / 2 + Area(P, Q, B) / 2
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0
