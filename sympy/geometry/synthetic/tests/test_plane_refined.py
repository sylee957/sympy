from sympy.core.symbol import symbols
from sympy.core.singleton import S
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryTLine as TLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.plane import area_method_plane


def test_plane_refined_foot_area():
    # Exercise 3.35, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    D, E, F = symbols('D E F')
    A, B = symbols('A B')

    constructions = [
        On(A, PLine(B, U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Area(A, B, Y) - Area(A, B, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(A, TLine(B, U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Area(A, B, Y) - Area(A, B, P)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(A, Line(U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Area(A, B, Y) - Area(U, B, V) * Pythagoras(P, U, A, V) / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(B, Line(U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Area(A, B, Y) - Area(A, U, V) * Pythagoras(P, U, B, V) / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero


def test_plane_refined_foot_pythagoras():
    # Exercise 3.35, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    D, E, F = symbols('D E F')
    A, B = symbols('A B')

    constructions = [
        On(A, PLine(B, U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Pythagoras(A, B, Y) - Pythagoras(A, B, P)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(A, TLine(B, U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Pythagoras(A, B, Y) - Pythagoras(A, B, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(B, Line(U, V)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Pythagoras(A, B, Y) - Pythagoras(A, B, U) * Pythagoras(P, B, U) / Pythagoras(U, B, U)
    assert area_method_plane(constructions, objective) is S.Zero


def test_plane_refined_foot_quadratic():
    # Exercise 3.35, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    D, E, F = symbols('D E F')
    A, B = symbols('A B')
    K, L = symbols('K L')
    M, N = symbols('M N')

    constructions = [
        Midpoint(A, Line(M, N)),
        Midpoint(B, Line(M, N)),
        Midpoint(P, Line(M, N)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Pythagoras(A, Y, B) - 16 * Area(P, U, V)**2 / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        Midpoint(A, Line(M, N)),
        Midpoint(B, Line(M, N)),
        Midpoint(U, Line(M, N)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Pythagoras(A, Y, B) - Pythagoras(P, U, V)**2 / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        Midpoint(A, Line(M, N)),
        Midpoint(U, Line(M, N)),
        Midpoint(B, Line(K, L)),
        Midpoint(V, Line(K, L)),
        Foot(Y, P, Line(U, V))
    ]
    objective = Pythagoras(A, Y, B) + Pythagoras(P, V, U) * Pythagoras(P, U, V) / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero


def test_refined_inter_line_pline_linear():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Area(U, P, R, Q) / Area(U, P, V, Q)
    YVUV = -Area(V, P, R, Q) / Area(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), PLine(R, P, Q))]

    G = lambda X: Area(A, B, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero

    G = lambda X: Area(A, B, C, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero

    G = lambda X: Pythagoras(A, B, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero

    G = lambda X: Pythagoras(A, B, C, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_tline_linear_1():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)
    YVUV = -Pythagoras(V, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), TLine(R, P, Q))]

    G = lambda X: Area(A, B, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_tline_linear_2():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)
    YVUV = -Pythagoras(V, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), TLine(R, P, Q))]

    G = lambda X: Area(A, B, C, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_tline_linear_3():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)
    YVUV = -Pythagoras(V, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), TLine(R, P, Q))]

    G = lambda X: Pythagoras(A, B, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_tline_linear_4():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)
    YVUV = -Pythagoras(V, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), TLine(R, P, Q))]

    G = lambda X: Pythagoras(A, B, C, X)
    lhs = G(Y)
    rhs = UYUV * G(V) + YVUV * G(U)
    assert area_method_plane(constructions, lhs - rhs) is S.Zero
