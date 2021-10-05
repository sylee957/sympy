from sympy.core.symbol import Symbol, symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.plane_tratio import _tratio_area
from sympy.geometry.synthetic.plane_tratio import _tratio_pythagoras
from sympy.geometry.synthetic.plane_tratio import _tratio_quadratic


def test_tratio_area():
    P, Q = symbols('P Q')
    A, B = symbols('A B')
    l = Symbol('lambda')
    Y = Symbol('Y')

    objective = Area(A, B, Y)
    desired = Area(A, B, P) - l / 4 * Pythagoras(P, A, Q, B)
    assert _tratio_area(Y, P, Q, l, objective) == {objective: desired}


def test_tratio_pythagoras():
    P, Q = symbols('P Q')
    A, B = symbols('A B')
    l = Symbol('lambda')
    Y = Symbol('Y')

    objective = Pythagoras(A, B, Y)
    desired = Pythagoras(A, B, P) - 4 * l * Area(P, A, Q, B)
    assert _tratio_pythagoras(Y, P, Q, l, objective) == {objective: desired}


def test_tratio_quadratic():
    P, Q = symbols('P Q')
    A, B = symbols('A B')
    l = Symbol('lambda')
    Y = Symbol('Y')

    objective = Pythagoras(A, Y, B)
    desired = (
        Pythagoras(A, P, B) + l**2 * Pythagoras(P, Q, P) -
        4*l*(Pythagoras(A, P, Q) + Pythagoras(B, P, Q))
    )
    assert _tratio_quadratic(Y, P, Q, l, objective) == {objective: desired}
