from sympy.core.symbol import symbols
from sympy.geometry.synthetic.area_coordinates_orthogonal import _area_coordinates_pythagoras
from sympy.geometry.synthetic.area_coordinates_orthogonal import _area_coordinates_herron
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area


def test_area_coordinates_pythagoras():
    O, U, V = symbols('O U V')
    A, B, C = symbols('A B C')

    objective = Pythagoras(A, B, A)
    assert _area_coordinates_pythagoras(O, U, V, objective) == {
        objective: (
            Pythagoras(O, U, O) *
            (Area(O, V, A) - Area(O, V, B))**2 / Area(O, U, V)**2 +
            Pythagoras(O, V, O) *
            (Area(O, U, A) - Area(O, U, B))**2 / Area(O, U, V)**2
        )
    }

    objective = Pythagoras(A, B, C)
    assert _area_coordinates_pythagoras(O, U, V, objective) == {
        objective: (
            Pythagoras(A, B, A) / 2 +
            Pythagoras(B, C, B) / 2 -
            Pythagoras(A, C, A) / 2
        )
    }


def test_area_coordinates_herron():
    O, U, V = symbols('O U V')

    objective = Area(O, U, V)
    assert _area_coordinates_herron(O, U, V, objective) == {}

    objective = Area(O, U, V)**2
    assert _area_coordinates_herron(O, U, V, objective) == {
        objective: Pythagoras(O, U, O) * Pythagoras(O, V, O) / 16
    }

    objective = Area(O, U, V)**3
    assert _area_coordinates_herron(O, U, V, objective) == {
        objective: Pythagoras(O, U, O) * Pythagoras(O, V, O) * Area(O, U, V) / 16
    }

    objective = Area(O, U, V)**-2
    assert _area_coordinates_herron(O, U, V, objective) == {
        objective: 16 / (Pythagoras(O, U, O) * Pythagoras(O, V, O))
    }
