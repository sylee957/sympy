from sympy.core.symbol import symbols, Symbol
from sympy.core.singleton import S
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryTLine as TLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryBLine as BLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircle as Circle
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.plane import area_method_plane


def test_plane_refined_foot_area():
    # Exercise 3.35, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    D, E, F = symbols('D E F')
    A, B = symbols('A B')

    constructions = [
        On(A, PLine(B, U, V)),
        Foot(Y, P, U, V)
    ]
    objective = Area(A, B, Y) - Area(A, B, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(A, TLine(B, U, V)),
        Foot(Y, P, U, V)
    ]
    objective = Area(A, B, Y) - Area(A, B, P)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(A, Line(U, V)),
        Foot(Y, P, U, V)
    ]
    objective = Area(A, B, Y) - Area(U, B, V) * Pythagoras(P, U, A, V) / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(B, Line(U, V)),
        Foot(Y, P, U, V)
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
        Foot(Y, P, U, V)
    ]
    objective = Pythagoras(A, B, Y) - Pythagoras(A, B, P)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(A, TLine(B, U, V)),
        Foot(Y, P, U, V)
    ]
    objective = Pythagoras(A, B, Y) - Pythagoras(A, B, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        On(B, Line(U, V)),
        Foot(Y, P, U, V)
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
        Midpoint(A, M, N),
        Midpoint(B, M, N),
        Midpoint(P, M, N),
        Foot(Y, P, U, V)
    ]
    objective = Pythagoras(A, Y, B) - 16 * Area(P, U, V)**2 / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        Midpoint(A, M, N),
        Midpoint(B, M, N),
        Midpoint(U, M, N),
        Foot(Y, P, U, V)
    ]
    objective = Pythagoras(A, Y, B) - Pythagoras(P, U, V)**2 / Pythagoras(U, V, U)
    assert area_method_plane(constructions, objective) is S.Zero

    constructions = [
        Midpoint(A, M, N),
        Midpoint(U, M, N),
        Midpoint(B, K, L),
        Midpoint(V, K, L),
        Foot(Y, P, U, V)
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

    for G in [
        lambda X: Area(A, B, X),
        lambda X: Area(A, B, C, X),
        lambda X: Pythagoras(A, B, X),
        lambda X: Pythagoras(A, B, C, X),
    ]:
        lhs = G(Y)
        rhs = UYUV * G(V) + YVUV * G(U)

        objective = lhs - rhs
        assert area_method_plane(constructions, objective) == 0


def test_refined_inter_line_pline_quadratic():
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')

    UYUV = Area(U, P, R, Q) / Area(U, P, V, Q)
    YVUV = -Area(V, P, R, Q) / Area(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), PLine(R, P, Q))]

    def Q(Y):
        return Pythagoras(A, Y, B)

    lhs = Q(Y)
    rhs = UYUV*Q(V) + YVUV*Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_refined_inter_line_pline_ratio():
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')

    UYUV = Area(U, P, R, Q) / Area(U, P, V, Q)

    constructions = [
        Intersection(Y, Line(U, V), PLine(R, P, Q)),
        On(D, PLine(Y, E, F))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = Area(D, U, V) / Area(E, U, F, V)
    assert area_method_plane(constructions, lhs - rhs) == 0

    constructions = [
        Intersection(Y, Line(U, V), PLine(R, P, Q)),
        On(D, Line(U, V))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = (Ratio(D, U, U, V) + UYUV) / Ratio(E, F, U, V)
    assert area_method_plane(constructions, lhs - rhs) == 0


def test_refined_inter_line_tline_linear():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)
    YVUV = -Pythagoras(V, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), TLine(R, P, Q))]

    for G in [
        lambda X: Area(A, B, X),
        lambda X: Area(A, B, C, X),
        lambda X: Pythagoras(A, B, X),
        lambda X: Pythagoras(A, B, C, X),
    ]:
        lhs = G(Y)
        rhs = UYUV * G(V) + YVUV * G(U)
        assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_tline_quadratic():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)
    YVUV = -Pythagoras(V, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), TLine(R, P, Q))]

    def Q(Y):
        return Pythagoras(A, Y, B)

    lhs = Q(Y)
    rhs = UYUV*Q(V) + YVUV*Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_refined_inter_line_tline_ratio():
    Y, P, Q, R, U, V = symbols('Y P Q R U V')
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')

    UYUV = Pythagoras(U, P, R, Q) / Pythagoras(U, P, V, Q)

    constructions = [
        Intersection(Y, Line(U, V), TLine(R, P, Q)),
        On(D, PLine(Y, E, F))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = Area(D, U, V) / Area(E, U, F, V)
    assert area_method_plane(constructions, lhs - rhs) == 0

    constructions = [
        Intersection(Y, Line(U, V), TLine(R, P, Q)),
        On(D, Line(U, V))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = (Ratio(D, U, U, V) + UYUV) / Ratio(E, F, U, V)
    assert area_method_plane(constructions, lhs - rhs) == 0


def test_refined_inter_line_bline_linear():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    A, B, C = symbols('A B C')

    UYUV = (Pythagoras(U, P, Q) - Pythagoras(P, Q, P) / 2) / Pythagoras(U, P, V, Q)
    YVUV = -(Pythagoras(V, P, Q) - Pythagoras(P, Q, P) / 2) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), BLine(P, Q))]

    for G in [
        lambda X: Area(A, B, X),
        lambda X: Area(A, B, C, X),
        lambda X: Pythagoras(A, B, X),
        lambda X: Pythagoras(A, B, C, X),
    ]:
        lhs = G(Y)
        rhs = UYUV * G(V) + YVUV * G(U)
        assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_bline_quadratic():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    A, B, C = symbols('A B C')

    UYUV = (Pythagoras(U, P, Q) - Pythagoras(P, Q, P) / 2) / Pythagoras(U, P, V, Q)
    YVUV = -(Pythagoras(V, P, Q) - Pythagoras(P, Q, P) / 2) / Pythagoras(U, P, V, Q)

    constructions = [Intersection(Y, Line(U, V), BLine(P, Q))]

    def Q(Y):
        return Pythagoras(A, Y, B)

    lhs = Q(Y)
    rhs = UYUV*Q(V) + YVUV*Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_refined_inter_line_bline_ratio():
    Y, P, Q, U, V = symbols('Y P Q U V')
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')

    UYUV = (Pythagoras(U, P, Q) - Pythagoras(P, Q, P) / 2) / Pythagoras(U, P, V, Q)

    constructions = [
        Intersection(Y, Line(U, V), BLine(P, Q)),
        On(D, PLine(Y, E, F))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = Area(D, U, V) / Area(E, U, F, V)
    assert area_method_plane(constructions, lhs - rhs) == 0

    constructions = [
        Intersection(Y, Line(U, V), BLine(P, Q)),
        On(D, Line(U, V))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = (Ratio(D, U, U, V) + UYUV) / Ratio(E, F, U, V)
    assert area_method_plane(constructions, lhs - rhs) == 0


def test_refined_inter_line_circle_linear():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, O, P, U, V = symbols('Y O P U V')
    A, B, C = symbols('A B C')

    UYUV = 2 * Pythagoras(O, U, V) / Pythagoras(U, V, U)
    YVUV = (Pythagoras(O, V, O) - Pythagoras(O, U, O)) / Pythagoras(U, V, U)

    constructions = [Intersection(Y, Line(U, V), Circle(O, U))]

    for G in [
        lambda X: Area(A, B, X),
        lambda X: Area(A, B, C, X),
        lambda X: Pythagoras(A, B, X),
        lambda X: Pythagoras(A, B, C, X),
    ]:
        lhs = G(Y)
        rhs = UYUV * G(V) + YVUV * G(U)
        assert area_method_plane(constructions, lhs - rhs) is S.Zero


def test_refined_inter_line_circle_quadratic():
    # Exercise 3.37, Machine Proofs in Geometry
    Y, O, P, U, V = symbols('Y O P U V')
    A, B, C = symbols('A B C')

    UYUV = 2 * Pythagoras(O, U, V) / Pythagoras(U, V, U)
    YVUV = (Pythagoras(O, V, O) - Pythagoras(O, U, O)) / Pythagoras(U, V, U)

    constructions = [Intersection(Y, Line(U, V), Circle(O, U))]

    def Q(Y):
        return Pythagoras(A, Y, B)

    lhs = Q(Y)
    rhs = UYUV*Q(V) + YVUV*Q(U) - UYUV*YVUV*Pythagoras(U, V, U)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_refined_inter_line_circle_ratio():
    Y, O, P, U, V = symbols('Y O P U V')
    A, B, C = symbols('A B C')
    D, E, F = symbols('D E F')

    UYUV = 2 * Pythagoras(O, U, V) / Pythagoras(U, V, U)

    constructions = [
        Intersection(Y, Line(U, V), Circle(O, U)),
        On(D, PLine(Y, E, F))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = Area(D, U, V) / Area(E, U, F, V)
    assert area_method_plane(constructions, lhs - rhs) == 0

    constructions = [
        Intersection(Y, Line(U, V), Circle(O, U)),
        On(D, Line(U, V))
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = (Ratio(D, U, U, V) + UYUV) / Ratio(E, F, U, V)
    assert area_method_plane(constructions, lhs - rhs) == 0


def test_refined_inter_pline_pline():
    # Exercise 3.38, Machine Proofs in Geometry
    # XXX May add this as elimination strategy after completing the
    # elimination of length ratio
    Y = symbols('Y')
    U, V, W = symbols('U V W')
    P, Q, R = symbols('P Q R')
    A, B, C = symbols('A B C')

    r = Area(W, P, R, Q) / Area(U, P, V, Q)
    constructions = [Intersection(Y, PLine(W, U, V), PLine(R, P, Q))]

    for G in [
        lambda X: Area(A, C, X),
        lambda X: Area(A, B, C, X),
        lambda X: Pythagoras(A, B, X),
        lambda X: Pythagoras(A, B, C, X)
    ]:
        lhs = G(Y)
        rhs = G(W) + r*(G(V) - G(U))
        assert area_method_plane(constructions, lhs - rhs) == 0

    Q = lambda X: Pythagoras(A, X, B)
    lhs = Q(Y)
    rhs = Q(W) + r*(Q(V) - Q(U) + 2*Pythagoras(W, U, V)) - r*(1 - r)*Pythagoras(U, V, U)
    assert area_method_plane(constructions, lhs - rhs) == 0


def test_refined_inter_tline_tline_area():
    # Exercise 3.54, Machine Proofs in Geometry
    O, U, V = symbols('O U V')
    A, B = symbols('A B')
    Y = Symbol('Y')

    # AB and OU perpendicular
    constructions = [
        On(U, TLine(O, A, B)),
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]

    objective = Area(A, B, Y) - Area(A, B, U)
    assert area_method_plane(constructions, objective) == 0

    # AB and OV perpendicular
    constructions = [
        On(V, TLine(O, A, B)),
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]

    objective = Area(A, B, Y) - Area(A, B, V)
    assert area_method_plane(constructions, objective) == 0

    constructions = [
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]

    # A = U, B = V
    lhs = Area(A, B, Y).xreplace({A: U, B: V})
    rhs = Pythagoras(O, U, V)*Pythagoras(O, V, U) / (-16*Area(O, U, V))
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = O, B = U
    lhs = Area(A, B, Y).xreplace({A: O, B: U})
    rhs = Pythagoras(O, V, U)*Pythagoras(O, U, O) / (16*Area(O, U, V))
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = O, B = V
    lhs = Area(A, B, Y).xreplace({A: O, B: V})
    rhs = Pythagoras(O, U, V)*Pythagoras(O, V, O) / (16*Area(O, V, U))
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_refined_inter_tline_tline_pythagoras():
    # Exercise 3.54, Machine Proofs in Geometry
    O, U, V = symbols('O U V')
    A, B = symbols('A B')
    Y = Symbol('Y')

    # AB, OU Perpendicular
    constructions = [
        On(U, PLine(O, A, B)),
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]
    lhs = Pythagoras(A, B, Y)
    rhs = Pythagoras(A, B, U)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # AB, OV Perpendicular
    constructions = [
        On(V, PLine(O, A, B)),
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]
    lhs = Pythagoras(A, B, Y)
    rhs = Pythagoras(A, B, V)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = U, B = V
    constructions = [
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]
    lhs = Pythagoras(A, B, Y).xreplace({A: U, B: V})
    rhs = Pythagoras(O, U, V)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0


def test_refined_inter_tline_tline_quadratic():
    # Exercise 3.54, Machine Proofs in Geometry
    O, U, V = symbols('O U V')
    A, B = symbols('A B')
    Y = Symbol('Y')

    constructions = [
        Intersection(Y, TLine(U, U, O), TLine(V, V, O))
    ]

    # A = U, B = V
    lhs = Pythagoras(A, Y, B).xreplace({A: U, B: V})
    rhs = -Pythagoras(U, O, V) * Pythagoras(O, V, U) * Pythagoras(O, U, V) / (16 * Area(O, U, V)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = O, B = U
    lhs = Pythagoras(A, Y, B).xreplace({A: O, B: U})
    rhs = Pythagoras(O, U, O) * Pythagoras(O, V, U)**2 / (16 * Area(O, U, V)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = U, B = U
    lhs = Pythagoras(A, Y, B).xreplace({A: U, B: U})
    rhs = Pythagoras(O, U, O) * Pythagoras(O, V, U)**2 / (16 * Area(O, U, V)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = O, B = V
    lhs = Pythagoras(A, Y, B).xreplace({A: O, B: V})
    rhs = Pythagoras(O, V, O) * Pythagoras(O, U, V)**2 / (16 * Area(O, U, V)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = V, B = V
    lhs = Pythagoras(A, Y, B).xreplace({A: V, B: V})
    rhs = Pythagoras(O, V, O) * Pythagoras(O, U, V)**2 / (16 * Area(O, U, V)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # A = O, B = O
    lhs = Pythagoras(A, Y, B).xreplace({A: O, B: O})
    rhs = Pythagoras(O, U, O) * Pythagoras(O, V, O) * Pythagoras(U, V, U) / (16 * Area(O, U, V)**2)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0
