from __future__ import print_function, division

from sympy.core.basic import Basic
from sympy.core.function import Function, UndefinedFunction
from sympy.core.logic import fuzzy_bool, fuzzy_and
from sympy.core.singleton import S
from sympy.core.sympify import _sympify
from sympy.logic.boolalg import BooleanFunction

from .sets import ProductSet


class Relation(UndefinedFunction):
    """Symbolic relational representation as sets and a subset of its
    cartesian product.
    """
    def __new__(cls, *args, **kwargs):
        args = _sympify(args)

        if len(args) < 2:
            raise ValueError(
                'There should be at least 2 sets provided.')
        s_list, r = args[:-1], args[-1]

        s_product = ProductSet(*s_list)
        if not s_product.is_superset(r):
            raise ValueError(
                '{} is not a subset of the product {}.'.format(r, s_product))

        obj = super(Relation, cls).__new__(cls, *args, **kwargs)
        return obj


    @property
    def domains(self):
        return self.args[:-1]


    @property
    def pairs(self):
        return self.args[-1]


    @classmethod
    def eval(cls, *args, **kwargs):
        print(cls)
        contains = cls.pairs.contains(args)
        if contains == True:
            return S.true

        if len(args) != len(cls.domains):
            return S.false





