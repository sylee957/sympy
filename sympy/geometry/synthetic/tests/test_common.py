from sympy.core.symbol import symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio


def test_uniformize_area():
    A, B, C = symbols("A B C")
    assert Area(A, B, C).doit() == Area(A, B, C)
    assert Area(A, C, B).doit() == -Area(A, B, C)
    assert Area(B, A, C).doit() == -Area(A, B, C)
    assert Area(B, C, A).doit() == Area(A, B, C)
    assert Area(C, A, B).doit() == Area(A, B, C)
    assert Area(C, B, A).doit() == -Area(A, B, C)


def test_uniformize_pythagoras():
    A, B, C = symbols("A B C")
    assert Pythagoras(A, B, C).doit() == Pythagoras(A, B, C)
    assert Pythagoras(A, C, B).doit() == Pythagoras(A, C, B)
    assert Pythagoras(B, A, C).doit() == Pythagoras(B, A, C)
    assert Pythagoras(B, C, A).doit() == Pythagoras(A, C, B)
    assert Pythagoras(C, A, B).doit() == Pythagoras(B, A, C)
    assert Pythagoras(C, B, A).doit() == Pythagoras(A, B, C)
    assert Pythagoras(A, B, A).doit() == Pythagoras(A, B, A)
    assert Pythagoras(B, A, B).doit() == Pythagoras(A, B, A)


def test_simplify_area():
    A, B, C = symbols("A B C")
    assert Area(A, A, A).doit() == 0
    assert Area(A, A, B).doit() == 0
    assert Area(A, B, A).doit() == 0
    assert Area(B, A, A).doit() == 0


def test_simplify_ratio():
    A, B, C, D = symbols("A B C D")
    assert Ratio(A, B, C, D).doit() == Ratio(A, B, C, D)
    assert Ratio(A, A, C, D).doit() == 0
    assert Ratio(A, B, A, B).doit() == 1
    assert Ratio(A, B, B, A).doit() == -1


def test_simplify_pythagoras():
    A, B, C = symbols("A B C")
    assert Pythagoras(A, B, C).doit() == Pythagoras(A, B, C)
    assert Pythagoras(A, A, B).doit() == 0
    assert Pythagoras(A, B, B).doit() == 0
