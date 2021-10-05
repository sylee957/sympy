from sympy.core.symbol import Symbol, symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.plane import area_method_plane


def test_tratio_area():
    P, Q = symbols('P Q')
    A, B, C = symbols('A B C')
    l = Symbol('lambda')
    Y = Symbol('Y')

    constructions = [TRatio(Y, P, Q, l)]
    objective = Area(A, B, Y)
    desired = Area(A, B, P) - l / 4 * Pythagoras(P, A, Q, B)
    assert area_method_plane(constructions, objective - desired) == 0

    objective = Area(A, B, C, Y)
    desired = Area(A, B, C, P) - l / 4 * Pythagoras(P, A, Q, C)
    assert area_method_plane(constructions, objective - desired) == 0


def test_tratio_pythagoras():
    P, Q = symbols('P Q')
    A, B, C = symbols('A B C')
    l = Symbol('lambda')
    Y = Symbol('Y')

    constructions = [TRatio(Y, P, Q, l)]
    objective = Pythagoras(A, B, Y)
    desired = Pythagoras(A, B, P) - 4 * l * Area(P, A, Q, B)
    assert area_method_plane(constructions, objective - desired) == 0

    objective = Pythagoras(A, B, C, Y)
    desired = Pythagoras(A, B, C, P) - 4 * l * Area(P, A, Q, C)
    assert area_method_plane(constructions, objective - desired) == 0


def test_tratio_quadratic():
    P, Q = symbols('P Q')
    A, B = symbols('A B')
    l = Symbol('lambda')
    Y = Symbol('Y')

    constructions = [TRatio(Y, P, Q, l)]
    objective = Pythagoras(A, Y, B)
    desired = (
        Pythagoras(A, P, B) + l**2 * Pythagoras(P, Q, P) -
        4*l*(Area(A, P, Q) + Area(B, P, Q))
    )
    assert area_method_plane(constructions, objective - desired) == 0
