from __future__ import print_function, division

from sympy.core.expr import Expr
from sympy.core.compatibility import as_int
from sympy.core.power import Pow
from sympy.core.sympify import _sympify
from sympy.core.singleton import S
from sympy.core.evaluate import global_evaluate
from sympy.core.relational import Eq, Ge
from sympy.functions.elementary.piecewise import Piecewise


class Tetration(Expr):
    def __new__(cls, a, n):
        a, n = _sympify(a), _sympify(n)
        return super(Tetration, cls).__new__(cls, a, n)

    def doit(self, recurse=0):
        """Evaluate the tetration when `n` is an integer.

        Parameters
        ==========

        recurse : int
            Controls the maximum depth of evaluation.
        """
        a, n = self.args
        if n == 0:
            return 1

        if recurse <= 0:
            return self

        if n.is_Integer:
            return Pow(a, Tetration(a, n-1).doit(recurse=recurse-1))
        return self


class SudanF(Expr):
    def __new__(cls, x, y, n):
        x, y, n = _sympify(x), _sympify(y), _sympify(n)
        if n.is_integer == False or n.is_nonnegative == False:
            raise ValueError('{} must be a nonnegative integer.'.format(n))
        return super(SudanF, cls).__new__(cls, x, y, n)


    def do_one(self):
        x, y, n = self.args
        if n == 0:
            return x + y
        elif y == 0:
            return x
        elif n.is_Integer and y.is_Integer:
            return SudanF(SudanF(x, y-1, n), SudanF(x, y-1, n), n-1)
        return self


    def exhaust(self):
        prev = self
        do = prev.do_one()
        while do != prev:
            prev = do
            do = do.do_one()
        return do


class KnuthUpArrow(Expr):
    def __new__(cls, a, b, n):
        a, b, n = _sympify(a), _sympify(b), _sympify(n)

        if a.is_integer == False:
            raise ValueError('{} must be an integer.'.format(a))

        if b.is_integer == False or b.is_nonnegative == False:
            raise ValueError('{} must be a nonnegative integer.'.format(b))

        if n.is_integer == False or n.is_nonnegative == False:
            raise ValueError('{} must be a nonnegative integer.'.format(n))

        return super(KnuthUpArrow, cls).__new__(cls, a, b, n)


    def doit(self, deep=True):
        Arrow = lambda a, b, n: KnuthUpArrow(a, b, n)

        a, b, n = self.args

        if deep:
            a, b, n = a.doit(deep=deep), b.doit(deep=deep), n.doit(deep=deep)

        if n == 1:
            return self
        elif n >= 1 and b == 0:
            return S.One

        if b.is_Integer and n.is_Integer:
            return Arrow(a, Arrow(a, b-1, n), n-1)
        return self


class HyperoperationSequence(Expr):
    def __new__(cls, a, b, n):
        a, b, n = _sympify(a), _sympify(b), _sympify(n)

        if a.is_integer == False:
            raise ValueError('{} must be an integer.'.format(a))
        if b.is_integer == False or b.is_nonnegative == False:
            raise ValueError('{} must be a nonnegative integer.'.format(b))
        if n.is_integer == False or n.is_nonnegative == False:
            raise ValueError('{} must be a nonnegative integer.'.format(n))

        return super(HyperoperationSequence, cls).__new__(cls, a, b, n)


    def doit(self):
        H = HyperoperationSequence
        a, b, n = self.args

        if n == 0:
            return b + 1
        elif n == 1 and b == 0:
            return a
        elif n == 2 and b == 0:
            return S.Zero
        elif n >= 3 and b == 0:
            return S.One
        else:
            if b.is_Integer and n.is_Integer:
                return H(a, H(a, b-1, n), n-1)
            return self


    def level_down(self):
        H = HyperoperationSequence
        a, b, n = self.args

        if not b.is_number or not n.is_number:
            return self

        if n == 1 and b == 0:
            return a
        if n == 2 and b == 0:
            return S.Zero
        if n >= 3 and b == 0:
            return S.One
        return H(a, H(a, b-1, n).level_down(), n-1)
