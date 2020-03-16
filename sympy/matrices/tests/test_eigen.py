from sympy import (
    Rational, Poly, Symbol, N, I, Abs, sqrt, exp, Float, sin,
    cos, symbols)
from sympy.abc import x, y
from sympy.core.singleton import S
from sympy.matrices import eye, Matrix
from sympy.matrices.dense import diag, MutableDenseMatrix
from sympy.matrices.common import _MinimalMatrix, _CastableMatrix
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
from sympy.matrices.immutable import ImmutableMatrix
from sympy.matrices.matrices import \
    NonSquareMatrixError, MatrixError, MatrixEigen
from sympy.polys.polytools import PurePoly
from sympy.simplify.simplify import simplify
from sympy.testing.pytest import slow, warns_deprecated_sympy, raises, XFAIL


class EigenOnlyMatrix(_MinimalMatrix, _CastableMatrix, MatrixEigen):
    pass


def test_charpoly():
    UA, K_i, K_w = symbols('UA K_i K_w')

    A = Matrix([[-K_i - UA + K_i**2/(K_i + K_w),       K_i*K_w/(K_i + K_w)],
                [           K_i*K_w/(K_i + K_w), -K_w + K_w**2/(K_i + K_w)]])

    charpoly = A.charpoly(x)

    assert charpoly == \
        Poly(x**2 + (K_i*UA + K_w*UA + 2*K_i*K_w)/(K_i + K_w)*x +
        K_i*K_w*UA/(K_i + K_w), x, domain='ZZ(K_i,K_w,UA)')

    assert type(charpoly) is PurePoly

    A = Matrix([[1, 3], [2, 0]])
    assert A.charpoly() == A.charpoly(x) == PurePoly(x**2 - x - 6)

    A = Matrix([[1, 2], [x, 0]])
    p = A.charpoly(x)
    assert p.gen != x
    assert p.as_expr().subs(p.gen, x) == x**2 - 3*x


def test_eigen():
    R = Rational

    assert eye(3).charpoly(x) == Poly((x - 1)**3, x)
    assert eye(3).charpoly(y) == Poly((y - 1)**3, y)

    M = Matrix([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])

    assert M.eigenvals(multiple=False) == {S.One: 3}
    assert M.eigenvals(multiple=True) == [1, 1, 1]

    assert M.eigenvects() == (
        [(1, 3, [Matrix([1, 0, 0]),
                 Matrix([0, 1, 0]),
                 Matrix([0, 0, 1])])])

    assert M.left_eigenvects() == (
        [(1, 3, [Matrix([[1, 0, 0]]),
                 Matrix([[0, 1, 0]]),
                 Matrix([[0, 0, 1]])])])

    M = Matrix([[0, 1, 1],
                [1, 0, 0],
                [1, 1, 1]])

    assert M.eigenvals() == {2*S.One: 1, -S.One: 1, S.Zero: 1}

    assert M.eigenvects() == (
        [
            (-1, 1, [Matrix([-1, 1, 0])]),
            ( 0, 1, [Matrix([0, -1, 1])]),
            ( 2, 1, [Matrix([R(2, 3), R(1, 3), 1])])
        ])

    assert M.left_eigenvects() == (
        [
            (-1, 1, [Matrix([[-2, 1, 1]])]),
            (0, 1, [Matrix([[-1, -1, 1]])]),
            (2, 1, [Matrix([[1, 1, 1]])])
        ])

    a = Symbol('a')
    M = Matrix([[a, 0],
                [0, 1]])

    assert M.eigenvals() == {a: 1, S.One: 1}

    M = Matrix([[1, -1],
                [1,  3]])
    assert M.eigenvects() == ([(2, 2, [Matrix(2, 1, [-1, 1])])])
    assert M.left_eigenvects() == ([(2, 2, [Matrix([[1, 1]])])])

    M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    a = R(15, 2)
    b = 3*33**R(1, 2)
    c = R(13, 2)
    d = (R(33, 8) + 3*b/8)
    e = (R(33, 8) - 3*b/8)

    def NS(e, n):
        return str(N(e, n))
    r = [
        (a - b/2, 1, [Matrix([(12 + 24/(c - b/2))/((c - b/2)*e) + 3/(c - b/2),
                              (6 + 12/(c - b/2))/e, 1])]),
        (      0, 1, [Matrix([1, -2, 1])]),
        (a + b/2, 1, [Matrix([(12 + 24/(c + b/2))/((c + b/2)*d) + 3/(c + b/2),
                              (6 + 12/(c + b/2))/d, 1])]),
    ]
    r1 = [(NS(r[i][0], 2), NS(r[i][1], 2),
        [NS(j, 2) for j in r[i][2][0]]) for i in range(len(r))]
    r = M.eigenvects()
    r2 = [(NS(r[i][0], 2), NS(r[i][1], 2),
        [NS(j, 2) for j in r[i][2][0]]) for i in range(len(r))]
    assert sorted(r1) == sorted(r2)

    eps = Symbol('eps', real=True)

    M = Matrix([[abs(eps), I*eps    ],
                [-I*eps,   abs(eps) ]])

    assert M.eigenvects() == (
        [
            ( 0, 1, [Matrix([[-I*eps/abs(eps)], [1]])]),
            ( 2*abs(eps), 1, [ Matrix([[I*eps/abs(eps)], [1]]) ] ),
        ])

    assert M.left_eigenvects() == (
        [
            (0, 1, [Matrix([[I*eps/Abs(eps), 1]])]),
            (2*Abs(eps), 1, [Matrix([[-I*eps/Abs(eps), 1]])])
        ])

    M = Matrix(3, 3, [1, 2, 0, 0, 3, 0, 2, -4, 2])
    M._eigenvects = M.eigenvects(simplify=False)
    assert max(i.q for i in M._eigenvects[0][2][0]) > 1
    M._eigenvects = M.eigenvects(simplify=True)
    assert max(i.q for i in M._eigenvects[0][2][0]) == 1
    M = Matrix([[Rational(1, 4), 1], [1, 1]])
    assert M.eigenvects(simplify=True) == [
        (Rational(5, 8) - sqrt(73)/8, 1, [Matrix([[-sqrt(73)/8 - Rational(3, 8)], [1]])]),
        (Rational(5, 8) + sqrt(73)/8, 1, [Matrix([[Rational(-3, 8) + sqrt(73)/8], [1]])])]
    assert M.eigenvects(simplify=False) == [
        (Rational(5, 8) - sqrt(73)/8, 1, [Matrix([[-1/(-Rational(3, 8) + sqrt(73)/8)], [1]])]),
        (Rational(5, 8) + sqrt(73)/8, 1, [Matrix([[8/(3 + sqrt(73))], [1]])])]

    m = Matrix([[1, .6, .6], [.6, .9, .9], [.9, .6, .6]])
    evals = { Rational(5, 4) - sqrt(385)/20: 1, sqrt(385)/20 + Rational(5, 4): 1, S.Zero: 1}
    assert m.eigenvals() == evals
    nevals = list(sorted(m.eigenvals(rational=False).keys()))
    sevals = list(sorted(evals.keys()))
    assert all(abs(nevals[i] - sevals[i]) < 1e-9 for i in range(len(nevals)))

    # issue 10719
    assert Matrix([]).eigenvals() == {}
    assert Matrix([]).eigenvects() == []

    # issue 15119
    raises(NonSquareMatrixError, lambda : Matrix([[1, 2], [0, 4], [0, 0]]).eigenvals())
    raises(NonSquareMatrixError, lambda : Matrix([[1, 0], [3, 4], [5, 6]]).eigenvals())
    raises(NonSquareMatrixError, lambda : Matrix([[1, 2, 3], [0, 5, 6]]).eigenvals())
    raises(NonSquareMatrixError, lambda : Matrix([[1, 0, 0], [4, 5, 0]]).eigenvals())
    raises(NonSquareMatrixError, lambda : Matrix([[1, 2, 3], [0, 5, 6]]).eigenvals(error_when_incomplete = False))
    raises(NonSquareMatrixError, lambda : Matrix([[1, 0, 0], [4, 5, 0]]).eigenvals(error_when_incomplete = False))

    # issue 15125
    from sympy.core.function import count_ops
    q = Symbol("q", positive = True)
    m = Matrix([[-2, exp(-q), 1], [exp(q), -2, 1], [1, 1, -2]])
    assert count_ops(m.eigenvals(simplify=False)) > count_ops(m.eigenvals(simplify=True))
    assert count_ops(m.eigenvals(simplify=lambda x: x)) > count_ops(m.eigenvals(simplify=True))

    assert isinstance(m.eigenvals(simplify=True, multiple=False), dict)
    assert isinstance(m.eigenvals(simplify=True, multiple=True), list)
    assert isinstance(m.eigenvals(simplify=lambda x: x, multiple=False), dict)
    assert isinstance(m.eigenvals(simplify=lambda x: x, multiple=True), list)


def test_issue_8240():
    # Eigenvalues of large triangular matrices
    n = 200

    diagonal_variables = [Symbol('x%s' % i) for i in range(n)]
    M = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        M[i][i] = diagonal_variables[i]
    M = Matrix(M)

    eigenvals = M.eigenvals()
    assert len(eigenvals) == n
    for i in range(n):
        assert eigenvals[diagonal_variables[i]] == 1

    eigenvals = M.eigenvals(multiple=True)
    assert set(eigenvals) == set(diagonal_variables)

    # with multiplicity
    M = Matrix([[x, 0, 0], [1, y, 0], [2, 3, x]])
    eigenvals = M.eigenvals()
    assert eigenvals == {x: 2, y: 1}

    eigenvals = M.eigenvals(multiple=True)
    assert len(eigenvals) == 3
    assert eigenvals.count(x) == 2
    assert eigenvals.count(y) == 1

# EigenOnlyMatrix tests
def test_eigenvals():
    M = EigenOnlyMatrix([[0, 1, 1],
                [1, 0, 0],
                [1, 1, 1]])
    assert M.eigenvals() == {2*S.One: 1, -S.One: 1, S.Zero: 1}

    # if we cannot factor the char poly, we raise an error
    m = Matrix([
        [3,  0,  0, 0, -3],
        [0, -3, -3, 0,  3],
        [0,  3,  0, 3,  0],
        [0,  0,  3, 0,  3],
        [3,  0,  0, 3,  0]])
    raises(MatrixError, lambda: m.eigenvals())


def test_eigenvects():
    M = EigenOnlyMatrix([[0, 1, 1],
                [1, 0, 0],
                [1, 1, 1]])
    vecs = M.eigenvects()
    for val, mult, vec_list in vecs:
        assert len(vec_list) == 1
        assert M*vec_list[0] == val*vec_list[0]


def test_left_eigenvects():
    M = EigenOnlyMatrix([[0, 1, 1],
                [1, 0, 0],
                [1, 1, 1]])
    vecs = M.left_eigenvects()
    for val, mult, vec_list in vecs:
        assert len(vec_list) == 1
        assert vec_list[0]*M == val*vec_list[0]


@slow
def test_bidiagonalize():
    M = Matrix([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])
    assert M.bidiagonalize() == M
    assert M.bidiagonalize(upper=False) == M
    assert M.bidiagonalize() == M
    assert M.bidiagonal_decomposition() == (M, M, M)
    assert M.bidiagonal_decomposition(upper=False) == (M, M, M)
    assert M.bidiagonalize() == M

    import random
    #Real Tests
    for real_test in range(2):
        test_values = []
        row = 2
        col = 2
        for _ in range(row * col):
            value = random.randint(-1000000000, 1000000000)
            test_values = test_values + [value]
        # L     -> Lower Bidiagonalization
        # M     -> Mutable Matrix
        # N     -> Immutable Matrix
        # 0     -> Bidiagonalized form
        # 1,2,3 -> Bidiagonal_decomposition matrices
        # 4     -> Product of 1 2 3
        M = Matrix(row, col, test_values)
        N = ImmutableMatrix(M)

        N1, N2, N3 = N.bidiagonal_decomposition()
        M1, M2, M3 = M.bidiagonal_decomposition()
        M0 = M.bidiagonalize()
        N0 = N.bidiagonalize()

        N4 = N1 * N2 * N3
        M4 = M1 * M2 * M3

        N2.simplify()
        N4.simplify()
        N0.simplify()

        M0.simplify()
        M2.simplify()
        M4.simplify()

        LM0 = M.bidiagonalize(upper=False)
        LM1, LM2, LM3 = M.bidiagonal_decomposition(upper=False)
        LN0 = N.bidiagonalize(upper=False)
        LN1, LN2, LN3 = N.bidiagonal_decomposition(upper=False)

        LN4 = LN1 * LN2 * LN3
        LM4 = LM1 * LM2 * LM3

        LN2.simplify()
        LN4.simplify()
        LN0.simplify()

        LM0.simplify()
        LM2.simplify()
        LM4.simplify()

        assert M == M4
        assert M2 == M0
        assert N == N4
        assert N2 == N0
        assert M == LM4
        assert LM2 == LM0
        assert N == LN4
        assert LN2 == LN0

    #Complex Tests
    for complex_test in range(2):
        test_values = []
        size = 2
        for _ in range(size * size):
            real = random.randint(-1000000000, 1000000000)
            comp = random.randint(-1000000000, 1000000000)
            value = real + comp * I
            test_values = test_values + [value]
        M = Matrix(size, size, test_values)
        N = ImmutableMatrix(M)
        # L     -> Lower Bidiagonalization
        # M     -> Mutable Matrix
        # N     -> Immutable Matrix
        # 0     -> Bidiagonalized form
        # 1,2,3 -> Bidiagonal_decomposition matrices
        # 4     -> Product of 1 2 3
        N1, N2, N3 = N.bidiagonal_decomposition()
        M1, M2, M3 = M.bidiagonal_decomposition()
        M0 = M.bidiagonalize()
        N0 = N.bidiagonalize()

        N4 = N1 * N2 * N3
        M4 = M1 * M2 * M3

        N2.simplify()
        N4.simplify()
        N0.simplify()

        M0.simplify()
        M2.simplify()
        M4.simplify()

        LM0 = M.bidiagonalize(upper=False)
        LM1, LM2, LM3 = M.bidiagonal_decomposition(upper=False)
        LN0 = N.bidiagonalize(upper=False)
        LN1, LN2, LN3 = N.bidiagonal_decomposition(upper=False)

        LN4 = LN1 * LN2 * LN3
        LM4 = LM1 * LM2 * LM3

        LN2.simplify()
        LN4.simplify()
        LN0.simplify()

        LM0.simplify()
        LM2.simplify()
        LM4.simplify()

        assert M == M4
        assert M2 == M0
        assert N == N4
        assert N2 == N0
        assert M == LM4
        assert LM2 == LM0
        assert N == LN4
        assert LN2 == LN0

    M = Matrix(18, 8, range(1, 145))
    M = M.applyfunc(lambda i: Float(i))
    assert M.bidiagonal_decomposition()[1] == M.bidiagonalize()
    assert M.bidiagonal_decomposition(upper=False)[1] == M.bidiagonalize(upper=False)
    a, b, c = M.bidiagonal_decomposition()
    diff = a * b * c - M
    assert abs(max(diff)) < 10**-12


def test_is_diagonalizable():
    a, b, c = symbols('a b c')
    m = EigenOnlyMatrix(2, 2, [a, c, c, b])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    assert not EigenOnlyMatrix(2, 2, [1, 1, 0, 1]).is_diagonalizable()

    m = EigenOnlyMatrix(2, 2, [0, -1, 1, 0])
    assert m.is_diagonalizable()
    assert not m.is_diagonalizable(reals_only=True)

    m = Matrix([[1, 0], [0, I]])
    assert m.is_diagonalizable()


@slow
def test_jordan_form_slow():
    m = Matrix([[0, 6, 3], [1, 3, 1], [-2, 2, 1]])
    P, J = m.jordan_form()


@XFAIL
def test_failing_jordan_form():
    # If we cannot factor the characteristic polynomial
    m = Matrix([
        [3, 0, 0, 0, -3],
        [0, -3, -3, 0, 3],
        [0, 3, 0, 3, 0],
        [0, 0, 3, 0, 3],
        [3, 0, 0, 3, 0]])
    m.jordan_form()


def test_jordan_form():
    m = Matrix([[-3, 1, -3], [20, 3, 10]])
    raises(NonSquareMatrixError, lambda: m.jordan_form())

    # the next two tests test the cases where the old
    # algorithm failed due to the fact that the block structure can
    # *NOT* be determined  from algebraic and geometric multiplicity alone
    # This can be seen most easily when one lets compute the J.c.f. of a matrix that
    # is in J.c.f already.
    m = Matrix([
        [2, 1, 0, 0],
        [0, 2, 1, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 2]])
    P, J = m.jordan_form()
    assert m == J.as_explicit()

    m = Matrix([
        [2, 1, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 2, 1],
        [0, 0, 0, 2]])
    P, J = m.jordan_form()
    assert m == J.as_explicit()

    A = Matrix([
        [2, 4, 1, 0],
        [-4, 2, 0, 1],
        [0, 0, 2, 4],
        [0, 0, -4, 2]])
    P, J = A.jordan_form()
    J = J.as_explicit()
    assert simplify(P*J) == A*P

    assert Matrix([1]).jordan_form() == \
        (Matrix([[1]]), BlockDiagMatrix(Matrix([1])))
    assert Matrix([1]).jordan_form(calc_transform=False) == \
        BlockDiagMatrix(Matrix([1]))

    # make sure that if the input has floats, the output does too
    m = Matrix([
        [                0.6875, 0.125 + 0.1875*sqrt(3)],
        [0.125 + 0.1875*sqrt(3),                 0.3125]])
    P, J = m.jordan_form()
    assert all(isinstance(x, Float) or x == 0 for x in P)
    assert all(isinstance(x, Float) or x == 0 for x in J)

    A = Matrix([
        [2, 4, 1, 0],
        [-4, 2, 0, 1],
        [0, 0, 2, 4],
        [0, 0, -4, 2]])
    p = 2 - 4*I
    q = 2 + 4*I

    Jmust = BlockDiagMatrix(
        Matrix([[p, 1], [0, p]]),
        Matrix([[q, 1], [0, q]]))
    P, J = A.jordan_form()
    assert J == Jmust
    assert (P * J - A * P).as_explicit().simplify() == Matrix.zeros(4, 4)

    # diagonalizable
    m = Matrix([[7, -12, 6], [10, -19, 10], [12, -24, 13]])
    Jmust = BlockDiagMatrix(Matrix([-1]), Matrix([1]), Matrix([1]))
    P, J = m.jordan_form()
    assert Jmust == J
    assert Jmust == m.diagonalize()[1]

    # complexity: one of eigenvalues is zero
    m = Matrix([[0, 1, 0], [-4, 4, 0], [-2, 1, 2]])
    # The blocks are ordered according to the value of their eigenvalues,
    # in order to make the matrix compatible with .diagonalize()
    Jmust = BlockDiagMatrix(Matrix([[2, 1], [0, 2]]), Matrix([2]))
    P, J = m.jordan_form()
    assert Jmust == J

    # complexity: all of eigenvalues are equal
    m = Matrix([[2, 6, -15], [1, 1, -5], [1, 2, -6]])
    # same here see 1456ff
    Jmust = BlockDiagMatrix(Matrix([[-1, 1], [0, -1]]), Matrix([-1]))
    P, J = m.jordan_form()
    assert Jmust == J

    # complexity: two of eigenvalues are zero
    m = Matrix([[4, -5, 2], [5, -7, 3], [6, -9, 4]])
    Jmust = BlockDiagMatrix(Matrix([[0, 1], [0, 0]]), Matrix([1]))
    P, J = m.jordan_form()
    assert Jmust == J

    m = Matrix([
        [6, 5, -2, -3],
        [-3, -1, 3, 3],
        [2, 1, -2, -3],
        [-1, 1, 5, 5]])
    Jmust = BlockDiagMatrix(
        Matrix([[2, 1], [0, 2]]), Matrix([[2, 1], [0, 2]]))
    P, J = m.jordan_form()
    assert Jmust == J

    m = Matrix([
        [6, 2, -8, -6],
        [-3, 2, 9, 6],
        [2, -2, -8, -6],
        [-1, 0, 3, 4]])
    # same here see 1456ff
    Jmust = BlockDiagMatrix(
        Matrix([-2]), Matrix([[2, 1], [0, 2]]), Matrix([2]))
    P, J = m.jordan_form()
    assert Jmust == J

    m = Matrix([[5, 4, 2, 1], [0, 1, -1, -1], [-1, -1, 3, 0], [1, 1, -1, 2]])
    assert not m.is_diagonalizable()
    Jmust = BlockDiagMatrix(
        Matrix([1]), Matrix([2]), Matrix([[4, 1], [0, 4]]))
    P, J = m.jordan_form()
    assert Jmust == J

    # checking for maximum precision to remain unchanged
    a = Float('1.0', precision=110)
    b = Float('2.0', precision=110)
    c = Float('3.14159265358979323846264338327', precision=110)
    d = Float('4.0', precision=110)
    m = Matrix([[a, b], [c, d]])
    P, J = m.jordan_form()
    J = J.as_explicit()
    for term in J._mat:
        if isinstance(term, Float):
            assert term._prec == 110

    # two non-orthogonal Jordan blocks with eigenvalue 1
    M = Matrix([
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1]])
    P, J = M.jordan_form()
    assert P == Matrix([
        [0, 1, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]])
    assert J == BlockDiagMatrix(
        Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]]),
        Matrix([1]))

    A = Matrix([
        [1, 1, 1, 0],
        [-2, -1, 0, -1],
        [0, 0, -1, -1],
        [0, 0, 2, 1]])
    P, J = A.jordan_form()
    assert P.expand() == Matrix([
        [    -I,          -I/2,      I,           I/2],
        [-1 + I,             0, -1 - I,             0],
        [     0, -S(1)/2 - I/2,      0, -S(1)/2 + I/2],
        [     0,             1,      0,             1]])
    assert J == BlockDiagMatrix(
        Matrix([[-I, 1], [0, -I]]), Matrix([[I, 1], [0, I]]))


def test_singular_values():
    x = Symbol('x', real=True)

    A = EigenOnlyMatrix([[0, 1*I], [2, 0]])
    # if singular values can be sorted, they should be in decreasing order
    assert A.singular_values() == [2, 1]

    A = eye(3)
    A[1, 1] = x
    A[2, 2] = 5
    vals = A.singular_values()
    # since Abs(x) cannot be sorted, test set equality
    assert set(vals) == set([5, 1, Abs(x)])

    A = EigenOnlyMatrix([[sin(x), cos(x)], [-cos(x), sin(x)]])
    vals = [sv.trigsimp() for sv in A.singular_values()]
    assert vals == [S.One, S.One]

    A = EigenOnlyMatrix([
        [2, 4],
        [1, 3],
        [0, 0],
        [0, 0]
        ])
    assert A.singular_values() == \
        [sqrt(sqrt(221) + 15), sqrt(15 - sqrt(221))]
    assert A.T.singular_values() == \
        [sqrt(sqrt(221) + 15), sqrt(15 - sqrt(221)), 0, 0]


def test_diagonalization():
    # make sure we use floats out if floats are passed in
    m = Matrix([[0, .5], [.5, 0]])
    P, D = m.diagonalize()
    D = D.as_explicit()
    assert all(isinstance(e, Float) for e in D.values())
    assert all(isinstance(e, Float) for e in P.values())
    _, D2 = m.diagonalize(reals_only=True)
    D2 = D2.as_explicit()
    assert D == D2

    m = Matrix([[1, 2+I], [2-I, 3]])
    assert m.is_diagonalizable()

    m = Matrix([[-3, 1], [-3, 20], [3, 10]])
    assert not m.is_diagonalizable()
    assert not m.is_symmetric()
    raises(NonSquareMatrixError, lambda: m.diagonalize())

    # diagonalizable
    m = diag(1, 2, 3)
    P, D = m.diagonalize()
    assert P == eye(3)
    assert D == BlockDiagMatrix(Matrix([[1]]), Matrix([[2]]), Matrix([[3]]))

    m = Matrix([[0, 1], [1, 0]])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    P, D = m.diagonalize()
    assert m * P == (P * D).as_explicit()

    m = Matrix([[1, 0], [0, 3]])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    P, D = m.diagonalize()
    assert m * P == (P * D).as_explicit()
    assert P == eye(2)
    assert D.as_explicit() == m

    m = Matrix([[1, 1], [0, 0]])
    assert m.is_diagonalizable()
    P, D = m.diagonalize()
    assert m * P == (P * D).as_explicit()

    m = Matrix([[1, 2, 0], [0, 3, 0], [2, -4, 2]])
    assert m.is_diagonalizable()
    P, D = m.diagonalize()
    assert m * P == (P * D).as_explicit()
    for i in P:
        assert i.as_numer_denom()[1] == 1

    m = Matrix([[1, 0], [0, 0]])
    assert m.is_diagonal()
    assert m.is_diagonalizable()
    P, D = m.diagonalize()
    assert m * P == (P * D).as_explicit()
    assert P == Matrix([[0, 1], [1, 0]])

    # diagonalizable, complex only
    m = Matrix([[0, 1], [-1, 0]])
    assert not m.is_diagonalizable(reals_only=True)
    raises(MatrixError, lambda: m.diagonalize(True))
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert m * P == (P * D).as_explicit()

    # not diagonalizable
    m = Matrix([[0, 1], [0, 0]])
    assert not m.is_diagonalizable()
    raises(MatrixError, lambda: m.diagonalize())

    m = Matrix([[-3, 1, -3], [20, 3, 10], [2, -2, 4]])
    assert not m.is_diagonalizable()
    raises(MatrixError, lambda: m.diagonalize())

    # symbolic
    a, b, c, d = symbols('a b c d')
    m = Matrix([[a, c], [c, b]])
    assert m.is_symmetric()
    assert m.is_diagonalizable()


def test_issue_15887():
    # Mutable matrix should not use cache
    a = MutableDenseMatrix([[0, 1], [1, 0]])
    assert a.is_diagonalizable() is True
    a[1, 0] = 0
    assert a.is_diagonalizable() is False

    a = MutableDenseMatrix([[0, 1], [1, 0]])
    a.diagonalize()
    a[1, 0] = 0
    raises(MatrixError, lambda: a.diagonalize())

    # Test deprecated cache and kwargs
    with warns_deprecated_sympy():
        a.is_diagonalizable(clear_cache=True)

    with warns_deprecated_sympy():
        a.is_diagonalizable(clear_subproducts=True)
