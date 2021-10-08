from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometrySignedArea as Area,
    SyntheticGeometrySignedRatio as Ratio
)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryMidpoint as Midpoint
)
from sympy.geometry.synthetic.affine import area_method_affine as area_method
from sympy.core.symbol import symbols, Symbol
from sympy.logic.boolalg import true
from sympy.core.numbers import Integer, Rational
from sympy.simplify.radsimp import numer, denom


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


def test_menelaus_1():
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')
    constructions = [
        On(D, Line(B, C)),
        On(E, Line(A, C)),
        Intersection(F, Line(D, E), Line(A, B))
    ]
    objective = Ratio(A, F, F, B) * Ratio(B, D, D, C) * Ratio(C, E, E, A)
    assert area_method(constructions, objective).cancel() == -Integer(1)


def test_menelaus_2():
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')
    X, Y = symbols('X Y')
    constructions = [
        Intersection(D, Line(B, C), Line(X, Y)),
        Intersection(E, Line(A, C), Line(X, Y)),
        Intersection(F, Line(A, B), Line(X, Y))
    ]
    objective = Ratio(A, F, F, B) * Ratio(B, D, D, C) * Ratio(C, E, E, A)
    assert area_method(constructions, objective).cancel() == -Integer(1)


def test_gauss_line_1():
    A0, A1, A2, A3 = symbols('A0 A1 A2 A3')
    X, Y = symbols('X Y')
    M1, M2, M3 = symbols('M1 M2 M3')
    constructions = [
        Intersection(X, Line(A0, A3), Line(A1, A2)),
        Intersection(Y, Line(A2, A3), Line(A1, A0)),
        Midpoint(M1, Line(A1, A3)),
        Midpoint(M2, Line(A0, A2)),
        Midpoint(M3, Line(X, Y))
    ]
    objective = Area(M1, M2, M3)
    assert area_method(constructions, objective) == Integer(0)


def test_gauss_line_2():
    A0, A1, A2, A3 = symbols('A0 A1 A2 A3')
    X, Y, Z = symbols('X Y Z')
    M1, M2, M3 = symbols('M1 M2 M3')
    constructions = [
        Intersection(X, Line(A0, A3), Line(A1, A2)),
        Intersection(Y, Line(A2, A3), Line(A1, A0)),
        Midpoint(M1, Line(A1, A3)),
        Midpoint(M2, Line(A0, A2)),
        Midpoint(M3, Line(X, Y)),
        Intersection(Z, Line(M2, M1), Line(X, Y))
    ]
    objective = Ratio(X, M3, Y, M3) / Ratio(X, Z, Y, Z)
    assert area_method(constructions, objective) == Integer(1)


def test_trapezoid():
    A, B, C, D, E, F, G, H = symbols('A B C D E F G H')
    construction = [
        On(D, PLine(C, A, B)),
        On(E, Line(B, C)),
        Intersection(H, Line(A, D), PLine(E, A, B)),
        Intersection(F, Line(B, D), Line(E, H)),
        Intersection(G, Line(A, C), Line(E, F))
    ]
    objective = Ratio(E, F, A, B) + Ratio(H, G, A, B)
    assert area_method(construction, objective) == Integer(0)


def test_triangle_midpoint():
    A, B, C, D, M, P, Q = symbols('A B C D M P Q')

    construction = [
        On(C, Line(A, P)),
        Intersection(D, Line(B, P), PLine(C, A, B)),
        Intersection(Q, Line(A, D), Line(B, C)),
        Intersection(M, Line(A, B), Line(P, Q))
    ]
    objective = Ratio(A, M, B, M)
    assert area_method(construction, objective) == Integer(-1)


def test_pappus():
    A, B, C = symbols('A B C')
    A1, B1, C1 = symbols('A1 B1 C1')
    P, Q, S, T = symbols('P Q S T')

    construction = [
        On(C, Line(A, B)),
        On(C1, Line(A1, B1)),
        Intersection(P, Line(A1, B), Line(A, B1)),
        Intersection(Q, Line(A1, C), Line(A, C1)),
        Intersection(S, Line(B1, C), Line(B, C1)),
        Intersection(T, Line(B1, C), Line(P, Q)),
    ]
    objective = Ratio(B1, S, C, S) / Ratio(B1, T, C, T)
    assert area_method(construction, objective) == Integer(1)


def test_descargues():
    A, B, C = symbols('A B C')
    A1, B1, C1 = symbols('A1 B1 C1')
    S = Symbol('S')

    construction = [
        On(A1, Line(S, A)),
        Intersection(B1, Line(S, B), PLine(A1, A, B)),
        Intersection(C1, Line(S, C), PLine(A1, A, C)),
    ]
    objective = Parallel(B, C, B1, C1)
    assert area_method(construction, objective) is true


def test_pascal():
    A, B, C = symbols('A B C')
    A1, B1, C1 = symbols('A1 B1 C1')

    construction = [
        On(C, Line(A, B)),
        On(B1, PLine(A, B, A1)),
        Intersection(C1, Line(A1, B1), PLine(A, C, A1)),
    ]
    objective = Parallel(B, C1, B1, C)
    assert area_method(construction, objective) is true


def test_triangle_area():
    A, B, C = symbols('A B C')
    L, M, N = symbols('L M N')

    construction = [
        Midpoint(L, Line(A, B)),
        Midpoint(M, Line(B, C)),
        Midpoint(N, Line(C, A))
    ]
    objective = Area(L, M, N) / Area(A, B, C)
    assert area_method(construction, objective) == Rational(1, 4)

    A1, B1, C1 = symbols('A1 B1 C1')
    r1, r2, r3 = symbols('r1 r2 r3')

    construction = [
        LRatio(A1, Line(B, C), 1 / (r1 + 1)),
        LRatio(B1, Line(C, A), 1 / (r2 + 1)),
        LRatio(C1, Line(A, B), 1 / (r3 + 1)),
    ]
    objective = Area(A1, B1, C1) / Area(A, B, C)
    assert area_method(construction, objective) == (r1*r2*r3 + 1) / (r1*r2*r3 + r1*r2 + r1*r3 + r2*r3 + r1 + r2 + r3 + 1)


def test_parallelogram_area():
    A, B, C, D = symbols('A B C D')
    A1, B1 = symbols('A1 B1')
    A2 = Symbol('A2')
    r = Symbol('r')

    construction = [
        PRatio(D, C, Line(A, B), Integer(-1)),
        LRatio(A1, Line(C, D), r),
        LRatio(B1, Line(D, A), r),
        Intersection(A2, Line(A, A1), Line(B, B1))
    ]
    objective = Area(A, B, A2) / Area(A, B, C, D)
    assert area_method(construction, objective) == (1 - r) / (2*r**2 - 4*r + 4)


def test_quadrilateral_area():
    A, B, C, D = symbols('A B C D')
    E, F, G, H = symbols('E F G H')
    r1, r2 = symbols('r1 r2')
    I = Symbol('I')

    construction = [
        LRatio(E, Line(A, B), r1),
        LRatio(F, Line(D, C), r1),
        LRatio(H, Line(A, D), r2),
        LRatio(G, Line(B, C), r2),
        Intersection(I, Line(E, F), Line(H, G))
    ]
    objective = Ratio(H, I, G, I)
    assert area_method(construction, objective) == r1 / (r1 - 1)


def test_quadrilateral_grid():
    A, B, C, D = symbols('A B C D')
    n = Symbol('n')
    U, V, Q, X, Y = symbols('U V Q X Y')

    construction = [
        LRatio(X, Line(A, B), n / (2*n + 1)),
        LRatio(U, Line(D, C), n / (2*n + 1)),
        LRatio(Q, Line(D, C), (n + 1) / (2*n + 1)),
        PRatio(V, U, Line(D, C), 1 / (2*n + 1)),
        PRatio(Y, X, Line(A, B), 1 / (2*n + 1)),
    ]
    objective = (Area(Q, X, Y) + Area(U, X, V)) / Area(A, B, C, D)
    assert area_method(construction, objective) == 1 / (2*n + 1)


def test_73_configuration():
    P1, P2, P3, P4, P5, P6, P7 = symbols("P1:8")

    construction = [
        On(P3, Line(P1, P2)),
        On(P5, Line(P1, P4)),
        Intersection(P6, Line(P2, P4), Line(P3, P5)),
        Intersection(P7, Line(P2, P5), Line(P3, P4))
    ]
    objective = Area(P1, P6, P7)
    result = area_method(construction, objective)
    assert result.xreplace({Area(P1, P6, P7): Integer(0)})


def test_93_configuration_1():
    P1, P2, P3, P4, P5, P6, P7, P8, P9 = symbols("P1:10")
    r1, r2, r3, r4 = symbols('r1 r2 r3 r4')

    construction = [
        LRatio(P7, Line(P1, P3), r1),
        LRatio(P8, Line(P1, P5), r2),
        LRatio(P9, Line(P3, P5), r3),
        LRatio(P2, Line(P5, P7), r4),
        Intersection(P4, Line(P1, P9), Line(P2, P8)),
        Intersection(P6, Line(P3, P8), Line(P2, P9))
    ]
    objective = Area(P4, P6, P7) / Area(P1, P3, P5)
    result = area_method(construction, objective)
    assert numer(result) == (
        r1**3*r2**2*r3*r4**2 - r1**3*r2*r3**2*r4**2 - r1**2*r2**2*r3**2*r4**2
        + 2*r1**2*r2**2*r3**2*r4 - 2*r1**2*r2**2*r3*r4
        + 3*r1**2*r2*r3**2*r4**2 - 2*r1**2*r2*r3**2*r4 - 2*r1**2*r2*r3*r4**2
        + 2*r1**2*r2*r3*r4 + r1*r2**2*r3**2*r4**2 - 2*r1*r2**2*r3**2*r4
        - r1*r2**2*r3*r4**2 + 2*r1*r2**2*r3*r4 - 2*r1*r2*r3**2*r4**2
        + 2*r1*r2*r3**2*r4 + 2*r1*r2*r3*r4**2 - 2*r1*r2*r3*r4
    )
    assert denom(result) == (
        r1**2*r2*r3*r4**2 - r1*r2**2*r3*r4 + r1*r2**2*r4 + r1*r2*r3**2*r4
        - r1*r2*r3*r4**2 + r1*r2*r4**2 - r1*r2*r4 - r1*r3**2*r4 - r1*r3*r4**2
        + r1*r3*r4 - r2**2*r3**2 + 2*r2**2*r3 - r2**2 - r2*r3**2*r4
        + 2*r2*r3**2 + 3*r2*r3*r4 - 4*r2*r3 - 2*r2*r4 + 2*r2 + r3**2*r4
        - r3**2 + r3*r4**2 - 3*r3*r4 + 2*r3 - r4**2 + 2*r4 - 1
    )


def test_93_configuration_2():
    # TODO Verify the result with the example in
    # Chou, Shang-Ching & Gao, Xiao-Shan & Zhang, Jing-Zhong. (2021).
    # Area Method and Automated Reasoning in Affine Geometries.
    P1, P2, P3, P4, P5, P6, P7, P8, P9 = symbols("P1:10")
    r1, r2, r3, r4 = symbols('r1 r2 r3 r4')

    construction = [
        LRatio(P3, Line(P1, P7), r1),
        LRatio(P6, Line(P1, P4), r2),
        LRatio(P8, Line(P3, P6), r3),
        LRatio(P9, Line(P4, P7), r4),
        Intersection(P5, Line(P1, P8), Line(P3, P9)),
        Intersection(P2, Line(P4, P8), Line(P6, P9))
    ]
    objective = Area(P2, P5, P7) / Area(P1, P4, P7)
    result = area_method(construction, objective)
    assert numer(result) == (
        r1**3*r2*r3**2*r4 - r1**3*r2*r3**2 - 2*r1**3*r2*r3*r4 + 2*r1**3*r2*r3
        + r1**3*r2*r4 - r1**3*r2 + r1**3*r3**2*r4**2 - 2*r1**3*r3**2*r4
        + r1**3*r3**2 - 2*r1**3*r3*r4**2 + 4*r1**3*r3*r4 - 2*r1**3*r3
        + r1**3*r4**2 - 2*r1**3*r4 + r1**3 - r1**2*r2**2*r3**2*r4
        + r1**2*r2**2*r3*r4 - 2*r1**2*r2*r3**2*r4**2 + r1**2*r2*r3**2*r4
        + r1**2*r2*r3**2 + 3*r1**2*r2*r3*r4**2 - r1**2*r2*r3*r4
        - 2*r1**2*r2*r3 - r1**2*r2*r4**2 + r1**2*r2 - r1**2*r3**2*r4**2
        + 2*r1**2*r3**2*r4 - r1**2*r3**2 + 2*r1**2*r3*r4**2 - 4*r1**2*r3*r4
        + 2*r1**2*r3 - r1**2*r4**2 + 2*r1**2*r4 - r1**2 + r1*r2**3*r3**2*r4
        + 2*r1*r2**2*r3**2*r4**2 - r1*r2**2*r3**2*r4 - r1*r2**2*r3*r4**2
        - r1*r2**2*r3*r4 + r1*r2*r3**2*r4**2 - r1*r2*r3**2*r4
        - 3*r1*r2*r3*r4**2 + 3*r1*r2*r3*r4 + r1*r2*r4**2 - r1*r2*r4
        - r2**3*r3**2*r4**2 + r2**2*r3*r4**2
    )
    assert denom(result) == (
        r1**2*r2**2*r3**2 - r1**2*r2**2*r3 + 2*r1**2*r2*r3**2*r4
        - 2*r1**2*r2*r3**2 - 3*r1**2*r2*r3*r4 + 3*r1**2*r2*r3 + r1**2*r2*r4
        - r1**2*r2 + r1**2*r3**2*r4**2 - 2*r1**2*r3**2*r4 + r1**2*r3**2
        - 2*r1**2*r3*r4**2 + 4*r1**2*r3*r4 - 2*r1**2*r3 + r1**2*r4**2
        - 2*r1**2*r4 + r1**2 - 2*r1*r2**2*r3**2*r4 + r1*r2**2*r3*r4
        - 2*r1*r2*r3**2*r4**2 + 2*r1*r2*r3**2*r4 + 2*r1*r2*r3*r4**2
        - r1*r2*r3*r4 + r1*r3*r4**2 - r1*r3*r4 - r1*r4**2 + r1*r4
        + r2**2*r3**2*r4**2 - r2*r3*r4**2
    )


def test_transversals_quadrilateral():
    A, B, C, D, E, F, G, H, O = symbols('A B C D E F G H O')

    construction = [
        Intersection(E, Line(B, D), Line(A, O)),
        Intersection(F, Line(A, C), Line(B, O)),
        Intersection(G, Line(B, D), Line(C, O)),
        Intersection(H, Line(A, C), Line(D, O)),
    ]
    objective = Ratio(C, F, F, A) * Ratio(B, E, E, D) * Ratio(A, H, H, C) * Ratio(D, G, G, B)
    assert area_method(construction, objective) == Integer(1)


def test_transversals_pentagram():
    A, B, C, D, E = symbols('A B C D E')
    P, Q, R, S, T = symbols('P Q R S T')

    construction = [
        Intersection(P, Line(A, D), Line(B, E)),
        Intersection(Q, Line(A, C), Line(B, E)),
        Intersection(R, Line(B, D), Line(A, C)),
        Intersection(S, Line(B, D), Line(C, E)),
        Intersection(T, Line(A, D), Line(C, E)),
    ]

    objective = Ratio(A, T, P, D) * Ratio(D, R, S, B) * Ratio(B, P, Q, E) * Ratio(E, S, T, C) * Ratio(C, Q, R, A)
    assert area_method(construction, objective) == Integer(1)

    objective = Ratio(A, T, P, D) * Ratio(D, R, S, B) * Ratio(B, P, Q, E) * Ratio(E, S, T, C) * Ratio(C, Q, R, A)
    assert area_method(construction, objective) == Integer(1)


def test_pratt_kasapi():
    A, B, C, D, E = symbols('A B C D E')
    A1, B1, C1, D1, E1 = symbols('A1 B1 C1 D1 E1')

    construction = [
        Intersection(A1, PLine(B, C, A), PLine(A, E, B)),
        Intersection(B1, PLine(C, B, D), PLine(B, A, C)),
        Intersection(C1, PLine(D, C, E), PLine(C, B, D)),
        Intersection(D1, PLine(E, A, D), PLine(D, C, E)),
        Intersection(E1, PLine(A, B, E), PLine(E, A, D)),
    ]
    objective = Ratio(A1, B, B, B1) * Ratio(B1, C, C, C1) * Ratio(C1, D, D, D1) * Ratio(D1, E, E, E1) * Ratio(E1, A, A, A1)
    assert area_method(construction, objective) == Integer(1)
