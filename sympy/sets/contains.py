from __future__ import print_function, division

from sympy.core import S
from sympy.core.relational import Eq, Ne
from sympy.core.expr import Expr
from sympy.logic.boolalg import BooleanFunction
from sympy.utilities.misc import func_name


class Contains(BooleanFunction, Expr):
    """
    Asserts that x is an element of the set S

    Examples
    ========

    >>> from sympy import Symbol, Integer, S
    >>> from sympy.sets.contains import Contains
    >>> Contains(Integer(2), S.Integers)
    True
    >>> Contains(Integer(-2), S.Naturals)
    False
    >>> i = Symbol('i', integer=True)
    >>> Contains(i, S.Naturals)
    Contains(i, Naturals)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Element_%28mathematics%29
    """
    @classmethod
    def eval(cls, x, s):
        from sympy.sets.sets import Set

        if not isinstance(s, Set):
            raise TypeError('expecting Set, not %s' % func_name(s))

        ret = s.contains(x)
        if not isinstance(ret, Contains) and (
                ret in (S.true, S.false) or isinstance(ret, Set)):
            return ret

    @property
    def binary_symbols(self):
        return set().union(*[i.binary_symbols
            for i in self.args[1].args
            if i.is_Boolean or i.is_Symbol or
            isinstance(i, (Eq, Ne))])

    def as_set(self):
        raise NotImplementedError()

    def _eval_expand_contains(self, **kwargs):
        from sympy.logic.boolalg import And, Or, Not, Xor
        from .sets import \
            Union, Intersection, Complement, SymmetricDifference, \
            ProductSet

        x, s = self.args

        if isinstance(s, Intersection):
            args = [Contains(x, arg) for arg in s.args]
            return And(*args)
        elif isinstance(s, Union):
            args = [Contains(x, arg) for arg in s.args]
            return Or(*args)
        elif isinstance(s, Complement):
            args = [Contains(x, arg) for arg in s.args]
            A, B = args
            return And(A, Not(B))
        elif isinstance(s, SymmetricDifference):
            args = [Contains(x, arg) for arg in s.args]
            A, B = args
            return Xor(A, B)
        return self

    def _eval_rewrite_as_Relational(self, *args, **kwargs):
        from .sets import FiniteSet
        from sympy.logic.boolalg import Or
        from sympy.core.relational import Relational, Eq

        x, s = self.args
        deep = kwargs.get('deep', True)
        if deep:
            s = s.rewrite(Relational, deep=deep)

        x, s = self.args

        if isinstance(s, FiniteSet):
            return Or(*[Eq(x, elem) for elem in s.args])
