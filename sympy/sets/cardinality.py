from __future__ import print_function, division

from sympy.core.expr import Expr
from sympy.core.sympify import _sympify
from sympy.core.evaluate import global_evaluate

from .sets import Set


class Cardinality(Expr):
    """A symbolic cardinality object
    """
    def __new__(cls, a, evaluate=global_evaluate[0]):
        a = _sympify(a)

        if not isinstance(a, Set):
            raise ValueError('{} must be a valid sympy Set object'.format(a))

        if evaluate:
            if hasattr(a, '_eval_cardinality'):
                return a._eval_cardinality()

        return super(Cardinality, cls).__new__(cls, a)


