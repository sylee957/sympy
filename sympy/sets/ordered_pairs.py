from __future__ import print_function, division

from sympy.core.basic import Basic
from sympy.core.sympify import _sympify
from sympy.core.singleton import S


class OrderedPair(Basic):
    def __new__(cls, A, B, **kwargs):
        A, B = _sympify(A), _sympify(B)
        obj = super(OrderedPair, cls).__new__(cls, A, B)
        return obj

    def __getitem__(self, i):
        if isinstance(i, slice):
            indices = i.indices(len(self))
            args = (self.args[i] for i in range(*indices))
            return self.func(*args)
        return self.args[i]

    def __len__(self):
        return len(self.args)

    def __contains__(self, item):
        return item in self.args

    def __iter__(self):
        return iter(self.args)

    def __eq__(self, other):
        if isinstance(other, Basic):
            return super(OrderedPair, self).__eq__(other)
        return self.args == other

    def __ne__(self, other):
        if isinstance(other, Basic):
            return super(OrderedPair, self).__ne__(other)
        return self.args != other

    def _eval_rewrite_as_FiniteSet(self, *args, **kwargs):
        from .sets import FiniteSet

        a, b = self.args

        reverse = kwargs.pop('reverse', False)
        notation = kwargs.pop('notation', 'kuratowski')
        deep = kwargs.pop('deep', True)

        if reverse:
            a, b = b, a

        if deep:
            if isinstance(a, OrderedPair):
                a = a.rewrite(FiniteSet, notation=notation, deep=deep)
            if isinstance(b, OrderedPair):
                b = b.rewrite(FiniteSet, notation=notation, deep=deep)

        if notation == 'wiener':
            return FiniteSet(
                FiniteSet(FiniteSet(a), S.EmptySet), FiniteSet(FiniteSet(b)))
        elif notation == 'kuratowski':
            return FiniteSet(FiniteSet(a), FiniteSet(a, b))
