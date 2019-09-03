from __future__ import print_function, division

from sympy.core.containers import Tuple
from sympy.core.logic import fuzzy_and, fuzzy_bool
from sympy.core.relational import Eq
from sympy.core.sympify import _sympify
from sympy.core.singleton import S
from sympy.logic.boolalg import And

from .sets import Set, FiniteSet, ProductSet


class CartesianPower(Set):
    def __new__(cls, a, e, **assumptions):
        a, e = _sympify(a), _sympify(e)
        if not isinstance(a, Set):
            raise TypeError(
                "{} should be of type Set".format(a))

        if e.is_integer == False or e.is_nonnegative == False:
            raise ValueError(
                '{} should be a positive integer.'.format(e))

        # Nullary product of sets is *not* the empty set
        if e == 0:
            return FiniteSet(())

        if a == S.EmptySet:
            return a

        return super(CartesianPower, cls).__new__(cls, a, e, **assumptions)


    def _eval_Eq(self, other):
        if isinstance(other, ProductSet):
            self_base, self_exp = self.args
            other_sets = other.args

            if len(other_sets) == self_exp:
                equalities = [Eq(self_base, s) for s in other_sets]
                pred = And(*equalities)
                if fuzzy_bool(pred) is not None:
                    return pred

        elif isinstance(other, CartesianPower):
            self_base, self_exp = self.args
            other_base, other_exp = other.args

            pred = And(Eq(self_base, other_base), Eq(self_exp, other_exp))
            if fuzzy_bool(pred) is not None:
                return pred


    def _contains(self, element):
        s, exp = self.args

        if element.is_Symbol:
            return None

        if not isinstance(element, Tuple):
            return False

        if len(element) != exp:
            return False

        return fuzzy_and(
            fuzzy_bool(s.contains(e)) for e in element)


    def _eval_rewrite_as_ProductSet(self, *args, **kwargs):
        s, exp = self.args

        deep = kwargs.pop('deep', True)
        if deep:
            s = s.rewrite(ProductSet, deep=deep)

        if exp.is_Integer:
            new_args = [s]*exp
            return ProductSet(*new_args)