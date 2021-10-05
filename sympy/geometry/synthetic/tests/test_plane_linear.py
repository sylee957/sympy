from sympy.core.symbol import Symbol, symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.plane_linear import _linear_pratio
from sympy.geometry.synthetic.plane_linear import _linear_inter_line_line
from sympy.geometry.synthetic.plane_linear import _linear_foot


def test_linear_pratio():
    U, V, W = symbols('U V W')
    A, B, C = symbols('A B C')
    l = Symbol('lambda')
    Y = Symbol('Y')

    C = PRatio(Y, W, U, V, l)

    G = lambda Y: Area(A, B, Y)
    objective = G(Y)
    desired = G(W) + l * (G(V) - G(U))
    assert _linear_pratio(C, objective) == {objective: desired}

    G = lambda Y: Area(A, B, C, Y)
    objective = G(Y)
    desired = G(W) + l * (G(V) - G(U))
    assert _linear_pratio(C, objective) == {objective: desired}

    G = lambda Y: Pythagoras(A, B, Y)
    objective = G(Y)
    desired = G(W) + l * (G(V) - G(U))
    assert _linear_pratio(C, objective) == {objective: desired}

    G = lambda Y: Pythagoras(A, B, C, Y)
    objective = G(Y)
    desired = G(W) + l * (G(V) - G(U))
    assert _linear_pratio(C, objective) == {objective: desired}


def test_linear_inter_line_line():
    U, V = symbols('U V')
    P, Q = symbols('P Q')
    A, B, C = symbols('A B C')
    Y = Symbol('Y')

    C = Intersection(Y, Line(U, V), Line(P, Q))

    G = lambda Y: Area(A, B, Y)
    objective = G(Y)
    desired = (Area(U, P, Q) * G(V) - Area(V, P, Q) * G(U)) / Area(U, P, V, Q)
    assert _linear_inter_line_line(C, objective) == {objective: desired}

    G = lambda Y: Area(A, B, C, Y)
    objective = G(Y)
    desired = (Area(U, P, Q) * G(V) - Area(V, P, Q) * G(U)) / Area(U, P, V, Q)
    assert _linear_inter_line_line(C, objective) == {objective: desired}

    G = lambda Y: Pythagoras(A, B, Y)
    objective = G(Y)
    desired = (Area(U, P, Q) * G(V) - Area(V, P, Q) * G(U)) / Area(U, P, V, Q)
    assert _linear_inter_line_line(C, objective) == {objective: desired}

    G = lambda Y: Pythagoras(A, B, C, Y)
    objective = G(Y)
    desired = (Area(U, P, Q) * G(V) - Area(V, P, Q) * G(U)) / Area(U, P, V, Q)
    assert _linear_inter_line_line(C, objective) == {objective: desired}


def test_linear_foot():
    U, V = symbols('U V')
    P = Symbol('P')
    A, B, C = symbols('A B C')
    Y = Symbol('Y')

    C = Foot(Y, P, U, V)

    G = lambda Y: Area(A, B, Y)
    objective = G(Y)
    desired = (Pythagoras(P, U, V) * G(V) + Pythagoras(P, V, U) * G(U)) / Pythagoras(U, V, U)
    assert _linear_foot(C, objective) == {objective: desired}

    G = lambda Y: Area(A, B, C, Y)
    objective = G(Y)
    desired = (Pythagoras(P, U, V) * G(V) + Pythagoras(P, V, U) * G(U)) / Pythagoras(U, V, U)
    assert _linear_foot(C, objective) == {objective: desired}

    G = lambda Y: Pythagoras(A, B, Y)
    objective = G(Y)
    desired = (Pythagoras(P, U, V) * G(V) + Pythagoras(P, V, U) * G(U)) / Pythagoras(U, V, U)
    assert _linear_foot(C, objective) == {objective: desired}

    G = lambda Y: Pythagoras(A, B, C, Y)
    objective = G(Y)
    desired = (Pythagoras(P, U, V) * G(V) + Pythagoras(P, V, U) * G(U)) / Pythagoras(U, V, U)
    assert _linear_foot(C, objective) == {objective: desired}
